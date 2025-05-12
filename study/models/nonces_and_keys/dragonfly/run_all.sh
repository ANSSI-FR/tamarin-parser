set -x

echo "No patch"

tamarin-prover --prove dragonfly_basic.spthy 2>/dev/null > dragonfly_basic_standard_results.spthy
tamarin-prover --prove dragonfly_leak_always_0.spthy 2>/dev/null > dragonfly_leak_always_0_standard_results.spthy
tamarin-prover --prove dragonfly_leak_always_1.spthy 2>/dev/null > dragonfly_leak_always_1_standard_results.spthy
tamarin-prover --prove dragonfly_leak_always_2.spthy 2>/dev/null > dragonfly_leak_always_2_standard_results.spthy
tamarin-prover --prove dragonfly_leak_always_3.spthy 2>/dev/null > dragonfly_leak_always_3_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_always_0.spthy 2>/dev/null > dragonfly_reuse_always_0_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_always_1.spthy 2>/dev/null > dragonfly_reuse_always_1_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_always_2.spthy 2>/dev/null > dragonfly_reuse_always_2_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_always_3.spthy 2>/dev/null > dragonfly_reuse_always_3_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_0_0.spthy 2>/dev/null > dragonfly_reuse_once_0_0_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_0_1.spthy 2>/dev/null > dragonfly_reuse_once_0_1_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_0_2.spthy 2>/dev/null > dragonfly_reuse_once_0_2_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_0_3.spthy 2>/dev/null > dragonfly_reuse_once_0_3_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_1_1.spthy 2>/dev/null > dragonfly_reuse_once_1_1_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_1_2.spthy 2>/dev/null > dragonfly_reuse_once_1_2_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_1_3.spthy 2>/dev/null > dragonfly_reuse_once_1_3_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_2_2.spthy 2>/dev/null > dragonfly_reuse_once_2_2_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_2_3.spthy 2>/dev/null > dragonfly_reuse_once_2_3_standard_results.spthy
tamarin-prover --prove dragonfly_reuse_once_3_3.spthy 2>/dev/null > dragonfly_reuse_once_3_3_standard_results.spthy

echo "PatchReflection"

tamarin-prover --prove -DPatchReflection dragonfly_basic.spthy 2>/dev/null > dragonfly_basic_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_leak_always_0.spthy 2>/dev/null > dragonfly_leak_always_0_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_leak_always_1.spthy 2>/dev/null > dragonfly_leak_always_1_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_leak_always_2.spthy 2>/dev/null > dragonfly_leak_always_2_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_leak_always_3.spthy 2>/dev/null > dragonfly_leak_always_3_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_always_0.spthy 2>/dev/null > dragonfly_reuse_always_0_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_always_1.spthy 2>/dev/null > dragonfly_reuse_always_1_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_always_2.spthy 2>/dev/null > dragonfly_reuse_always_2_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_always_3.spthy 2>/dev/null > dragonfly_reuse_always_3_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_0_0.spthy 2>/dev/null > dragonfly_reuse_once_0_0_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_0_1.spthy 2>/dev/null > dragonfly_reuse_once_0_1_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_0_2.spthy 2>/dev/null > dragonfly_reuse_once_0_2_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_0_3.spthy 2>/dev/null > dragonfly_reuse_once_0_3_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_1_1.spthy 2>/dev/null > dragonfly_reuse_once_1_1_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_1_2.spthy 2>/dev/null > dragonfly_reuse_once_1_2_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_1_3.spthy 2>/dev/null > dragonfly_reuse_once_1_3_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_2_2.spthy 2>/dev/null > dragonfly_reuse_once_2_2_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_2_3.spthy 2>/dev/null > dragonfly_reuse_once_2_3_patchreflection_results.spthy
tamarin-prover --prove -DPatchReflection dragonfly_reuse_once_3_3.spthy 2>/dev/null > dragonfly_reuse_once_3_3_patchreflection_results.spthy
