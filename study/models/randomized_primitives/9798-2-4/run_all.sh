set -x
tamarin-prover 979824_basic.spthy --prove --auto-sources 2>/dev/null > 979824_basic_standard_results.spthy
tamarin-prover 979824_leak_always_0.spthy --prove --auto-sources 2>/dev/null > 979824_leak_always_0_standard_results.spthy
tamarin-prover 979824_leak_always_1.spthy --prove --auto-sources 2>/dev/null > 979824_leak_always_1_standard_results.spthy
tamarin-prover 979824_leak_always_2.spthy --prove --auto-sources 2>/dev/null > 979824_leak_always_2_standard_results.spthy
tamarin-prover 979824_leak_always_3.spthy --prove --auto-sources 2>/dev/null > 979824_leak_always_3_standard_results.spthy
tamarin-prover 979824_leak_once_0.spthy --prove --auto-sources 2>/dev/null > 979824_leak_once_0_standard_results.spthy
tamarin-prover 979824_leak_once_1.spthy --prove --auto-sources 2>/dev/null > 979824_leak_once_1_standard_results.spthy
tamarin-prover 979824_leak_once_2.spthy --prove --auto-sources 2>/dev/null > 979824_leak_once_2_standard_results.spthy
tamarin-prover 979824_leak_once_3.spthy --prove --auto-sources 2>/dev/null > 979824_leak_once_3_standard_results.spthy
tamarin-prover 979824_reuse_always_0.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_always_0_standard_results.spthy
tamarin-prover 979824_reuse_always_1.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_always_1_standard_results.spthy
tamarin-prover 979824_reuse_always_2.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_always_2_standard_results.spthy
tamarin-prover 979824_reuse_always_3.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_always_3_standard_results.spthy
tamarin-prover 979824_reuse_once_0_0.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_0_0_standard_results.spthy
tamarin-prover 979824_reuse_once_0_1.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_0_1_standard_results.spthy
tamarin-prover 979824_reuse_once_0_2.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_0_2_standard_results.spthy
tamarin-prover 979824_reuse_once_0_3.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_0_3_standard_results.spthy
tamarin-prover 979824_reuse_once_1_1.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_1_1_standard_results.spthy
tamarin-prover 979824_reuse_once_1_2.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_1_2_standard_results.spthy
tamarin-prover 979824_reuse_once_1_3.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_1_3_standard_results.spthy
tamarin-prover 979824_reuse_once_2_2.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_2_2_standard_results.spthy
tamarin-prover 979824_reuse_once_2_3.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_2_3_standard_results.spthy
tamarin-prover 979824_reuse_once_3_3.spthy --prove --auto-sources 2>/dev/null > 979824_reuse_once_3_3_standard_results.spthy

tamarin-prover 979824_basic.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_basic_keyleak_results.spthy
tamarin-prover 979824_leak_always_0.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_always_0_keyleak_results.spthy
tamarin-prover 979824_leak_always_1.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_always_1_keyleak_results.spthy
tamarin-prover 979824_leak_always_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_always_2_keyleak_results.spthy
tamarin-prover 979824_leak_always_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_always_3_keyleak_results.spthy
tamarin-prover 979824_leak_once_0.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_once_0_keyleak_results.spthy
tamarin-prover 979824_leak_once_1.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_once_1_keyleak_results.spthy
tamarin-prover 979824_leak_once_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_once_2_keyleak_results.spthy
tamarin-prover 979824_leak_once_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_leak_once_3_keyleak_results.spthy
tamarin-prover 979824_reuse_always_0.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_always_0_keyleak_results.spthy
tamarin-prover 979824_reuse_always_1.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_always_1_keyleak_results.spthy
tamarin-prover 979824_reuse_always_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_always_2_keyleak_results.spthy
tamarin-prover 979824_reuse_always_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_always_3_keyleak_results.spthy
tamarin-prover 979824_reuse_once_0_0.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_0_0_keyleak_results.spthy
tamarin-prover 979824_reuse_once_0_1.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_0_1_keyleak_results.spthy
tamarin-prover 979824_reuse_once_0_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_0_2_keyleak_results.spthy
tamarin-prover 979824_reuse_once_0_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_0_3_keyleak_results.spthy
tamarin-prover 979824_reuse_once_1_1.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_1_1_keyleak_results.spthy
tamarin-prover 979824_reuse_once_1_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_1_2_keyleak_results.spthy
tamarin-prover 979824_reuse_once_1_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_1_3_keyleak_results.spthy
tamarin-prover 979824_reuse_once_2_2.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_2_2_keyleak_results.spthy
tamarin-prover 979824_reuse_once_2_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_2_3_keyleak_results.spthy
tamarin-prover 979824_reuse_once_3_3.spthy --prove -Dn_reuse_keyleak --auto-sources 2>/dev/null > 979824_reuse_once_3_3_keyleak_results.spthy

tamarin-prover 979824_basic.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_basic_messleak_results.spthy
tamarin-prover 979824_leak_always_0.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_always_0_messleak_results.spthy
tamarin-prover 979824_leak_always_1.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_always_1_messleak_results.spthy
tamarin-prover 979824_leak_always_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_always_2_messleak_results.spthy
tamarin-prover 979824_leak_always_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_always_3_messleak_results.spthy
tamarin-prover 979824_leak_once_0.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_once_0_messleak_results.spthy
tamarin-prover 979824_leak_once_1.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_once_1_messleak_results.spthy
tamarin-prover 979824_leak_once_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_once_2_messleak_results.spthy
tamarin-prover 979824_leak_once_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_leak_once_3_messleak_results.spthy
tamarin-prover 979824_reuse_always_0.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_always_0_messleak_results.spthy
tamarin-prover 979824_reuse_always_1.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_always_1_messleak_results.spthy
tamarin-prover 979824_reuse_always_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_always_2_messleak_results.spthy
tamarin-prover 979824_reuse_always_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_always_3_messleak_results.spthy
tamarin-prover 979824_reuse_once_0_0.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_0_0_messleak_results.spthy
tamarin-prover 979824_reuse_once_0_1.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_0_1_messleak_results.spthy
tamarin-prover 979824_reuse_once_0_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_0_2_messleak_results.spthy
tamarin-prover 979824_reuse_once_0_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_0_3_messleak_results.spthy
tamarin-prover 979824_reuse_once_1_1.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_1_1_messleak_results.spthy
tamarin-prover 979824_reuse_once_1_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_1_2_messleak_results.spthy
tamarin-prover 979824_reuse_once_1_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_1_3_messleak_results.spthy
tamarin-prover 979824_reuse_once_2_2.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_2_2_messleak_results.spthy
tamarin-prover 979824_reuse_once_2_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_2_3_messleak_results.spthy
tamarin-prover 979824_reuse_once_3_3.spthy --prove -Dn_reuse_messleak --auto-sources 2>/dev/null > 979824_reuse_once_3_3_messleak_results.spthy
