echo "=============== Leak Once 0"
tamarin-prover -DFreshness --prove wpa3_stef_leak_once_0.spthy 2>&1 | grep "\(time:\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_leak_once_0.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Once 1"
tamarin-prover -DFreshness --prove wpa3_stef_leak_once_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_leak_once_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Always 0"
tamarin-prover -DFreshness --prove wpa3_stef_leak_always_0.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --prove wpa3_stef_leak_always_0.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Always 1"
tamarin-prover -DFreshness --prove wpa3_stef_leak_always_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_leak_always_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 0 = 2"
tamarin-prover -DFreshness --prove wpa3_stef_reuse_once_0_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_reuse_once_0_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 0 = 3"
tamarin-prover -DFreshness --prove wpa3_stef_reuse_once_0_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_reuse_once_0_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 1 = 2"
tamarin-prover -DFreshness --prove wpa3_stef_reuse_once_1_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_reuse_once_1_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 1 = 3"
tamarin-prover -DFreshness --prove wpa3_stef_reuse_once_1_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"
tamarin-prover -DAddPrivate --stop-on-trace=seqdfs --prove wpa3_stef_reuse_once_1_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "======================FINISHED COMPLICATED MODELS================================"

echo "=============== Basic"
tamarin-prover --prove wpa3_stef_basic.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Always 2"
tamarin-prover --prove wpa3_stef_leak_always_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Always 3"
tamarin-prover --prove wpa3_stef_leak_always_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Once 2"
tamarin-prover --prove wpa3_stef_leak_once_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Leak Once 3"
tamarin-prover --prove wpa3_stef_leak_once_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Always 0"
tamarin-prover --prove wpa3_stef_reuse_always_0.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Always 1"
tamarin-prover --prove wpa3_stef_reuse_always_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Always 2"
tamarin-prover --prove wpa3_stef_reuse_always_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Always 3"
tamarin-prover --prove wpa3_stef_reuse_always_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 0 = 0"
tamarin-prover --prove wpa3_stef_reuse_once_0_0.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 0 = 1"
tamarin-prover --prove wpa3_stef_reuse_once_0_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 1 = 1"
tamarin-prover --prove wpa3_stef_reuse_once_1_1.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 2 = 2"
tamarin-prover --prove wpa3_stef_reuse_once_2_2.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 2 = 3"
tamarin-prover --prove wpa3_stef_reuse_once_2_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

echo "=============== Reuse Once 3 = 3"
tamarin-prover --prove wpa3_stef_reuse_once_3_3.spthy 2>&1 | grep "\(time\|(\(all\|exists\)-trace\)"

