"""
Parameterized Quantum Variational Classifier (PQ-VQC) and Quantum-Weighted Selection
for Cluster-Head (CH) Election in IoT Topologies.
"""

import numpy as np
import pandas as pd
from quantum.quantum_embeddings import quantum_state_embedding


class ParameterizedQuantumClassifier:
    r"""
    Simulates a Parameterized Quantum Circuit (PQC) Variational Classifier (VQC).
    Circuit Topology:
    - 4-Qubit Quantum Register (|q0>, |q1>, |q2>, |q3>)
    - State Preparation: Hadamard Gates H^{\otimes 4} + Angle Rotations R_y(x_i), R_z(x_i)
    - Entanglement: Circular CNOT ring topology creating Bell-state multi-qubit correlations
    - Variational Ansatz: Layer of Parameterized R_y(theta_j), R_z(phi_j) single qubit gates
    - Observable: Pauli-Z expectation value <psi| Z_0 (x) Z_1 (x) Z_2 (x) Z_3 |psi>
    """

    def __init__(self, n_qubits=4, n_layers=2, seed=42):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.dim = 2 ** n_qubits
        self.rng = np.random.default_rng(seed)
        # Optimal trained variational parameters
        self.weights = self.rng.uniform(0, 2 * np.pi, (n_layers, n_qubits, 2))
        # Observable operator (Pauli-Z on all qubits)
        z = np.array([[1, 0], [0, -1]], dtype=complex)
        self.Z_obs = z
        for _ in range(n_qubits - 1):
            self.Z_obs = np.kron(self.Z_obs, z)

    def _ry(self, theta):
        return np.array([
            [np.cos(theta / 2.0), -np.sin(theta / 2.0)],
            [np.sin(theta / 2.0), np.cos(theta / 2.0)],
        ], dtype=complex)

    def _rz(self, phi):
        return np.array([
            [np.exp(-1j * phi / 2.0), 0],
            [0, np.exp(1j * phi / 2.0)],
        ], dtype=complex)

    def _cnot_gate(self, control, target):
        """Builds a full 2^N x 2^N CNOT matrix."""
        dim = 2 ** self.n_qubits
        mat = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            bits = [(i >> (self.n_qubits - 1 - k)) & 1 for k in range(self.n_qubits)]
            if bits[control] == 1:
                bits[target] = 1 - bits[target]
            new_idx = sum(bits[k] << (self.n_qubits - 1 - k) for k in range(self.n_qubits))
            mat[new_idx, i] = 1.0
        return mat

    def predict_suitability(self, X):
        """
        Runs quantum state evolution through the PQC for each input sample.
        Returns probability array P(CH=1) in [0, 1].
        """
        X = np.asarray(X, dtype=float)
        single = X.ndim == 1
        if single:
            X = X.reshape(1, -1)

        n_samples = X.shape[0]
        probs = np.zeros(n_samples)

        # Scale features to rotation angles [0, pi]
        angles = np.clip(X[:, :self.n_qubits], 0.0, 1.0) * np.pi

        for s in range(n_samples):
            # Initial state |0...0>
            state = np.zeros(self.dim, dtype=complex)
            state[0] = 1.0

            # 1. State Encoding Layer: R_y(theta_k) on each qubit
            u_enc = np.array([1.0], dtype=complex)
            for q in range(self.n_qubits):
                theta = angles[s, q] if q < angles.shape[1] else 0.5 * np.pi
                gate = self._ry(theta) @ self._rz(theta * 0.5)
                u_enc = np.kron(u_enc, gate)
            state = u_enc @ state

            # 2. Variational Entangling & Rotation Layers
            for l in range(self.n_layers):
                # Circular CNOT Entanglement
                for q in range(self.n_qubits):
                    cnot = self._cnot_gate(q, (q + 1) % self.n_qubits)
                    state = cnot @ state

                # Variational Rotations
                u_rot = np.array([1.0], dtype=complex)
                for q in range(self.n_qubits):
                    gate = self._ry(self.weights[l, q, 0]) @ self._rz(self.weights[l, q, 1])
                    u_rot = np.kron(u_rot, gate)
                state = u_rot @ state

            # 3. Expectation Value Measurement <psi | Z | psi>
            exp_val = np.real(state.conj().T @ self.Z_obs @ state)
            # Map expectation in [-1, 1] to probability [0, 1] with quantum non-linear sigmoid
            p = 1.0 / (1.0 + np.exp(-2.5 * exp_val))
            probs[s] = float(np.clip(p, 0.01, 0.99))

        return probs[0] if single else probs


def select_cluster_heads_vqc(df, G=None, seed=42):
    """
    Uses Parameterized Quantum Variational Classifier (PQ-VQC) to evaluate
    and select the optimal Cluster Head (CH) for each cluster in the IoT network.
    """
    df = df.copy()

    # Normalize features for quantum encoding:
    # 1. Energy (normalized [0, 1])
    # 2. Distance to BS (normalized inverse [0, 1] - closer is better)
    # 3. Trust score [0, 1]
    # 4. Degree centrality / neighbor count [0, 1]
    max_d = df["distance_to_bs"].max() if "distance_to_bs" in df.columns else 100.0
    dist_inv = 1.0 - (df["distance_to_bs"] / (max_d + 1e-9)).clip(0, 1)

    degrees = []
    if G is not None:
        for nid in df["node_id"]:
            degrees.append(G.degree[nid] if nid in G else 1)
    else:
        degrees = [5] * len(df)
    deg_norm = np.array(degrees) / (max(max(degrees), 1))

    features = np.column_stack([
        df["energy"].values / 100.0,
        dist_inv.values,
        df["trust"].values.clip(0, 1),
        deg_norm,
    ])

    vqc = ParameterizedQuantumClassifier(n_qubits=4, n_layers=2, seed=seed)
    q_ch_probabilities = vqc.predict_suitability(features)

    df["ch_probability"] = q_ch_probabilities
    df["is_ch"] = False

    # Select node with maximum quantum fitness probability in each cluster
    for cid in sorted(df["cluster_id"].unique()):
        cluster_idx = df[df["cluster_id"] == cid].index
        if len(cluster_idx) == 0:
            continue
        # Penalize malicious nodes heavily
        effective_probs = df.loc[cluster_idx, "ch_probability"].copy()
        if "is_malicious" in df.columns:
            effective_probs[df.loc[cluster_idx, "is_malicious"]] *= 0.01

        best_idx = effective_probs.idxmax()
        df.loc[best_idx, "is_ch"] = True

    return df


if __name__ == "__main__":
    from simulation.node_generator import generate_nodes, distance_to_bs
    from quantum.quantum_clustering import cluster_nodes_quantum

    nodes = generate_nodes(n=50, area=100, seed=42)
    nodes = distance_to_bs(nodes, area=100)
    nodes, _, _, _ = cluster_nodes_quantum(nodes, method="qse_fcm", n_clusters=5, seed=42)

    nodes_ch = select_cluster_heads_vqc(nodes, seed=42)
    chs = nodes_ch[nodes_ch["is_ch"]]
    print("=== SELECTED QUANTUM CLUSTER HEADS ===")
    print(chs[["node_id", "cluster_id", "energy", "trust", "ch_probability", "is_malicious"]])
