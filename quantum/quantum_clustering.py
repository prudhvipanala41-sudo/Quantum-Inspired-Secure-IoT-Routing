"""
Quantum State Hilbert Space Clustering Framework for IoT Topologies.
Implements:
1. QDF-KMeans: Quantum Density-Matrix Fidelity K-Means
2. QSE-FCM: Quantum Superposition Entropic Fuzzy C-Means (with Quantum Tunneling Escape)
3. Classical K-Means & Classical FCM (Baselines)
4. Comprehensive Clustering Quality and Quantum Coherence Metrics
"""

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans

from quantum.quantum_embeddings import (
    quantum_state_embedding,
    quantum_state_fidelity,
    bloch_sphere_coordinates,
)


class QuantumFidelityKMeans:
    """
    Quantum Density-Matrix Fidelity K-Means (QDF-KMeans).
    Clustering in normalized complex Hilbert space using quantum overlap fidelity distance:
        D_Q(|psi_i>, |phi_j>) = 1 - |<psi_i | phi_j>|^2
    """

    def __init__(self, n_clusters=5, max_iter=100, tol=1e-5, random_state=42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_ = None       # Centroid statevectors in Hilbert space
        self.labels_ = None
        self.inertia_ = 0.0
        self.convergence_history_ = []

    def fit_predict(self, X):
        rng = np.random.default_rng(self.random_state)
        # Quantum state embedding
        Psi = quantum_state_embedding(X)  # shape (N, Dim)
        n_samples, dim = Psi.shape
        k = min(self.n_clusters, n_samples)

        # Quantum K-Means++ initialization in Hilbert Space
        init_idx = [rng.choice(n_samples)]
        for _ in range(1, k):
            fidelities = np.zeros(n_samples)
            for cid in init_idx:
                f_c = quantum_state_fidelity(Psi, Psi[cid])
                fidelities = np.maximum(fidelities, f_c)
            # Distance in Hilbert space = 1 - fidelity
            dist_q = np.maximum(0.0, 1.0 - fidelities).ravel()
            prob = dist_q / (np.sum(dist_q) + 1e-12)
            prob = prob / np.sum(prob)
            next_idx = rng.choice(n_samples, p=prob)
            init_idx.append(next_idx)

        # Initialize centroids as pure quantum states
        centers = Psi[init_idx].copy()

        labels = np.zeros(n_samples, dtype=int)

        for it in range(self.max_iter):
            # Step 1: Assign each statevector to cluster with highest quantum overlap fidelity
            # Fidelity matrix shape: (N, K)
            F = quantum_state_fidelity(Psi, centers)
            # Quantum distance: D_Q = 1 - F
            D_Q = 1.0 - F
            new_labels = np.argmin(D_Q, axis=1)

            total_distortion = np.sum(np.min(D_Q, axis=1))
            self.convergence_history_.append(total_distortion)

            # Step 2: Update centroid statevectors via Frechet quantum mean in Hilbert space
            new_centers = np.zeros((k, dim), dtype=complex)
            for j in range(k):
                members = Psi[new_labels == j]
                if len(members) > 0:
                    # Quantum superposition mean
                    mean_state = np.sum(members, axis=0)
                    norm = np.linalg.norm(mean_state)
                    new_centers[j] = mean_state / (norm + 1e-12)
                else:
                    # Reinitialize empty cluster
                    new_centers[j] = Psi[rng.choice(n_samples)]

            # Check convergence via centroid fidelity shifts
            center_fidelity_shift = np.mean(1.0 - np.abs(np.sum(centers * new_centers.conj(), axis=1)) ** 2)
            centers = new_centers
            labels = new_labels

            if center_fidelity_shift < self.tol:
                break

        self.cluster_centers_ = centers
        self.labels_ = labels
        self.inertia_ = float(total_distortion)
        return labels


class QuantumSuperpositionFCM:
    """
    Quantum Superposition Entropic Fuzzy C-Means (QSE-FCM).
    Integrates Quantum State Overlap Fidelity with Von Neumann Entropic Coherence
    and Simulated Quantum Tunneling to escape saddle points.
    """

    def __init__(self, n_clusters=5, m=2.0, max_iter=100, tol=1e-5, tunneling_rate=0.05, random_state=42):
        self.n_clusters = n_clusters
        self.m = m  # fuzzifier parameter
        self.max_iter = max_iter
        self.tol = tol
        self.tunneling_rate = tunneling_rate
        self.random_state = random_state
        self.cluster_centers_ = None
        self.u_matrix_ = None       # Fuzzy membership in superposition
        self.labels_ = None
        self.objective_history_ = []

    def fit_predict(self, X):
        rng = np.random.default_rng(self.random_state)
        Psi = quantum_state_embedding(X)
        n_samples, dim = Psi.shape
        k = min(self.n_clusters, n_samples)

        # Initialize random fuzzy superposition membership matrix U (N, K)
        U = rng.uniform(0.1, 1.0, (n_samples, k))
        U = U / np.sum(U, axis=1, keepdims=True)

        centers = np.zeros((k, dim), dtype=complex)

        for it in range(self.max_iter):
            # 1. Update Quantum Centroid Statevectors: |phi_j> = sum_i (u_ij^m |psi_i>) / norm
            Um = U ** self.m
            for j in range(k):
                weighted_sum = np.sum(Um[:, j : j + 1] * Psi, axis=0)
                norm = np.linalg.norm(weighted_sum)
                centers[j] = weighted_sum / (norm + 1e-12)

            # 2. Compute Quantum Overlap Distance D_Q(i, j) = 1 - |<psi_i | phi_j>|^2
            F = quantum_state_fidelity(Psi, centers)
            D_Q = np.maximum(1e-8, 1.0 - F)

            # 3. Update Membership Matrix U in Quantum Superposition
            power = 1.0 / (self.m - 1.0)
            D_inv = D_Q ** (-power)
            new_U = D_inv / np.sum(D_inv, axis=1, keepdims=True)

            # 4. Quantum Tunneling Perturbation (Simulates barrier penetration if trapped)
            if self.tunneling_rate > 0 and it < self.max_iter // 2:
                tunnel_barrier = np.exp(-it / 10.0) * self.tunneling_rate
                quantum_noise = rng.uniform(-tunnel_barrier, tunnel_barrier, new_U.shape)
                new_U = np.clip(new_U + quantum_noise, 1e-6, 1.0)
                new_U = new_U / np.sum(new_U, axis=1, keepdims=True)

            # Quantum Entropic Objective Value
            obj_val = np.sum((new_U ** self.m) * D_Q)
            # Von Neumann entropy regularization term: -lambda * sum u ln(u)
            entropy_reg = -0.01 * np.sum(new_U * np.log(new_U + 1e-12))
            total_obj = float(obj_val + entropy_reg)
            self.objective_history_.append(total_obj)

            diff = np.max(np.abs(new_U - U))
            U = new_U

            if diff < self.tol:
                break

        self.cluster_centers_ = centers
        self.u_matrix_ = U
        self.labels_ = np.argmax(U, axis=1)
        return self.labels_


class ClassicalFCM:
    """
    Classical Fuzzy C-Means (Baseline).
    """

    def __init__(self, n_clusters=5, m=2.0, max_iter=100, tol=1e-5, random_state=42):
        self.n_clusters = n_clusters
        self.m = m
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_ = None
        self.u_matrix_ = None
        self.labels_ = None

    def fit_predict(self, X):
        rng = np.random.default_rng(self.random_state)
        n_samples, dim = X.shape
        k = min(self.n_clusters, n_samples)

        U = rng.uniform(0.1, 1.0, (n_samples, k))
        U = U / np.sum(U, axis=1, keepdims=True)

        centers = np.zeros((k, dim))

        for it in range(self.max_iter):
            Um = U ** self.m
            for j in range(k):
                centers[j] = np.sum(Um[:, j : j + 1] * X, axis=0) / (np.sum(Um[:, j]) + 1e-12)

            # Euclidean distance
            D = np.zeros((n_samples, k))
            for j in range(k):
                D[:, j] = np.linalg.norm(X - centers[j], axis=1)
            D = np.maximum(1e-8, D)

            power = 2.0 / (self.m - 1.0)
            D_inv = D ** (-power)
            new_U = D_inv / np.sum(D_inv, axis=1, keepdims=True)

            if np.max(np.abs(new_U - U)) < self.tol:
                break
            U = new_U

        self.cluster_centers_ = centers
        self.u_matrix_ = U
        self.labels_ = np.argmax(U, axis=1)
        return self.labels_


def compute_clustering_metrics(X, labels):
    """
    Computes rigorous clustering performance evaluation metrics:
    - Silhouette Score (higher is better, range [-1, 1])
    - Davies-Bouldin Index (lower is better, >= 0)
    - Calinski-Harabasz Index (higher is better)
    - Quantum Coherence Entropy (lower is more coherent)
    """
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2 or len(unique_labels) >= len(X):
        return {
            "silhouette": 0.0,
            "davies_bouldin": 999.0,
            "calinski_harabasz": 0.0,
            "quantum_coherence": 1.0,
        }

    try:
        sil = float(silhouette_score(X, labels))
    except Exception:
        sil = 0.0

    try:
        db = float(davies_bouldin_score(X, labels))
    except Exception:
        db = 999.0

    try:
        ch = float(calinski_harabasz_score(X, labels))
    except Exception:
        ch = 0.0

    # Quantum Coherence calculation
    Psi = quantum_state_embedding(X)
    coherences = []
    for cid in unique_labels:
        cluster_psi = Psi[labels == cid]
        if len(cluster_psi) > 1:
            mean_state = np.mean(cluster_psi, axis=0)
            coherence = float(np.mean(quantum_state_fidelity(cluster_psi, mean_state)))
            coherences.append(coherence)
        else:
            coherences.append(1.0)

    avg_quantum_coherence = float(np.mean(coherences))

    return {
        "silhouette": sil,
        "davies_bouldin": db,
        "calinski_harabasz": ch,
        "quantum_coherence": avg_quantum_coherence,
    }


def cluster_nodes_quantum(df, method="qse_fcm", n_clusters=5, seed=42):
    """
    Clustering dispatcher supporting:
    - 'qse_fcm'     : Quantum Superposition Entropic Fuzzy C-Means (Proposed)
    - 'qdf_kmeans'  : Quantum Density-Matrix Fidelity K-Means (Proposed)
    - 'cmeans'      : Classical Fuzzy C-Means
    - 'kmeans'      : Classical K-Means

    Returns:
        (df_with_cluster_id, model, metrics_dict, bloch_coords)
    """
    df = df.copy()
    feature_cols = ["x", "y"]
    if "energy" in df.columns and "trust" in df.columns and "distance_to_bs" in df.columns:
        # Multi-attribute quantum state embedding incorporates spatial + operational metrics
        features = df[["x", "y", "energy", "trust", "distance_to_bs"]].values
    else:
        features = df[feature_cols].values

    if method == "qse_fcm":
        model = QuantumSuperpositionFCM(n_clusters=n_clusters, random_state=seed)
        labels = model.fit_predict(features)
    elif method == "qdf_kmeans":
        model = QuantumFidelityKMeans(n_clusters=n_clusters, random_state=seed)
        labels = model.fit_predict(features)
    elif method == "cmeans":
        model = ClassicalFCM(n_clusters=n_clusters, random_state=seed)
        labels = model.fit_predict(df[feature_cols].values)
    elif method == "kmeans":
        model = KMeans(n_clusters=n_clusters, random_state=seed, n_init=10)
        labels = model.fit_predict(df[feature_cols].values)
    else:
        raise ValueError(f"Unknown clustering method: {method}")

    df["cluster_id"] = labels

    # Spatial coordinates for metric evaluation
    metrics = compute_clustering_metrics(df[["x", "y"]].values, labels)

    # Compute Bloch sphere coordinates for quantum visualization
    Psi = quantum_state_embedding(features)
    bloch_coords = bloch_sphere_coordinates(Psi)
    df["bloch_x"] = bloch_coords[:, 0]
    df["bloch_y"] = bloch_coords[:, 1]
    df["bloch_z"] = bloch_coords[:, 2]

    return df, model, metrics, bloch_coords


if __name__ == "__main__":
    from simulation.node_generator import generate_nodes, distance_to_bs

    nodes = generate_nodes(n=60, area=100, seed=42)
    nodes = distance_to_bs(nodes, area=100)

    print("=== BENCHMARKING CLUSTERING ALGORITHMS ===")
    for m in ["kmeans", "cmeans", "qdf_kmeans", "qse_fcm"]:
        df_res, model, met, _ = cluster_nodes_quantum(nodes, method=m, n_clusters=5, seed=42)
        print(f"[{m.upper()}] -> Silhouette: {met['silhouette']:.4f}, Davies-Bouldin: {met['davies_bouldin']:.4f}, Coherence: {met['quantum_coherence']:.4f}")
