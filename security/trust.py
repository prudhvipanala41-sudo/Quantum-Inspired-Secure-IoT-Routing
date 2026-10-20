"""
Computes trust scores for nodes based on packet-forwarding history,
and classifies nodes as Trusted / Suspicious / Malicious.
"""

import pandas as pd


def compute_trust(df):
    """
    trust = forwarded / sent

    Requires 'sent' and 'forwarded' columns
    (see security/attack.py::simulate_packet_forwarding).
    """
    df = df.copy()
    df["trust"] = (df["forwarded"] / df["sent"]).clip(0, 1)
    return df


def classify_trust(df, trusted_th=0.8, suspicious_th=0.5):
    """
    Adds a 'trust_label' column:
        trust > trusted_th            -> 'trusted'
        suspicious_th <= trust <= trusted_th -> 'suspicious'
        trust < suspicious_th         -> 'malicious'
    """
    df = df.copy()

    def label(t):
        if t > trusted_th:
            return "trusted"
        elif t >= suspicious_th:
            return "suspicious"
        else:
            return "malicious"

    df["trust_label"] = df["trust"].apply(label)
    return df


if __name__ == "__main__":
    from attack import inject_malicious_nodes, simulate_packet_forwarding

    df = pd.read_csv("data/nodes.csv")
    df = inject_malicious_nodes(df, malicious_ratio=0.1)
    df = simulate_packet_forwarding(df)
    df = compute_trust(df)
    df = classify_trust(df)

    print(df[["node_id", "is_malicious", "trust", "trust_label"]].sort_values("trust"))
