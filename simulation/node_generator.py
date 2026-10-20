"""
Generates a virtual IoT network of N nodes with random positions,
energy, trust, and packet-rate attributes. Also places a Base Station
at the center of the simulation area.
"""

import numpy as np
import pandas as pd


def generate_nodes(n=1000, area=200, seed=None):
    """
    Create N virtual IoT nodes (default: 1000 nodes in 200m x 200m area).

    Parameters
    ----------
    n : int          Number of nodes (default 1000)
    area : float     Side length of the square simulation area (default 200)
    seed : int|None  RNG seed for reproducibility

    Returns
    -------
    pd.DataFrame with columns:
        node_id, x, y, energy, trust, packet_rate,
        cluster_id, is_ch, is_malicious
    """
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "node_id": np.arange(n),
        "x": rng.uniform(0, area, n),
        "y": rng.uniform(0, area, n),
        "energy": rng.uniform(70, 100, n),          # start with healthy energy
        "trust": np.ones(n),                         # starts fully trusted
        "packet_rate": rng.integers(5, 25, n),        # packets generated per round
        "cluster_id": -1,                             # assigned later
        "is_ch": False,                                # assigned later
        "is_malicious": False,                         # assigned later
    })
    return df


def sample_nodes(df, n_samples=500, seed=42):
    """
    Sample n_samples from a larger node DataFrame for high-speed benchmark execution.

    Parameters
    ----------
    df : pd.DataFrame
        Source DataFrame containing full set of nodes (e.g., 1000 nodes)
    n_samples : int
        Number of active nodes to sample for execution (default 500)
    seed : int
        RNG seed

    Returns
    -------
    pd.DataFrame with reindexed node_id for seamless execution.
    """
    if len(df) <= n_samples:
        return df.copy()

    rng = np.random.default_rng(seed)
    sampled_indices = rng.choice(len(df), size=n_samples, replace=False)
    sampled_indices.sort()
    sampled_df = df.iloc[sampled_indices].copy().reset_index(drop=True)
    sampled_df["node_id"] = np.arange(len(sampled_df))
    return sampled_df


def get_base_station(area=200):
    """Base Station sits at the center of the simulation area."""
    return {"x": area / 2, "y": area / 2}


def distance_to_bs(df, area=200):
    """Add a distance_to_bs column (Euclidean distance to Base Station)."""
    bs = get_base_station(area)
    df = df.copy()
    df["distance_to_bs"] = np.sqrt((df["x"] - bs["x"]) ** 2 + (df["y"] - bs["y"]) ** 2)
    return df


if __name__ == "__main__":
    nodes = generate_nodes(n=1000, area=200, seed=42)
    nodes = distance_to_bs(nodes, area=200)
    nodes.to_csv("data/nodes.csv", index=False)
    print(f"Generated {len(nodes)} nodes -> data/nodes.csv")
    print(nodes.head())
    sample = sample_nodes(nodes, n_samples=500, seed=42)
    print(f"Sampled {len(sample)} execution nodes for simulation.")
