#!/usr/bin/env python3
import sys
import numpy as np

def read_dump(fname):
    frames = []
    with open(fname,'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.strip().startswith("ITEM: TIMESTEP"):
                step = int(f.readline().strip())
                while True:
                    h = f.readline()
                    if h.strip().startswith("ITEM: NUMBER OF ATOMS"):
                        n_atoms = int(f.readline().strip())
                        break
                while True:
                    h = f.readline()
                    if h.strip().startswith("ITEM: ATOMS"):
                        headers = h.strip().split()[2:]
                        break
                coords = []
                for _ in range(n_atoms):
                    parts = f.readline().split()
                    vals = list(map(float, parts))
                    x,y,z = vals[-3], vals[-2], vals[-1]
                    coords.append((x,y,z))
                frames.append((step, np.array(coords)))
    return frames

def rg2_of_frame(pos):
    com = pos.mean(axis=0)
    return np.mean(np.sum((pos - com)**2, axis=1))

if __name__ == "__main__":
    dump = sys.argv[1] if len(sys.argv) > 1 else "group1_traj.lammpsdump"
    out = sys.argv[2] if len(sys.argv) > 2 else "rg_time.dat"
    frames = read_dump(dump)
    with open(out, "w") as fo:
        fo.write("#frame rg2\n")
        for i, (step, pos) in enumerate(frames):
            fo.write(f"{i} {rg2_of_frame(pos):.8e}\n")
    print(f"Wrote {out} with {len(frames)} frames")
