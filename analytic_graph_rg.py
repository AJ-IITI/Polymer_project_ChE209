#!/usr/bin/env python3
from collections import deque

def read_edges(fname="topology_edges.txt"):
    edges = []
    nodes = set()
    with open(fname) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                i = int(parts[0]); j = int(parts[1])
                edges.append((i,j))
                nodes.add(i); nodes.add(j)
    return sorted(nodes), edges

def build_adj(nodes, edges):
    adj = {n: [] for n in nodes}
    for i,j in edges:
        adj[i].append(j); adj[j].append(i)
    return adj

def bfs(start, nodes, adj):
    dist = {n: None for n in nodes}
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

if __name__ == "__main__":
    nodes, edges = read_edges()
    adj = build_adj(nodes, edges)
    N = len(nodes)
    S = 0
    for i in nodes:
        di = bfs(i, nodes, adj)
        for j in nodes:
            S += di[j]
    Rg2 = S / (2.0 * N * N)
    print("N =", N)
    print("S =", S)
    print("Analytic Rg^2 (b^2=1) =", Rg2)
    print("Analytic Rg =", Rg2**0.5)
