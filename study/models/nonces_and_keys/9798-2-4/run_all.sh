set -x

tamarin-prover --prove --auto-sources 979824_basic.spthy 2>/dev/null > 979824_basic_results.spthy
tamarin-prover --prove --auto-sources 979824_leak_always_0.spthy 2>/dev/null > 979824_leak_always_0_results.spthy
tamarin-prover --prove --auto-sources 979824_leak_always_1.spthy 2>/dev/null > 979824_leak_always_1_results.spthy
tamarin-prover --prove --auto-sources 979824_reuse_always_0.spthy 2>/dev/null > 979824_reuse_always_0_results.spthy
tamarin-prover --prove --auto-sources 979824_reuse_always_1.spthy 2>/dev/null > 979824_reuse_always_1_results.spthy
tamarin-prover --prove --auto-sources 979824_reuse_once_0_0.spthy 2>/dev/null > 979824_reuse_once_0_0_results.spthy
tamarin-prover --prove --auto-sources 979824_reuse_once_0_1.spthy 2>/dev/null > 979824_reuse_once_0_1_results.spthy
tamarin-prover --prove --auto-sources 979824_reuse_once_1_1.spthy 2>/dev/null > 979824_reuse_once_1_1_results.spthy
