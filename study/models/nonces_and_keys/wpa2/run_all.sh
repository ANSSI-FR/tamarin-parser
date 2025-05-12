set -x

echo "StaticKey"

tamarin-prover --prove wpa2_basic.spthy 2>/dev/null > wpa2_basic_statickey_results.spthy
tamarin-prover --prove wpa2_leak_always_0.spthy 2>/dev/null > wpa2_leak_always_0_statickey_results.spthy
tamarin-prover --prove wpa2_leak_always_1.spthy 2>/dev/null > wpa2_leak_always_1_statickey_results.spthy
tamarin-prover --prove wpa2_reuse_always_0.spthy 2>/dev/null > wpa2_reuse_always_0_statickey_results.spthy
tamarin-prover --prove wpa2_reuse_always_1.spthy 2>/dev/null > wpa2_reuse_always_1_statickey_results.spthy
tamarin-prover --prove wpa2_reuse_once_0_0.spthy 2>/dev/null > wpa2_reuse_once_0_0_statickey_results.spthy
tamarin-prover --prove wpa2_reuse_once_0_1.spthy 2>/dev/null > wpa2_reuse_once_0_1_statickey_results.spthy
tamarin-prover --prove wpa2_reuse_once_1_1.spthy 2>/dev/null > wpa2_reuse_once_1_1_statickey_results.spthy

echo "FreshKey"

tamarin-prover --prove -DFreshKey wpa2_basic.spthy 2>/dev/null > wpa2_basic_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_leak_always_0.spthy 2>/dev/null > wpa2_leak_always_0_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_leak_always_1.spthy 2>/dev/null > wpa2_leak_always_1_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_reuse_always_0.spthy 2>/dev/null > wpa2_reuse_always_0_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_reuse_always_1.spthy 2>/dev/null > wpa2_reuse_always_1_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_reuse_once_0_0.spthy 2>/dev/null > wpa2_reuse_once_0_0_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_reuse_once_0_1.spthy 2>/dev/null > wpa2_reuse_once_0_1_freshkey_results.spthy
tamarin-prover --prove -DFreshKey wpa2_reuse_once_1_1.spthy 2>/dev/null > wpa2_reuse_once_1_1_freshkey_results.spthy
