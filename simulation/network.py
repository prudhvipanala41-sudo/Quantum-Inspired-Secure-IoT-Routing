"""
Builds a networkx graph connecting IoT nodes that are within
communication range of each other, plus the Base Station node.
"""

import numpy as np
import networkx as nx
from scipy.spatial import KDTree


BS_ID = "BS"


def build_network_graph(df, area=200, comm_range=30):
    """
    Build an undirected graph where an edge exists between two nodes
    (or a node and the Base Station) if their Euclidean distance is
    within comm_range.

    Optimized with KDTree for instant O(N log N) graph construction.
    Edge weight = distance (used as routing cost basis).
    """
    G = nx.Graph()

    bs_x, bs_y = area / 2.0, area / 2.0
    G.add_node(BS_ID, x=bs_x, y=bs_y, is_bs=True)

    node_ids = df["node_id"].values.astype(int)
    xs = df["x"].values
    ys = df["y"].values
    energies = df["energy"].values
    trusts = df["trust"].values
    malicious_arr = df["is_malicious"].values if "is_malicious" in df.columns else np.zeros(len(df), dtype=bool)
    ch_arr = df["is_ch"].values if "is_ch" in df.columns else np.zeros(len(df), dtype=bool)
    clusters = df["cluster_id"].values if "cluster_id" in df.columns else np.full(len(df), -1)

    for i in range(len(df)):
        G.add_node(
            int(node_ids[i]),
            x=float(xs[i]),
            y=float(ys[i]),
            energy=float(energies[i]),
            trust=float(trusts[i]),
            is_malicious=bool(malicious_arr[i]),
            is_ch=bool(ch_arr[i]),
            cluster_id=int(clusters[i]),
        )

    coords = np.column_stack([xs, ys])

    # Fast KDTree neighbor queries
    tree = KDTree(coords)
    pairs = tree.query_pairs(r=comm_range)

    for i, j in pairs:
        nid_a, nid_b = int(node_ids[i]), int(node_ids[j])
        d = float(np.hypot(xs[i] - xs[j], ys[i] - ys[j]))
        G.add_edge(nid_a, nid_b, weight=d)

    # Node-to-BS edges (BS has extended transmission/listening radius)
    bs_range = comm_range * 1.8
    dists_to_bs = np.hypot(xs - bs_x, ys - bs_y)
    bs_connect_mask = dists_to_bs <= bs_range

    for i in np.where(bs_connect_mask)[0]:
        G.add_edge(int(node_ids[i]), BS_ID, weight=float(dists_to_bs[i]))

    return G


def ensure_connected(G, df, area=200, comm_range=30, max_extra=120):
    """
    Safety net: if the graph ends up disconnected (isolated nodes),
    progressively widen comm_range until every node can reach BS,
    or give up after max_extra units of extra range.
    """
    extra = 0
    while extra <= max_extra:
        if BS_ID in G:
            reachable = nx.node_connected_component(G, BS_ID)
            if len(reachable) >= len(df) + 1:  # +1 for BS itself
                return G
        extra += 10
        G = build_network_graph(df, area=area, comm_range=comm_range + extra)
    return G


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/nodes.csv")
    G = build_network_graph(df, area=200, comm_range=30)
    G = ensure_connected(G, df, area=200, comm_range=30)
    print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
