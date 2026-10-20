"""
Clustering module for IoT nodes supporting both classical and quantum algorithms:
- Quantum Superposition Entropic Fuzzy C-Means (QSE-FCM) [Proposed Quantum]
- Quantum Density-Matrix Fidelity K-Means (QDF-KMeans) [Proposed Quantum]
- Classical Fuzzy C-Means (C-Means)
- Classical K-Means (Baseline)
"""

import pandas as pd
from sklearn.cluster import KMeans
from quantum.quantum_clustering import cluster_nodes_quantum


def cluster_nodes(df, method="qse_fcm", n_clusters=5, seed=42):
    """
    Assign each node to a cluster using either Quantum or Classical clustering.

    Parameters
    ----------
    df : pd.DataFrame
        Nodes dataframe.
    method : str
        'qse_fcm'     : Quantum Superposition Entropic Fuzzy C-Means (Default Proposed)
        'qdf_kmeans'  : Quantum Density-Matrix Fidelity K-Means
        'cmeans'      : Classical Fuzzy C-Means
        'kmeans'      : Classical K-Means baseline
    n_clusters : int
        Number of clusters
    seed : int
        Random seed

    Returns
    -------
    (df_clustered, model)
    """
    df_clustered, model, metrics, bloch_coords = cluster_nodes_quantum(
        df, method=method, n_clusters=n_clusters, seed=seed
    )
    return df_clustered, model


if __name__ == "__main__":
    from simulation.node_generator import generate_nodes, distance_to_bs

    nodes = generate_nodes(n=50, area=100, seed=42)
    nodes = distance_to_bs(nodes)
    clustered, model = cluster_nodes(nodes, method="qse_fcm", n_clusters=5)
    clustered.to_csv("data/nodes.csv", index=False)
    print(clustered[["node_id", "x", "y", "cluster_id", "bloch_x", "bloch_y", "bloch_z"]].head(10))
    print("\nCluster sizes:")
    print(clustered["cluster_id"].value_counts().sort_index())
