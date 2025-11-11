#!/bin/bash
set -e
cd "$(dirname "$0")"

module load lammps-openmpi >/dev/null 2>&1 || true

for b in lmp lmp_mpi lmp_serial lammps; do
  command -v "$b" >/dev/null 2>&1 && LMP=$b && break
done

if [ -z "$LMP" ]; then
  echo "No LAMMPS binary found"
  exit 1
fi

echo "[TEST] Generate polymer.data"
python3 generate_group1_tree.py

echo "[TEST] Run LAMMPS"
$LMP -in in.group1 | tee lammps_test.out

echo "[TEST] Postprocessing"
python3 compute_rg_from_dump.py group1_traj.lammpsdump rg_time_test.dat
python3 analytic_graph_rg.py > analytic_results.txt

echo "Test finished!"
