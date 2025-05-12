set -x
tamarin-prover --prove lorawan_10_basic.spthy 2>/dev/null > lorawan_10_basic_results.spthy
tamarin-prover --prove lorawan_10_leak_always_0.spthy 2>/dev/null > lorawan_10_leak_always_0_results.spthy
tamarin-prover --prove lorawan_10_leak_always_1.spthy 2>/dev/null > lorawan_10_leak_always_1_results.spthy
tamarin-prover --prove lorawan_10_reuse_always_0.spthy 2>/dev/null > lorawan_10_reuse_always_0_results.spthy
tamarin-prover --prove lorawan_10_reuse_always_1.spthy 2>/dev/null > lorawan_10_reuse_always_1_results.spthy
tamarin-prover --prove lorawan_10_reuse_once_0_0.spthy 2>/dev/null > lorawan_10_reuse_once_0_0_results.spthy
tamarin-prover --prove lorawan_10_reuse_once_0_1.spthy 2>/dev/null > lorawan_10_reuse_once_0_1_results.spthy
tamarin-prover --prove lorawan_10_reuse_once_1_1.spthy 2>/dev/null > lorawan_10_reuse_once_1_1_results.spthy
