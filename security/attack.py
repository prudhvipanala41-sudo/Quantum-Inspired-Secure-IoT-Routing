"""
Simulates malicious nodes that exhibit packet-dropping (blackhole-type)
behavior in the network.
"""

import numpy as np


def inject_malicious_nodes(df, malicious_ratio=0.1, seed=42):
    """
    Randomly mark a fraction of nodes as malicious. Malicious nodes
    get a drop_probability indicating how likely they are to drop a
    packet instead of forwarding it.

    Returns a copy of df with 'is_malicious' and 'drop_probability'
    columns.
    """
    rng = np.random.default_rng(seed)
    df = df.copy()

    n_malicious = max(1, int(len(df) * malicious_ratio)) if malicious_ratio > 0 else 0
    malicious_ids = rng.choice(df.index, size=n_malicious, replace=False) if n_malicious else []

    df["is_malicious"] = False
    df["drop_probability"] = 0.0

    if len(malicious_ids):
        df.loc[malicious_ids, "is_malicious"] = True
        # Malicious nodes drop 50-90% of packets
        df.loc[malicious_ids, "drop_probability"] = rng.uniform(0.5, 0.9, len(malicious_ids))

    return df


def simulate_packet_forwarding(df, attempts_per_node=100, seed=42):
    """
    Simulate `attempts_per_node` forwarding attempts per node.
    Normal nodes forward with high probability (95-100%); malicious
    nodes forward with (1 - drop_probability).

    Returns df with 'sent', 'forwarded' columns added.
    """
    rng = np.random.default_rng(seed)
    df = df.copy()

    sent = np.full(len(df), attempts_per_node)
    forwarded = np.zeros(len(df), dtype=int)

    for i, row in df.iterrows():
        if row.get("is_malicious", False):
            success_p = 1 - row["drop_probability"]
        else:
            success_p = rng.uniform(0.95, 1.0)
        forwarded[df.index.get_loc(i)] = rng.binomial(attempts_per_node, success_p)

    df["sent"] = sent
    df["forwarded"] = forwarded
    return df


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/nodes.csv")
    df = inject_malicious_nodes(df, malicious_ratio=0.1)
    df = simulate_packet_forwarding(df)
    print(df[df["is_malicious"]][["node_id", "drop_probability", "sent", "forwarded"]])
