"""
Generates a synthetic training dataset for the cluster-head-suitability
classifier. We don't have a real-world dataset, so we simulate one
using rule-based labeling plus noise, which is standard practice for
this kind of capstone project.
"""

import numpy as np
import pandas as pd


def generate_training_data(n_samples=10000, seed=42):
    rng = np.random.default_rng(seed)

    energy = rng.uniform(10, 100, n_samples)
    distance = rng.uniform(1, 80, n_samples)
    trust = rng.uniform(0, 1, n_samples)
    packet_delivery = rng.uniform(0.4, 1.0, n_samples)
    neighbors = rng.integers(1, 15, n_samples)

    # Rule-based "ground truth" score -- a good cluster head has:
    # high energy, low distance to BS, high trust, high delivery, many neighbors
    score = (
        0.30 * (energy / 100)
        + 0.20 * (1 - distance / 80)
        + 0.20 * trust
        + 0.20 * packet_delivery
        + 0.10 * (neighbors / 15)
    )

    # Add noise so the boundary isn't trivially linear
    noise = rng.normal(0, 0.05, n_samples)
    score_noisy = score + noise

    threshold = np.percentile(score_noisy, 75)  # top 25% become CH-suitable
    ch_label = (score_noisy >= threshold).astype(int)

    df = pd.DataFrame({
        "energy": energy,
        "distance": distance,
        "trust": trust,
        "packet_delivery": packet_delivery,
        "neighbors": neighbors,
        "CH": ch_label,
    })
    return df


if __name__ == "__main__":
    df = generate_training_data(n_samples=10000, seed=42)
    df.to_csv("data/training_data.csv", index=False)
    print(f"Generated {len(df)} training rows -> data/training_data.csv")
    print(df["CH"].value_counts())
    print(df.head())
