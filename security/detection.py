"""
Evaluates malicious-node detection performance by comparing the
trust-based classification against the ground-truth 'is_malicious'
labels that were injected during simulation.
"""

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def evaluate_detection(df):
    """
    Requires 'is_malicious' (ground truth) and 'trust_label' (predicted)
    columns. Treats trust_label == 'malicious' as the positive
    "detected as malicious" prediction.

    Returns a dict of accuracy / precision / recall / f1 and the
    confusion matrix.
    """
    y_true = df["is_malicious"].astype(int)
    y_pred = (df["trust_label"] == "malicious").astype(int)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }
    return metrics


if __name__ == "__main__":
    from attack import inject_malicious_nodes, simulate_packet_forwarding
    from trust import compute_trust, classify_trust

    df = pd.read_csv("data/nodes.csv")
    df = inject_malicious_nodes(df, malicious_ratio=0.15)
    df = simulate_packet_forwarding(df)
    df = compute_trust(df)
    df = classify_trust(df)

    metrics = evaluate_detection(df)
    print("=== Malicious Node Detection Performance ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
