### Randomized primitives

To study the effect of nonce misuse on randomized primitives, one needs to clarify which primitives are randomized.
The protocols studied can be put into two sets:
- Protocols that specify exactly the algorithms to use: LoRaWAN 1.0 OTAA, WPA2, WPA3, Bluetooth NC
- Protocols that specify a type of primitive but not its implementation: NSLPK, ISO 9798-2-4, 9798-2-6, 9798-3-4, 9798-4-4, Dragonfly

For all protocols that specify exactly the algorithm to use, we identify no randomized primitive amongst the studied protocol.
Note that for these, we model only the key agreement step, not the secure messaging that comes after key agreement.
In these key agreements, none of the primitives are randomized.
A specific note can be added for WPA2 and WPA3: the standard defines than an AP must transmit the Group Temporal Key (GTK) to the station, as well as other network parameters.
This GTK is sent encrypted by another key.
However, the encryption primitive used is AES NIST Key Wrap, which is not randomized.

For protocols that do not specify the exact primitive to use, their are four family of primitives that are defined:
- asymetric encryption: used in NSLPK
- authenticated encryption: used in ISO 9798-2-*
- signature: used in ISO 9798-3-4
- message authentication code: used in ISO 9798-4-4 and Dragonfly

We are aware that an unspecified MAC construction may be randomized, however the standardized MACs used in practice are not (e.g., AES-CMAC, HMAC-SHA256, etc.), so we do not consider MACs as possibly randomized primitives in our models.
For public key encryption, from the literature we identify no subtle flaw that may create problems when a nonce is misused with it.
For authenticated encryption, we reuse existing work that models subtle flaws in AEADs, in particular when it comes to the effect of nonce reuse.
For signature, we do not identify existing work that models subtle flaws in signature that arise from bad randomness, however we identify that commonly used ECDSA algorithm has well-documented flaws to that regard.
So, drawing from this example, a similar case of nonce misuse is modeled.

#### Authenticated Encryption

For authenticated encryption, we reuse the modeling from "Automated Analysis of Protocols that use Authenticated Encryption: How Subtle AEAD Differences can impact Protocol Security.", C. Cremers, A. Dax, C. Jacomme, M. Zhao.

In particular, we draw from their modeling of nonce reuse in AEAD primitives.
The two defined security models for that are NR-A1 and NR-A2.
In practice, NR-A1 leaks the encryption key if two distinct messages have been encrypted with the same nonce and key. 
NR-A2 leaks the messages if two distinct messages have been encrypted with the same nonce and key.

```
restriction notsame:
 "All x y #i. NotM(x,y)@i ==> not(x=y)"

// NR-A1
#ifdef n_reuse_keyleak 
rule n_reuse_keyleak:
    [ In(senc(k,m,n,ad)), In(senc(k,m2,n,ad)), !Key(k)]
  --[ NotM(m,m2)]->
    [ Out(k) ]
#endif

// NR-A2
#ifdef n_reuse_messleak
rule n_reuse_messleak:
    [ In(senc(k,m,n,ad)), In(senc(k,m2,n,ad)), !M(m), !M(m2)]
  --[ NotM(m,m2)]->
    [ Out(<m,m2>) ]
#endif
```

Note that there is a clear hierarchy between security models.
The 'Standard' models consists of the randomized primitive without further modeling of possible weaknesses.
Hence, the stronger attacker is the NR-A1 model.
NR-A2 is strictly weaker because if an NR-A1 attacker manages to leak a key, then it can decrypt messages m and m2.
As a result, if an attack is identified in NR-A2, we know that an attack will be identified in NR-A1.
The reverse is true: if a security property is proven in NR-A1 (i.e., there are no attacks on this property in the studied case), then there won't be any attack on it in NR-A2.
The standard model is by contrast the weaker attacker, so any property falsified for some studied case in this model is sure to be falsified in NR-A1 and NR-A2.

The models ISO 9798-2-6 models that consider randomized primitives take a significantly longer time to run.
When studying only nonce and key misgeneration, there are 19 models that take a total of 288 seconds to run.
When studying the effect of randomized primitives, there are 53 models.
In the "Standard" security models, it takes 16030 seconds to run.
In the "NR-A1" security model, it takes 106911 seconds to run.
For the "NR-A2" security model, only cases that were proven secure in "Standard" and insecure in "NR-A1" have been considered, following the hierarchy of security models.
To allow Tamarin to conclude, more restrictions were added (the files are in models/randomized-primitives/9798-2-6-messleak) and the 4 models take a total of 2583 seconds to run.

There is only one case that Tamarin was not able to conclude automatically on: the reuse of kAB as RA2 in the "Standard" model" (models/randomized-primitives/9798-2-6/979826_reuse_once_2_5.spthy).
However, we highlight that the case RA2 = kAB is already covered the file 'models/nonce_and_keys/9798-2-6/979826_reuse_once_2_3_results.spthy' that does not model randomness inside AEADs.
All security properties fail if RA2 = kAB, even in a "Standard" model.

#### Signature

For signature, we identify no previous work that models the adverse effects of nonce reuse from signatures.
However, we draw from the famous example of (EC)DSA, that is still a popular choice of signature algorithm to this day.

This algorithm takes as input a signing key, a random nonce, and a message.
It outputs a signature.
If the random nonce is known to the attacker, it is possible to recover the signing key from the nonce, the message and the signature.
Also, if a signer signs two distinct messages with the same signing key and nonce, an attacker has the ability to recover the nonce used from the two signatures and messages, then to recover the signing key.

This is modeled in attacker model NR-S:

```
#ifdef nmisuse
restriction ineq:
 "All x y #i. InEq(x,y)@i ==> not(x=y)"

rule n_leak:
    [In(sign(m, s, n)),
     In(n), In(m), !Key(s)]
    -->
    [Out(s)]

rule n_reuse:
    [In(sign(m1, s, n)), In(sign(m2, s, n)),
     In(m1), In(m2),
     !Key(s)]
    --[InEq(m1, m2)]->
    [Out(s)]
#endif

Overall, all models run without difficulty with this representation.
The "Standard" security model considers that signatures are randomized but there are no adverse effects to reusing the same nonce in a signature.
There are 19 models for this case, that overall run in 655 seconds.
In NR-S, all models run in 6784 seconds.
