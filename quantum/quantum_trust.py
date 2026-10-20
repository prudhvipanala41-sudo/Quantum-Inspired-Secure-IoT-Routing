"""
Quantum Density Matrix Trace Fidelity Trust Estimator (QDMTF-TE).
Models IoT forwarding behavior through 2-level quantum state projections,
state purity gamma = Tr(rho^2), and quantum trace distance D_tr.
"""

import numpy as np
import pandas as pd


def compute_quantum_trust(df, beta=0.2):
    """
    Computes Quantum Density Matrix Trust for each IoT node.

    Formulation:
    - Forwarding success probability: p_s = forwarded / sent
    - Node Density Matrix: rho = (1 - p_s)|0><0| + p_s|1><1|
    - Quantum State Purity: gamma = Tr(rho^2) = (1 - p_s)^2 + p_s^2
    - Quantum Trace Distance to Ideal Node: D_tr = 1 - p_s
    - Quantum Trust Metric: T_Q = p_s * sqrt(gamma) * (1 - beta * D_tr)
    """
    df = df.copy()

    if "forwarded" not in df.columns or "sent" not in df.columns:
        # Defaults if not simulated
        df["sent"] = 100
        df["forwarded"] = 100

    sent = df["sent"].values.astype(float)
    forwarded = df["forwarded"].values.astype(float)

    # Success ratio
    p_s = np.clip(forwarded / np.maximum(sent, 1.0), 0.0, 1.0)

    # Quantum state purity
    purity = (1.0 - p_s) ** 2 + (p_s ** 2)

    # Quantum trace distance
    d_trace = 1.0 - p_s

    # Quantum-Enhanced Trust score
    q_trust = p_s * np.sqrt(purity) * (1.0 - (beta * d_trace))
    df["trust"] = np.clip(q_trust, 0.0, 1.0)
    df["quantum_purity"] = purity
    df["quantum_trace_dist"] = d_trace

    return df


def classify_quantum_trust(df, trusted_th=0.75, suspicious_th=0.45):
    """
    Classifies nodes based on Quantum Trust & Density Matrix Purity.
    """
    df = df.copy()

    labels = []
    for _, row in df.iterrows():
        t = row["trust"]
        if t >= trusted_th:
            labels.append("trusted")
        elif t >= suspicious_th:
            labels.append("suspicious")
        else:
            labels.append("malicious")

    df["trust_label"] = labels
    return df


if __name__ == "__main__":
    test_df = pd.DataFrame({
        "node_id": [0, 1, 2, 3],
        "sent": [100, 100, 100, 100],
        "forwarded": [98, 85, 45, 10],
        "is_malicious": [False, False, True, True],
    })

    test_df = compute_quantum_trust(test_df)
    test_df = classify_quantum_trust(test_df)
    print("=== QUANTUM TRUST EVALUATION ===")
    print(test_df[["node_id", "forwarded", "trust", "quantum_purity", "trust_label"]])
