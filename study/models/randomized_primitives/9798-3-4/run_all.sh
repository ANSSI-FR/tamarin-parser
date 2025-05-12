set -x

tamarin-prover 979834_basic.spthy --prove 2>/dev/null > 979834_basic_standard_results.spthy
tamarin-prover 979834_leak_always_0.spthy --prove 2>/dev/null > 979834_leak_always_0_standard_results.spthy
tamarin-prover 979834_leak_always_1.spthy --prove 2>/dev/null > 979834_leak_always_1_standard_results.spthy
tamarin-prover 979834_leak_always_2.spthy --prove 2>/dev/null > 979834_leak_always_2_standard_results.spthy
tamarin-prover 979834_leak_always_3.spthy --prove 2>/dev/null > 979834_leak_always_3_standard_results.spthy
tamarin-prover 979834_reuse_always_0.spthy --prove 2>/dev/null > 979834_reuse_always_0_standard_results.spthy
tamarin-prover 979834_reuse_always_1.spthy --prove 2>/dev/null > 979834_reuse_always_1_standard_results.spthy
tamarin-prover 979834_reuse_always_2.spthy --prove 2>/dev/null > 979834_reuse_always_2_standard_results.spthy
tamarin-prover 979834_reuse_always_3.spthy --prove 2>/dev/null > 979834_reuse_always_3_standard_results.spthy
tamarin-prover 979834_reuse_once_0_0.spthy --prove 2>/dev/null > 979834_reuse_once_0_0_standard_results.spthy
tamarin-prover 979834_reuse_once_0_1.spthy --prove 2>/dev/null > 979834_reuse_once_0_1_standard_results.spthy
tamarin-prover 979834_reuse_once_0_2.spthy --prove 2>/dev/null > 979834_reuse_once_0_2_standard_results.spthy
tamarin-prover 979834_reuse_once_0_3.spthy --prove 2>/dev/null > 979834_reuse_once_0_3_standard_results.spthy
tamarin-prover 979834_reuse_once_1_1.spthy --prove 2>/dev/null > 979834_reuse_once_1_1_standard_results.spthy
tamarin-prover 979834_reuse_once_1_2.spthy --prove 2>/dev/null > 979834_reuse_once_1_2_standard_results.spthy
tamarin-prover 979834_reuse_once_1_3.spthy --prove 2>/dev/null > 979834_reuse_once_1_3_standard_results.spthy
tamarin-prover 979834_reuse_once_2_2.spthy --prove 2>/dev/null > 979834_reuse_once_2_2_standard_results.spthy
tamarin-prover 979834_reuse_once_2_3.spthy --prove 2>/dev/null > 979834_reuse_once_2_3_standard_results.spthy
tamarin-prover 979834_reuse_once_3_3.spthy --prove 2>/dev/null > 979834_reuse_once_3_3_standard_results.spthy

tamarin-prover 979834_basic.spthy -Dnmisuse --prove 2>/dev/null > 979834_basic_nrs_results.spthy
tamarin-prover 979834_leak_always_0.spthy -Dnmisuse --prove 2>/dev/null > 979834_leak_always_0_nrs_results.spthy
tamarin-prover 979834_leak_always_1.spthy -Dnmisuse --prove 2>/dev/null > 979834_leak_always_1_nrs_results.spthy
tamarin-prover 979834_leak_always_2.spthy -Dnmisuse --prove 2>/dev/null > 979834_leak_always_2_nrs_results.spthy
tamarin-prover 979834_leak_always_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_leak_always_3_nrs_results.spthy
tamarin-prover 979834_reuse_always_0.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_always_0_nrs_results.spthy
tamarin-prover 979834_reuse_always_1.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_always_1_nrs_results.spthy
tamarin-prover 979834_reuse_always_2.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_always_2_nrs_results.spthy
tamarin-prover 979834_reuse_always_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_always_3_nrs_results.spthy
tamarin-prover 979834_reuse_once_0_0.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_0_0_nrs_results.spthy
tamarin-prover 979834_reuse_once_0_1.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_0_1_nrs_results.spthy
tamarin-prover 979834_reuse_once_0_2.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_0_2_nrs_results.spthy
tamarin-prover 979834_reuse_once_0_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_0_3_nrs_results.spthy
tamarin-prover 979834_reuse_once_1_1.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_1_1_nrs_results.spthy
tamarin-prover 979834_reuse_once_1_2.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_1_2_nrs_results.spthy
tamarin-prover 979834_reuse_once_1_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_1_3_nrs_results.spthy
tamarin-prover 979834_reuse_once_2_2.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_2_2_nrs_results.spthy
tamarin-prover 979834_reuse_once_2_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_2_3_nrs_results.spthy
tamarin-prover 979834_reuse_once_3_3.spthy -Dnmisuse --prove 2>/dev/null > 979834_reuse_once_3_3_nrs_results.spthy
