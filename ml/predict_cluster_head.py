"""
Applies the trained Random Forest model to real simulated nodes to
select the best cluster head per cluster (AI-based selection --
this is the "proposed method" as opposed to the LEACH baseline).
"""

import joblib
import numpy as np
import pandas as pd

FEATURES = ["energy", "distance", "trust", "packet_delivery", "neighbors"]


def _prepare_features(df, G=None):
    """
    Build the feature columns the model expects from the live node
    DataFrame. 'distance' = distance_to_bs, 'packet_delivery' is
    approximated from trust if not separately simulated yet,
    'neighbors' is degree in the network graph if available.
    """
    df = df.copy()

    if "distance_to_bs" not in df.columns:
        raise ValueError("df must include 'distance_to_bs' (run distance_to_bs() first)")

    df["distance"] = df["distance_to_bs"]

    if "packet_delivery" not in df.columns:
        # Approximate delivery ratio from trust when not separately tracked
        df["packet_delivery"] = df["trust"].clip(0, 1)

    if G is not None:
        df["neighbors"] = df["node_id"].apply(
            lambda nid: G.degree[nid] if nid in G else 1
        )
    elif "neighbors" not in df.columns:
        df["neighbors"] = 5  # neutral default

    return df


def select_cluster_heads_ml(df, model_path="models/cluster_head_model.pkl", G=None):
    """
    Predict CH-suitability probability for every node, then pick the
    highest-probability node within each cluster as its cluster head.

    Returns a copy of df with updated 'is_ch' column and a
    'ch_probability' column for inspection/debugging.
    """
    model = joblib.load(model_path)

    df = _prepare_features(df, G=G)
    X = df[FEATURES]

    probs = model.predict_proba(X)[:, 1]  # probability of class "1" = suitable CH
    df["ch_probability"] = probs
    df["is_ch"] = False

    for cid in sorted(df["cluster_id"].unique()):
        cluster_idx = df[df["cluster_id"] == cid].index
        if len(cluster_idx) == 0:
            continue
        best_idx = df.loc[cluster_idx, "ch_probability"].idxmax()
        df.loc[best_idx, "is_ch"] = True

    return df


if __name__ == "__main__":
    from simulation.node_generator import generate_nodes, distance_to_bs
    from simulation.clustering import cluster_nodes

    nodes = generate_nodes(n=50, area=100, seed=42)
    nodes = distance_to_bs(nodes)
    nodes, _ = cluster_nodes(nodes, n_clusters=5)

    nodes = select_cluster_heads_ml(nodes)
    print(nodes[nodes["is_ch"]][["node_id", "cluster_id", "energy", "trust", "ch_probability"]])
