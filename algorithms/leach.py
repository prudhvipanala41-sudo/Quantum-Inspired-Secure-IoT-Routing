"""
Baseline LEACH-style cluster head selection.
Classic LEACH picks cluster heads semi-randomly (weighted lightly by
energy). We use this as the "traditional" baseline to compare our
AI-based (Random Forest) cluster-head selection against.
"""

import numpy as np


def select_cluster_heads_leach(df, seed=42):
    """
    For each cluster, pick one cluster head using a probability
    weighted by remaining energy (closer to classic LEACH than pure
    random selection, but with no AI / no trust / no multi-factor
    scoring).

    Returns a copy of df with an updated 'is_ch' boolean column.
    """
    rng = np.random.default_rng(seed)
    df = df.copy()
    df["is_ch"] = False

    for cid in sorted(df["cluster_id"].unique()):
        cluster_nodes = df[df["cluster_id"] == cid]
        if cluster_nodes.empty:
            continue

        weights = cluster_nodes["energy"].values
        weights = weights / weights.sum()

        chosen_idx = rng.choice(cluster_nodes.index, p=weights)
        df.loc[chosen_idx, "is_ch"] = True

    return df


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/nodes.csv")
    df = select_cluster_heads_leach(df)
    print(df[df["is_ch"]][["node_id", "cluster_id", "energy"]])
