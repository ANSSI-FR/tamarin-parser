### Models

There are two sets of models and results.
In the folder `nonce_and_keys`, nonces and ephemeral keys are considered to be possibly misgenerated.
In the folder `randomized-primitives`, relevant models have additional modeling to take into account the primitives behavior when nonces are reused.

For models that consider misgeneration of nonces and keys, everything should run without problems, except Dragonfly that may take few GBs of RAM for some cases, and WPA3 that may be a bit heavy also.
It should be possible, using TamarinParser to re-generate all the models and to re-run all of them, for about a few days of processing.
However, for WPA3 some modifications were made **after** the generation of the models with TamarinParser. These modifications allow Tamarin to autoprove the models, whereas by default it simply engulfed into wrong branches and never finished.
The modifications do not impact the results, they are summarized hereinafter:
- For all models that identify no attacks, adding a lemma "secrecy\_pe", tagged as a reuse lemma, that checks the attacker can never know pe helps Tamarin prove the properties. Obviously, this lemma must always be True for the considered models, or the results cannot be trusted.
- For all other models (i.e., when secrecype is False):
    + For the key freshness lemmas, they are proven as is, without restricting the attacker, hence the proof holds for the complete model
    + All the other security lemmas fail and Tamarin identify attacks on them. To prevent Tamarin from investigating incorrect paths where it does not end, the attacker is restricted, namely it cannot access the function symbol `add/2` (labelled private). This doesn't impact the results, because if a security property is false when the attacker is restricted, it is obviously false when there the attacker is not.
- The provided verification script (models/wpa3/run\_all.sh) should work on all WPA3 models, it is loaded with the correct options for each file.

For models that represent randomized primitives, they are longer to process, in particular ISO 9798-2-6 that requires a long time to conclude.
When necessary, additional guidance has been provided to Tamarin (in the form of tactics and restrictions) to enable it to conclude.
Note that additional restrictions have only been used to help Tamarin identify an attack, not to provide a security proof of a modified version of a protocol, so this doesn't affect the correctness of the results.

The models were run on two possible machines:

- Lenovo Thinkpad X13 ; Intel Core i7-10510U CPU (8 cores) ; 16 GB of RAM
- Computing server ; AMD EPYC 7H12 64-Core Processor (256 cores) ; 1 TB of RAM

By default the laptop has been used, except for models that required more than 16GB or RAM or if the processing was too long, in which case the server was used.
Overall, redoing all experiments and models takes about a week.
Processing time is still included in the models, however be reminded that the results may come from two distinct execution environments.
