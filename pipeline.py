"""
End-to-end pipeline orchestrating both classical baselines and proposed quantum algorithms.
Supports 5 comprehensive paradigms for benchmarking:
1. "leach"                 -> LEACH CH Selection + Dijkstra Routing (Baseline)
2. "leach_pso"             -> LEACH CH Selection + Classical PSO Routing
3. "proposed"              -> Classical K-Means + Random Forest CH + Trust + PSO Routing
4. "quantum_inspired"      -> QDF-KMeans + Parameterized Quantum VQC + Quantum Trust + Q-PSO
5. "quantum_superposition" -> QSE-FCM + Parameterized Quantum VQC + Quantum Trust + Q-PSO (Full Quantum)
"""

import pandas as pd
import numpy as np

from simulation.node_generator import generate_nodes, sample_nodes, distance_to_bs
from simulation.clustering import cluster_nodes
from simulation.network import build_network_graph, ensure_connected
from simulation.packet_simulation import run_packet_simulation, apply_energy_drain

from algorithms.leach import select_cluster_heads_leach
from algorithms.shortest_path import dijkstra_route, k_shortest_paths

from ml.predict_cluster_head import select_cluster_heads_ml

from security.attack import inject_malicious_nodes, simulate_packet_forwarding
from security.trust import compute_trust, classify_trust
from security.detection import evaluate_detection

from optimization.pso import pso_select_route
from results.metrics import summarize

# Quantum modules
from quantum.quantum_clustering import cluster_nodes_quantum
from quantum.quantum_vqc_ch import select_cluster_heads_vqc
from quantum.quantum_pso_routing import qpso_select_route
from quantum.quantum_trust import compute_quantum_trust, classify_quantum_trust


def build_base_network(n_nodes=1000, sample_nodes_count=500, n_clusters=8, area=200, malicious_ratio=0.1, seed=42, clustering_method="qse_fcm"):
    """
    Builds the base virtual IoT topology with spatial coordinates, quantum states,
    malicious node injection, and packet forwarding history.
    Supports generating 1000 total nodes and sampling 500 nodes for high-speed simulation execution.
    """
    df = generate_nodes(n=n_nodes, area=area, seed=seed)
    df = distance_to_bs(df, area=area)

    # If sampling active nodes for execution
    if sample_nodes_count is not None and sample_nodes_count < len(df):
        df = sample_nodes(df, n_samples=sample_nodes_count, seed=seed)
        df = distance_to_bs(df, area=area)

    # Apply quantum or classical clustering
    df, _, _, _ = cluster_nodes_quantum(df, method=clustering_method, n_clusters=n_clusters, seed=seed)

    df = inject_malicious_nodes(df, malicious_ratio=malicious_ratio, seed=seed)
    df = simulate_packet_forwarding(df, seed=seed)

    # Compute both classical and quantum trust metrics
    df = compute_trust(df)
    df = compute_quantum_trust(df)
    df = classify_quantum_trust(df)

    return df


def run_method(method, df, area=200, comm_range=30, n_packets=500, seed=42, model_path="models/cluster_head_model.pkl"):
    """
    Executes Cluster-Head selection, graph construction, routing optimization,
    and packet transmission simulation for a given method.
    """
    df = df.copy()

    # --- 1. Clustering & Cluster Head Selection ---
    if method == "leach":
        df = select_cluster_heads_leach(df, seed=seed)
    elif method == "leach_pso":
        df = select_cluster_heads_leach(df, seed=seed)
    elif method == "proposed":
        try:
            df = select_cluster_heads_ml(df, model_path=model_path)
        except Exception:
            df = select_cluster_heads_leach(df, seed=seed)
    elif method == "quantum_inspired":
        # Quantum Fidelity K-Means + Parameterized Quantum VQC
        df, _, _, _ = cluster_nodes_quantum(df, method="qdf_kmeans", n_clusters=len(df["cluster_id"].unique()), seed=seed)
        df = select_cluster_heads_vqc(df, seed=seed)
    elif method == "quantum_superposition":
        # Quantum Superposition FCM + Parameterized Quantum VQC
        df, _, _, _ = cluster_nodes_quantum(df, method="qse_fcm", n_clusters=len(df["cluster_id"].unique()), seed=seed)
        df = select_cluster_heads_vqc(df, seed=seed)
    else:
        raise ValueError(f"Unknown method: {method}")

    # --- 2. Build Network Graph ---
    G = build_network_graph(df, area=area, comm_range=comm_range)
    G = ensure_connected(G, df, area=area, comm_range=comm_range)

    # --- 3. Route Selector ---
    if method == "leach":
        def route_selector(src, G):
            path, _ = dijkstra_route(G, src)
            return path
    elif method in ("leach_pso", "proposed"):
        def route_selector(src, G):
            candidates = k_shortest_paths(G, src, k=5)
            if not candidates:
                return None
            best_route, _, _ = pso_select_route(candidates, G, seed=seed)
            return best_route
    elif method in ("quantum_inspired", "quantum_superposition"):
        # Quantum-Behaved Delta-Well Swarm Optimization (Q-PSO)
        def route_selector(src, G):
            candidates = k_shortest_paths(G, src, k=6)
            if not candidates:
                return None
            best_route, _, _ = qpso_select_route(candidates, G, seed=seed)
            return best_route

    # --- 4. Packet Transmission Simulation ---
    packet_df = run_packet_simulation(df, G, route_selector, n_packets=n_packets, seed=seed)
    df = apply_energy_drain(df, packet_df)

    # --- 5. Detection & Evaluation Metrics ---
    detection_metrics = evaluate_detection(df)

    return df, packet_df, detection_metrics


def run_full_comparison(n_nodes=1000, sample_nodes_count=500, n_clusters=8, area=200, malicious_ratio=0.1,
                         n_packets=500, seed=42, model_path="models/cluster_head_model.pkl",
                         include_all_quantum=True):
    """
    Runs all benchmark and proposed quantum methods on the SAME base network (500 execution nodes from 1000 total nodes).
    """
    base_df = build_base_network(
        n_nodes=n_nodes, sample_nodes_count=sample_nodes_count, n_clusters=n_clusters, area=area,
        malicious_ratio=malicious_ratio, seed=seed
    )

    methods = ["leach", "leach_pso", "proposed"]
    if include_all_quantum:
        methods.extend(["quantum_inspired", "quantum_superposition"])

    results = {}
    for method in methods:
        node_df, packet_df, detection = run_method(
            method, base_df, area=area, n_packets=n_packets, seed=seed, model_path=model_path
        )
        metrics = summarize(node_df, packet_df)
        metrics["detection"] = detection
        results[method] = {
            "node_df": node_df,
            "packet_df": packet_df,
            "metrics": metrics,
        }

    return results


if __name__ == "__main__":
    results = run_full_comparison(n_nodes=1000, sample_nodes_count=500, n_packets=300, include_all_quantum=True)
    for method, data in results.items():
        print(f"\n=== {method.upper()} ===")
        for k, v in data["metrics"].items():
            if k != "detection":
                print(f"  {k}: {v:.4f}")
        print(f"  detection F1: {data['metrics']['detection']['f1']:.4f}")
