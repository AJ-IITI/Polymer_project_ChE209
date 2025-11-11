#!/usr/bin/env python3
import math

BOND_LENGTH = 1.2
BOX_SIZE = 400.0

atoms = []
bonds = []

def add_atom(x, y, z):
    aid = len(atoms) + 1
    atoms.append((aid, 1, 1, float(x), float(y), float(z)))
    return aid

def add_bond(i, j):
    bid = len(bonds) + 1
    bonds.append((bid, 1, int(i), int(j)))

def unit(v):
    x, y, z = v
    r = math.sqrt(x*x + y*y + z*z)
    return (x/r, y/r, z/r) if r > 0 else (0, 0, 0)

def draw_chain(start_id, direction, n):
    ux, uy, uz = unit(direction)
    sx, sy, sz = atoms[start_id-1][3:6]
    prev = start_id
    for step in range(1, n+1):
        nid = add_atom(sx + ux*BOND_LENGTH*step, 
                       sy + uy*BOND_LENGTH*step, 
                       sz + uz*BOND_LENGTH*step)
        add_bond(prev, nid)
        prev = nid
    return prev

def center_atoms():
    cx = sum(a[3] for a in atoms)/len(atoms)
    cy = sum(a[4] for a in atoms)/len(atoms)
    cz = sum(a[5] for a in atoms)/len(atoms)
    for idx, a in enumerate(atoms):
        atoms[idx] = (a[0], a[1], a[2], a[3]-cx, a[4]-cy, a[5]-cz)

def write_lammps(filename="polymer.data"):
    with open(filename, "w") as f:
        f.write(f"# Group 1 dendrimer: 1 core + 3 junctions + 6 terminals\n\n")
        f.write(f"{len(atoms)} atoms\n{len(bonds)} bonds\n\n")
        f.write("1 atom types\n1 bond types\n\n")
        f.write(f"{-BOX_SIZE/2:.1f} {BOX_SIZE/2:.1f} xlo xhi\n")
        f.write(f"{-BOX_SIZE/2:.1f} {BOX_SIZE/2:.1f} ylo yhi\n")
        f.write(f"{-BOX_SIZE/2:.1f} {BOX_SIZE/2:.1f} zlo zhi\n\n")
        f.write("Masses\n\n1 1.0\n\nAtoms # bond\n\n")
        for i, m, t, x, y, z in atoms:
            f.write(f"{i} {m} {t} {x:.6f} {y:.6f} {z:.6f}\n")
        f.write("\nBonds\n\n")
        for k, t, i, j in bonds:
            f.write(f"{k} {t} {i} {j}\n")

def write_topology(filename="topology_edges.txt"):
    with open(filename, "w") as f:
        for k, t, i, j in bonds:
            f.write(f"{i} {j}\n")

# ===== DENDRIMER STRUCTURE =====
print("Building DENDRIMER: 1 core -> 3 junctions -> 6 terminals...")

# CENTRAL CORE at origin
CORE = add_atom(0, 0, 0)
print(f"  CORE: atom {CORE}")

# Define 3 directions from core (120° apart in xy plane)
import math
angles = [90, 210, 330]  # degrees
directions = [(math.cos(math.radians(a)), math.sin(math.radians(a)), 0) for a in angles]

terminals = []
junctions = []

for i, direction in enumerate(directions, 1):
    # Stem from core to junction
    stem_length = 15
    junction = draw_chain(CORE, direction, stem_length)
    junctions.append(junction)
    print(f"  Branch {i}: CORE -> Junction (atom {junction})")
    
    # From junction, create 2 arms (Y-fork)
    # Calculate perpendicular directions for the arms
    dx, dy, dz = direction
    # Arm 1: rotate 45° counterclockwise
    angle1 = math.radians(45)
    arm1_dir = (dx * math.cos(angle1) - dy * math.sin(angle1),
                dx * math.sin(angle1) + dy * math.cos(angle1),
                0)
    
    # Arm 2: rotate 45° clockwise
    angle2 = math.radians(-45)
    arm2_dir = (dx * math.cos(angle2) - dy * math.sin(angle2),
                dx * math.sin(angle2) + dy * math.cos(angle2),
                0)
    
    arm_length = 12
    term1 = draw_chain(junction, arm1_dir, arm_length)
    term2 = draw_chain(junction, arm2_dir, arm_length)
    
    terminals.extend([term1, term2])
    print(f"    Junction {junction} -> Terminals: {term1}, {term2}")

center_atoms()
write_lammps()
write_topology()

# Verify topology
connections = {a[0]: 0 for a in atoms}
for bid, btype, i, j in bonds:
    connections[i] += 1
    connections[j] += 1

core_connections = connections[CORE]
junction_nodes = [j for j in junctions]
terminal_nodes = [t for t in terminals]

print(f"\n✓ Wrote {len(atoms)} atoms, {len(bonds)} bonds")
print(f"  CORE (atom {CORE}): {core_connections} branches")
print(f"  JUNCTIONS: {junction_nodes} (each has 3 bonds)")
print(f"  TERMINALS: {len(terminal_nodes)} ends")

if core_connections == 3 and len(terminal_nodes) == 6:
    print("  ✓ DENDRIMER TOPOLOGY CORRECT!")
else:
    print(f"  ✗ Check topology")
