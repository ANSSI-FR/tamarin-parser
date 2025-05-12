from create_table import *

### ISO 9798-2-4
caption = "Detailed results for ISO 9798-2-4 - Nonces"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/nonces_and_keys/9798-2-4"
needle = "results"
nonces = {"N0": "$R_B$", "N1": "$R_A$"}
out_file = "table_979824.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-2-6
caption = "Detailed results for ISO 9798-2-6 - Nonces and keys"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/nonces_and_keys/9798-2-6"
needle = "results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$k_{AB}$", "N3": "$R_{A2}$"}
out_file = "table_979826.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-3-4
caption = "Detailed results for ISO 9798-3-4 - Nonces"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/nonces_and_keys/9798-3-4"
needle = "results"
nonces = {"N0": "$R_B$", "N1": "$R_A$"}
out_file = "table_979834.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-4-4
caption = "Detailed results for ISO 9798-4-4 - Nonces"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/nonces_and_keys/9798-4-4"
needle = "results"
nonces = {"N0": "$R_B$", "N1": "$R_A$"}
out_file = "table_979844.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### NSLPK3
caption = "Detailed results for NSLPK3 - Nonces"
lemmas = ["injective_agreeI", "injective_agreeR", "non_injective_agreeI", "non_injective_agreeR"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/nonces_and_keys/NSLPK3"
needle = "results"
nonces = {"N0": "$N_A$", "N1": "$N_B$"}
out_file = "table_nslpk.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### LoRaWAN 1.0 OTAA
caption = "Detailed results for LoRaWAN 1.0 OTAA - Nonces"
lemmas = ["s_inj_agree_simple_device", "s_inj_agree_simple_network", "s_noninj_agree_simple_device", "s_noninj_agree_simple_network", "s_inj_agree_keys", "s_noninj_agree_keys", "weaksecret_device", "weaksecret_network", "keys_freshness_device", "keys_freshness_network"]
lemma_names = ["IA\\_D", "IA\\_N", "NIA\\_D", "NIA\\_N", "IAK", "NIAK", "S\\_D", "S\\_N", "KF\\_D", "KF\\_N"]
folder = "../models/nonces_and_keys/lorawan_10"
needle = "results"
nonces = {"N0": "$DevNonce$", "N1": "$JoinNonce$"}
out_file = "table_lorawan10.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### Bluetooth NC
caption = "Detailed results for Bluetooth Secure Numeric Comparison - Nonces and keys"
lemmas = ["inj_agree_init", "inj_agree_resp", "noninj_agree_init", "noninj_agree_resp", "inj_agree_init_keys", "inj_agree_resp_keys", "noninj_agree_init_keys", "noninj_agree_resp_keys", "key_secrecy_init", "key_secrecy_resp", "key_freshness_init", "key_freshness_resp"]
lemma_names = ["IA\\_I", "IA\\_R", "NIA\\_I", "NIA\\_R", "IAK\\_I", "IAK\\_R", "NIAK\\_I", "NIAK\\_R", "S\\_I", "S\\_R", "KF\\_I", "KF\\_R"]
folder = "../models/nonces_and_keys/bluetooth_nc"
needle = "results"
nonces = {"N0": "$sk_i$", "N1": "$sk_r$", "N2": "$N_r$", "N3": "$N_i$"}
out_file = "table_bluetooth_nc.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### Four-Way Handshake - Static PSK
caption = "Detailed results for Four-Way Handshake - Static PSK - Nonces"
lemmas = ["inj_agree_ap", "inj_agree_client", "noninj_agree_ap", "noninj_agree_client", "keys_inj_agree_ap", "keys_inj_agree_client", "keys_noninj_agree_ap", "keys_noninj_agree_client", "weak_secrecy_ap", "weak_secrecy_Client", "key_freshness_ap", "key_freshness_client"]
lemma_names = ["IA\\_AP", "IA\\_C", "NIA\\_AP", "NIA\\_C", "IAK\\_AP", "IAK\\_C", "NIAK\\_AP", "NIAK\\_C", "S\\_AP", "S\\_C", "KF\\_AP", "KF\\_C"]
folder = "../models/nonces_and_keys/wpa2"
needle = "statickey_results"
nonces = {"N0": "$N_A$", "N1": "$N_S$"}
out_file = "table_wpa2_static.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### Four-Way Handshake - Fresh PSK
caption = "Detailed results for Four-Way Handshake - Fresh PSK - Nonces"
needle = "freshkey_results"
out_file = "table_wpa2_fresh.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### Dragonfly - No Patch
caption = "Detailed results for Dragonfly - no patch - Nonce and keys"
lemmas = ["InjAgreeAP", "InjAgreeClient", "NonInjAgreeAP", "NonInjAgreeClient", "KeysInjAgreeAP", "KeysInjAgreeClient", "KeysNonInjAgreeAP", "KeysNonInjAgreeClient", "WeakSecrecyAP", "WeakSecrecyClient", "KeyFreshnessAP", "KeyFreshnessClient"]
lemma_names = ["IA\\_AP", "IA\\_C", "NIA\\_AP", "NIA\\_C", "IAK\\_AP", "IAK\\_C", "NIAK\\_AP", "NIAK\\_C", "S\\_AP", "S\\_C", "KF\\_AP", "KF\\_C"]
folder = "../models/nonces_and_keys/dragonfly"
needle = "standard_results"
nonces = {"N0": "$sk_C$", "N1": "$m_C$", "N2": "$sk_{AP}$", "N3": "$m_{AP}$"}
out_file = "table_dragonfly_nopatch.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### Dragonfly - Patch reflection attack
caption = "Detailed results for Dragonfly - patch reflection attack - Nonces and keys"
needle = "patchreflection_results"
out_file = "table_dragonfly_patchreflection.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### WPA3
# It requires to merge the results file, this is done here
caption = "Detailed results for WPA3 - Nonces and keys"
lemmas = ["inj_agree_ap", "inj_agree_client", "noninj_agree_ap", "noninj_agree_client", "keys_inj_agree_ap", "keys_inj_agree_client", "keys_noninj_agree_ap", "keys_noninj_agree_client", "weak_secrecy_ap", "weak_secrecy_Client", "key_freshness_ap", "key_freshness_client"]
lemma_names = ["IA\\_AP", "IA\\_C", "NIA\\_AP", "NIA\\_C", "IAK\\_AP", "IAK\\_C", "NIAK\\_AP", "NIAK\\_C", "S\\_AP", "S\\_C", "KF\\_AP", "KF\\_C"]
folder = "../models/nonces_and_keys/wpa3"
needle = "results.spthy"
nonces = {"N0": "$sk_C$", "N1": "$m_C$", "N2": "$sk_{AP}$", "N3": "$m_{AP}$", "N4": "$N_{AP}$", "N5": "$N_C$"}
out_file = "table_wpa3.tex"

results_basic_files = get_cases(folder, needle)
raw_results_basic = get_raw_results(results_basic_files, lemmas)

results_freshness_files = get_cases(folder, "freshness")
raw_results_freshness = get_raw_results(results_freshness_files, lemmas)

results_other_files = get_cases(folder, "other")
raw_results_other = get_raw_results(results_other_files, lemmas)

for name in results_freshness_files:
    o = name.replace("freshness", "other")
    other_res = raw_results_other[o]
    fresh_res = raw_results_freshness[name]
    fresh_res.update(other_res)

raw_results_basic.update(raw_results_freshness)
fp = open(out_file, "w")
fp.write(print_header(30))
fp.write(print_caption(caption))
fp.write(print_table_header(lemma_names))
for r in process_raw_results(raw_results_basic, lemmas, nonces):
    fp.write(r)
    fp.write("\\\\ \\hline\n")

fp.write(print_footer())
fp.close()

### ISO 9798-2-4 - Standard
caption = "Detailed results for ISO 9798-2-4 - Nonces, keys, randomized primitives - Standard"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-4"
needle = "standard_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$n_1$", "N3": "$n_2$"}
out_file = "table_979824_randomized_standard.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### ISO 9798-2-4 - Keyleak
caption = "Detailed results for ISO 9798-2-4 - Nonces, keys, randomized primitives - NR-A1 / Keyleak"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-4"
needle = "keyleak_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$n_1$", "N3": "$n_2$"}
out_file = "table_979824_randomized_keyleak.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=30)

### ISO 9798-2-4 - Messleak
caption = "Detailed results for ISO 9798-2-4 - Nonces, keys, randomized primitives - NR-A2 / Messleak"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-4"
needle = "messleak_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$n_1$", "N3": "$n_2$"}
out_file = "table_979824_randomized_messleak.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-2-6 - Standard
caption = "Detailed results for ISO 9798-2-6 - Nonces, keys, randomized primitives - Standard"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-6"
needle = "standard_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$k_{AB}$", "N3": "$n_1$", "N4": "$n_2$", "N5": "$R_{A2}$", "N6": "$n_3$", "N7": "$n_4$"}
out_file = "table_979826_randomized_standard.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-2-6 - Keyleak
caption = "Detailed results for ISO 9798-2-6 - Nonces, keys, randomized primitives - NR-A1/Keyleak"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-6"
needle = "keyleak_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$k_{AB}$", "N3": "$n_1$", "N4": "$n_2$", "N5": "$R_{A2}$", "N6": "$n_3$", "N7": "$n_4$"}
out_file = "table_979826_randomized_keyleak.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-2-6 - Messleak
caption = "Detailed results for ISO 9798-2-6 - Nonces, keys, randomized primitives - NR-A2/Messleak"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-2-6-messleak"
needle = "agreea"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$k_{AB}$", "N3": "$n_1$", "N4": "$n_2$", "N5": "$R_{A2}$", "N6": "$n_3$", "N7": "$n_4$"}
out_file = "table_979826_randomized_messleak.tex"

results_agreea_files = get_cases(folder, needle)
raw_results_agreea = get_raw_results(results_agreea_files, lemmas)

results_agreeb_files = get_cases(folder, "agreeb")
raw_results_agreeb = get_raw_results(results_agreeb_files, lemmas)

for name in results_agreea_files:
    o = name.replace("agreea", "agreeb")
    a_res = raw_results_agreea[name]
    b_res = raw_results_agreeb[o]
    a_res.update(b_res)

fp = open(out_file, "w")
fp.write(print_header())
fp.write(print_caption(caption))
fp.write(print_table_header(lemma_names))
for r in process_raw_results(raw_results_agreea, lemmas, nonces):
    fp.write(r)
    fp.write("\\\\ \\hline\n")

fp.write(print_footer())
fp.close()

### ISO 9798-3-4 - Standard
caption = "Detailed results for ISO 9798-3-4 - Nonces, keys and randomized primitives - Standard"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-3-4"
needle = "standard_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$n_1$", "N3": "$n_2$"}
out_file = "table_979834_randomized_standard.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)

### ISO 9798-3-4 - NR-S
caption = "Detailed results for ISO 9798-3-4 - Nonces, keys and randomized primitives - NR-S"
lemmas = ["agree_a", "agree_b", "noninj_agree_a", "noninj_agree_b"]
lemma_names = ["IA\\_A", "IA\\_B", "NIA\\_A", "NIA\\_B"]
folder = "../models/randomized_primitives/9798-3-4"
needle = "nrs_results"
nonces = {"N0": "$R_B$", "N1": "$R_A$", "N2": "$n_1$", "N3": "$n_2$"}
out_file = "table_979834_randomized_nrs.tex"

create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces)
