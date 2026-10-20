"""
Computes network-level performance metrics from packet simulation
results and node state, used for the comparison graphs.
"""

import pandas as pd


def packet_delivery_ratio(packet_df):
    if len(packet_df) == 0:
        return 0.0
    delivered = (packet_df["status"] == "Delivered").sum()
    return delivered / len(packet_df)


def average_delay(packet_df):
    delivered = packet_df[packet_df["status"] == "Delivered"]
    if len(delivered) == 0:
        return 0.0
    return delivered["delay_ms"].mean()


def average_energy_remaining(node_df):
    return node_df["energy"].mean()


def network_lifetime_rounds(node_df, G, route_selector, packet_sim_fn, energy_drain_fn,
                             death_threshold=5.0, max_rounds=200, packets_per_round=100):
    """
    Repeatedly runs packet simulation + energy drain rounds until the
    fraction of "dead" nodes (energy below death_threshold) exceeds
    10% of the network, or max_rounds is reached.

    Returns the number of rounds survived.
    """
    df = node_df.copy()
    for round_num in range(1, max_rounds + 1):
        packets = packet_sim_fn(df, G, route_selector, n_packets=packets_per_round, seed=round_num)
        df = energy_drain_fn(df, packets)

        dead = (df["energy"] <= death_threshold).sum()
        if dead / len(df) > 0.10:
            return round_num
    return max_rounds


def packet_loss_ratio(packet_df):
    if len(packet_df) == 0:
        return 0.0
    dropped = (packet_df["status"] == "Dropped").sum()
    return dropped / len(packet_df)


def summarize(node_df, packet_df):
    return {
        "packet_delivery_ratio": packet_delivery_ratio(packet_df),
        "packet_loss_ratio": packet_loss_ratio(packet_df),
        "average_delay_ms": average_delay(packet_df),
        "average_energy_remaining": average_energy_remaining(node_df),
    }


if __name__ == "__main__":
    node_df = pd.read_csv("data/nodes.csv")
    packet_df = pd.read_csv("data/results.csv")
    print(summarize(node_df, packet_df))
