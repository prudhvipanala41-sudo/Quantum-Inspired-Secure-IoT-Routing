"""
Baseline routing: plain Dijkstra shortest path (by distance only).
No awareness of energy, trust, or security -- used as the comparison
baseline against the PSO multi-objective route optimizer.
"""

import networkx as nx


def dijkstra_route(G, source, target="BS"):
    """
    Returns (path, total_distance) using pure distance-weighted
    Dijkstra shortest path. Returns (None, None) if unreachable.
    """
    try:
        path = nx.dijkstra_path(G, source, target, weight="weight")
        length = nx.dijkstra_path_length(G, source, target, weight="weight")
        return path, length
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, None


def k_shortest_paths(G, source, target="BS", k=5):
    """
    Return up to k shortest (by distance) simple paths from source to
    target. Used to build the candidate route set that PSO chooses
    between.
    """
    try:
        gen = nx.shortest_simple_paths(G, source, target, weight="weight")
        paths = []
        for i, path in enumerate(gen):
            if i >= k:
                break
            paths.append(path)
        return paths
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


if __name__ == "__main__":
    import pandas as pd
    from simulation.network import build_network_graph, ensure_connected

    df = pd.read_csv("data/nodes.csv")
    G = build_network_graph(df)
    G = ensure_connected(G, df)

    src = int(df["node_id"].iloc[0])
    path, dist = dijkstra_route(G, src)
    print(f"Dijkstra route from {src} to BS: {path}, distance={dist:.2f}")

    candidates = k_shortest_paths(G, src, k=5)
    print(f"\n{len(candidates)} candidate routes found:")
    for p in candidates:
        print(p)
