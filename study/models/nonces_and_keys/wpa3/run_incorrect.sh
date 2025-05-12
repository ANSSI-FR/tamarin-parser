set -x

echo "=============== Leak Once 0"
tamarin-prover -DFreshness wpa3_leak_always_0.spthy --prove 2>/dev/null > wpa3_leak_always_0_results_freshness.spthy
#tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_leak_always_0.spthy --prove 2>/dev/null > wpa3_leak_always_0_results_other.spthy

echo "=============== Leak Once 1"
tamarin-prover -DFreshness wpa3_leak_always_1.spthy --prove 2>/dev/null > wpa3_leak_always_1_results_freshness.spthy
#tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_leak_always_1.spthy --prove 2>/dev/null > wpa3_leak_always_1_results_other.spthy

echo "=============== Leak Once 2"
tamarin-prover -DFreshness wpa3_leak_always_2.spthy --prove 2>/dev/null > wpa3_leak_always_2_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_leak_always_2.spthy --prove 2>/dev/null > wpa3_leak_always_2_results_other.spthy

echo "=============== Leak Once 3"
tamarin-prover -DFreshness wpa3_leak_always_3.spthy --prove 2>/dev/null > wpa3_leak_always_3_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_leak_always_3.spthy --prove 2>/dev/null > wpa3_leak_always_3_results_other.spthy

echo "=============== Reuse Once 0 = 4"
tamarin-prover -DFreshness wpa3_reuse_once_0_4.spthy --prove 2>/dev/null > wpa3_reuse_once_0_4_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_0_4.spthy --prove 2>/dev/null > wpa3_reuse_once_0_4_results_other.spthy

echo "=============== Reuse Once 0 = 5"
tamarin-prover -DFreshness wpa3_reuse_once_0_5.spthy --prove 2>/dev/null > wpa3_reuse_once_0_5_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_0_5.spthy --prove 2>/dev/null > wpa3_reuse_once_0_5_results_other.spthy

echo "=============== Reuse Once 1 = 4"
tamarin-prover -DFreshness wpa3_reuse_once_1_4.spthy --prove 2>/dev/null > wpa3_reuse_once_1_4_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_1_4.spthy --prove 2>/dev/null > wpa3_reuse_once_1_4_results_other.spthy

echo "=============== Reuse Once 1 = 5"
tamarin-prover -DFreshness wpa3_reuse_once_1_5.spthy --prove 2>/dev/null > wpa3_reuse_once_1_5_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_1_5.spthy --prove 2>/dev/null > wpa3_reuse_once_1_5_results_other.spthy

echo "=============== Reuse Once 2 = 4"
tamarin-prover -DFreshness wpa3_reuse_once_2_4.spthy --prove 2>/dev/null > wpa3_reuse_once_2_4_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_2_4.spthy --prove 2>/dev/null > wpa3_reuse_once_2_4_results_other.spthy

echo "=============== Reuse Once 2 = 5"
tamarin-prover -DFreshness wpa3_reuse_once_2_5.spthy --prove 2>/dev/null > wpa3_reuse_once_2_5_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_2_5.spthy --prove 2>/dev/null > wpa3_reuse_once_2_5_results_other.spthy

echo "=============== Reuse Once 3 = 4"
tamarin-prover -DFreshness wpa3_reuse_once_3_4.spthy --prove 2>/dev/null > wpa3_reuse_once_3_4_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_3_4.spthy --prove 2>/dev/null > wpa3_reuse_once_3_4_results_other.spthy

echo "=============== Reuse Once 3 = 5"
tamarin-prover -DFreshness wpa3_reuse_once_3_5.spthy --prove 2>/dev/null > wpa3_reuse_once_3_5_results_freshness.spthy
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs wpa3_reuse_once_3_5.spthy --prove 2>/dev/null > wpa3_reuse_once_3_5_results_other.spthy
