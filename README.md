# Polymer_project_ChE209

# 🧪 Group 1 — Dendrimer Radius of Gyration (RG) Analysis

This repository contains the full solution for Group 1’s dendrimer: structure generation, LAMMPS simulation, analytical derivation via Cantarella’s graph method, and the contraction factor g under both the assignment normalization (Group 1 as reference) and the path‑graph normalization from the paper.

---

## 👥 Group 1 Members

- Abhishek Nigam
- Aditya Dave
- Ananthula Shashivardhan
- Anshuman Jha
- Anushka Jain

---

## 📦 Features

- Deterministic generator for the dendrimer topology (118‑bead MD model + 10‑node graph).
- One‑command cluster run script for LAMMPS.
- Post‑processing for numerical Rg and Rg² from the trajectory.
- Analytical Rg² via two equivalent graph‑theory routes:
  - Shortest‑path sum S(G) (Definition 18)
  - Laplacian pseudoinverse trace tr(L⁺) (via Kirchhoff index)
- Contraction factor g reported in both normalizations.

---

## 🧬 Dendrimer Topology (Graph)

- Vertices (V) = 10, Edges (E) = 9 (tree)
- Edge list (0‑based labels):  
  (0,1), (0,2), (0,3), (1,4), (1,5), (2,6), (2,7), (3,8), (3,9)

Interpretation: 0 = core, 1–3 = junctions, 4–9 = terminals.


---

## 📁 Repository Layout

.
├─ README.md
├─ generate_group1_tree.py      # builds 118‑atom LAMMPS data + topology_edges.txt
├─ polymer.data                 # LAMMPS data (generated/overwritten)
├─ in.group1                    # LAMMPS input script
├─ run_group1_test.sh           # one‑click run on cluster
├─ compute_rg_from_dump.py      # numerical Rg/Rg² from trajectory
├─ analytic_graph_rg.py         # Rg² via graph theory from topology_edges.txt
├─ topology_edges.txt           # 10‑node edge list (graph)
└─ RESULTS_SUMMARY.txt          # consolidated outputs

---

## 🛠️ Requirements

# Python (install NumPy)
pip install numpy

# LAMMPS — ensure the executable is available on PATH.
# On most clusters the command is either `lmp` or `lmp_mpi`.
# You should be able to run one of the following without error:
lmp -h        # or:
lmp_mpi -h

# If neither works, load your site’s LAMMPS module (example):
# module load lammps

# Optional: verify MPI is available (for parallel runs)
mpirun --version   # or: mpiexec --version

---

## 🚀 Quickstart (Reproduce End‑to‑End)

# 1) Generate structure and topology
python3 generate_group1_tree.py

# 2) Run LAMMPS
chmod +x run_group1_test.sh
./run_group1_test.sh
# or (manual MPI):
mpirun -np 4 lmp -in in.group1

# 3) Numerical Rg from trajectory
python3 compute_rg_from_dump.py

# 4) Analytical (graph‑theory) Rg²
python3 analytic_graph_rg.py


---

## 🔬 Methods

### A) Graph‑Theory Rg² (Cantarella)

- Shortest‑path definition (Definition 18):  
  Compute all‑pairs shortest‑path distances n_ij on the 10‑node tree.  
  Sum S(G) = Σ_i Σ_j n_ij = 234. With V = 10:

- Rg² = S(G) / (2 V²) = 234 / (2 × 10²) = 234 / 200 = 1.17
  Rg = sqrt(1.17) ≈ 1.08

- Equivalent Laplacian pseudoinverse route:  
  Kirchhoff index Kf(G) = Σ_{i<j} n_ij = S/2 = 117.  
  For connected graphs, Kf(G) = V · tr(L⁺) ⇒ tr(L⁺) = 117 / 10 = 11.7.  
  Then: E[Rg²; G] = (1/V) · tr(L⁺) = 11.7 / 10 = 1.17


### B) Molecular Dynamics (LAMMPS)

- Model: 118‑bead coarse‑grained chain network mirroring the 10‑node connectivity.
- Thermostat: NVT at T = 1.0 (reduced), timestep 0.005.
- Duration: 100k steps; dump every 2000 steps.
- Post‑processing: Rg² = (1/N) Σ_i |r_i − r_cm|²

---

## 📊 Final Results (Cite These)

- Sum of graph distances: S(G) = 234
- Analytical (graph, V = 10):
- Rg² = 1.17
- Rg  ≈ 1.08
- Numerical (MD, 118 beads):
- Rg² ≈ 42.06
- Rg  ≈ 6.49

---

## 📏 Contraction Factor g

- Assignment normalization (Group 1 is the reference):
- g_group1 = Rg²(Group 1) / Rg²(Group 1) = 1.17 / 1.17 = 1.00
- Path‑graph normalization (paper’s linear reference with V = 10):
  Rg²(path_10) = (V/6) · ((V+1)/(V−1)) = (10/6) · (11/9) = 55/27 ≈ 2.0370
  g_path-ref = Rg²(dendrimer) / Rg²(path_10) = 1.17 / (55/27) = 3159/5500 ≈ 0.57436

## 📄 License

Academic coursework submission (ChE 209, Fall 2025).


