set -x
tamarin-prover wpa3_reuse_once_0_1.spthy --prove 2>/dev/null > wpa3_reuse_once_0_1_results.spthy
tamarin-prover wpa3_reuse_once_0_2.spthy --prove 2>/dev/null > wpa3_reuse_once_0_2_results.spthy
tamarin-prover wpa3_reuse_once_0_3.spthy --prove 2>/dev/null > wpa3_reuse_once_0_3_results.spthy
tamarin-prover wpa3_reuse_once_1_2.spthy --prove 2>/dev/null > wpa3_reuse_once_1_2_results.spthy
tamarin-prover wpa3_reuse_once_2_3.spthy --prove 2>/dev/null > wpa3_reuse_once_2_3_results.spthy
