### Results table

This folder contains all the tables as PDF.
The results have been discussed in the paper.
A few additional details are mentioned here

It is possible to recreate the tables from the results files present in the provided directories.
The script `create_all_tables.py` is a Python script that parses all results and re-create LaTeX files.
Then, LaTeX can be used to recompile them all ; the script 'make_all.sh' does that and relies on pdflatex.

#### WPA3

As explained in the WPA3 model, the cases that generate attacks (i.e., when nonces maskA (N0) or maskB (N1) can be predicted by an attacker) require two different set of options for Tamarin, hence two different result models.
The Key Freshness lemmas (KF) that are proven are proven using a model where the attacker is unrestricted, so for these lines the only lemmas proven are these two.

The other lemmas are proven by restricting a bit the attacker so Tamarin doesn't exhausts the RAM looking into useless paths. In these models, all lemmas are falsified.
The restriction mentioned is that a function symbol is made unavailable to the attacker, so this doesn't change the protocol or context studied.

The results table masks this difference in the models

#### LoRaWAN

The second "suprising" result are the properties NIA\_D and NIAK that are false in a basic model, but become True in a reuse case (Reuse always 0).

The offending lemmas follow:
```
lemma NIA_D: all-traces
  "∀ deveui joineui appkey devnonce joinnonce #i.
    (DevEnded( deveui, joineui, appkey, devnonce, joinnonce ) @ #i) ⇒
    (((∃ #j.
        (NetEnded( deveui, joineui, appkey, devnonce, joinnonce ) @ #j) ∧
        (#j < #i)) ∨
      (∃ #r. RevLtk( deveui ) @ #r)) ∨
     (∃ #r. RevLtk( joineui ) @ #r))"

lemma NIAK: all-traces
  "∀ deveui joineui appskey nwkskey #i.
    (DevEndedKeys( deveui, joineui, appskey, nwkskey ) @ #i) ⇒
    (((∃ #j.
        (NetEndedKeys( deveui, joineui, appskey, nwkskey ) @ #j) ∧ (#j < #i)) ∨
      (∃ #r. RevLtk( deveui ) @ #r)) ∨
     (∃ #r. RevLtk( joineui ) @ #r))"
```

Here is the LoRaWAN 1.0 protocol:
```
D -> N, <'0', DevEUI, JoinEUI, DevNonce, mac(AppKey, <'0', DevEUI, JoinEUI, DevNonce)>
N -> D, senc(AppKey, <'1', JoinNonce, DevAddr, mac(AppKey, <'1', JoinNonce, DevAddr>)>)
```

Basically, the Device (identified by DevEUI) sends to the network (identified by JoinEUI) a Nonce, and adds a MAC to the message using AppKey, shared between the Device and the network.
The network answers with a nonce JoinNonce, a device address and Mac-then-Encrypt this message using AppKey.
The "Reuse always 0" case that generates this result states that the Device D generates a nonce DevNonce, that is constant for all protocol runs.

Therefore, it is easy to see why the non injective agreement properties are proven:
In this scenario, the first message is completely, and always constant.
In the second message, the network generates a fresh nonce and sends it. 
Therefore, in this scenario, this protocol can be abstracted as:

```
D -> N, cst
N -> D, MtE(AppKey, <'1', JoinNonce, Addr>)
```

In this case, non-injective agreement NIA\_D is always True, because the attacker cannot forge the network's response (injective agreement still fails, though).

The NIAK property is non-injective agreement on keys.
The keys AppSKey and NwkSKey are derived from a kdf function and the nonces exchanged:

```
AppSKey = kdf(<'0', DevNonce, JoinNonce>, AppKey)
NwkSKey = kdf(<'1', DevNonce, JoinNonce>, AppKey)
```

Because DevNonce is always constant in the scenario studied, only the network's nonce is used to provide some sort of randomness to the keys.
If a device has derived a set of keys <AppSKey, NwkSKey>, it means the device has received a JoinNonce value from the network, that could only come from the network because AppKey is unknown to the attacker.
Therefore, non-injective agreement also holds, although again, injective agreement fails.

It makes little sense to study a (very) bad protocol such as LoRaWAN 1.0 OTAA using a powerful attack model such as Reuse always 0, but they have been kept for the sake of the systematic study.

#### Randomized primitives

Nonces in primitives are not named in the protocols or in the paper, so the choice is to call them 'n<number>'.

Some protocols rely on randomized primitives, in which cases vulnerabilities in the primitives wrt nonce misuse have been modeled.
An extensive explanation of the modeling choices and how to run the models is present in the relevant folder `models/randomize_primitives`

For ISO 9798-2-4 and 9798-3-4 there were no problems running the models, so the complete results are provided.

For ISO 9798-2-6, running the models was more expensive as Tamarin is easily lost in the branches.
It was only necessary to cover 4 cases with NR-A2 to provide a correct and complete security analysis, hence the smaller table.

