"""
End-to-end smoke test, benchmark suite, and patent specification compiler.
Executes comparison across:
1. LEACH Baseline
2. LEACH + PSO
3. Proposed Classical (K-Means + RF + Trust + PSO)
4. Quantum-Inspired (QDF-KMeans + VQC + Q-Trust + Q-PSO)
5. Full Quantum Superposition (QSE-FCM + VQC + Q-Trust + Q-PSO)

Configured for 1000 Total Nodes with 500 Sample Nodes Executed.
Generates full Suite of 10 Publication-Quality Graph Visualizations.
Saves summary CSV, comparison plots, and Patent Specification.
"""

import os
import sys
import pandas as pd

# Safe encoding for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ml.generate_dataset import generate_training_data
from ml.train_model import train as train_ch_model
from pipeline import run_full_comparison
from results.graphs import generate_all_10_graphs
from patent.patent_spec import save_patent_artifacts

OUTPUT_DIR = "results/output"


def ensure_model_ready():
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/training_data.csv"):
        print("[*] Generating ML training dataset...")
        df = generate_training_data(n_samples=10000, seed=42)
        df.to_csv("data/training_data.csv", index=False)

    if not os.path.exists("models/cluster_head_model.pkl"):
        print("[*] Training Random Forest cluster-head model...")
        train_ch_model()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ensure_model_ready()

    print("\n" + "=" * 78)
    print("[*] QUANTUM-ENHANCED SECURE IoT CLUSTERING & ROUTING BENCHMARK (1000 NODES)")
    print("=" * 78)
    print("[*] Total Topology Nodes: 1000 | Active Sample Executed Nodes: 1000 (full topology)")
    print("[*] Simulating IoT Network across 5 paradigms...")

    results = run_full_comparison(
        n_nodes=1000,
        sample_nodes_count=None,  # use all 1000 nodes, no downsampling
        n_clusters=8,
        area=200,
        malicious_ratio=0.1,
        n_packets=500,
        seed=42,
        include_all_quantum=True
    )

    name_mapping = {
        "leach": "LEACH",
        "leach_pso": "LEACH+PSO",
        "proposed": "Proposed (Classical)",
        "quantum_inspired": "Quantum-Inspired",
        "quantum_superposition": "Full Quantum Superposition",
    }

    summary_rows = []
    print("\n" + "-" * 78)
    print(f"{'Method':<28} | {'PDR':<7} | {'Loss':<7} | {'Delay(ms)':<10} | {'Energy(%)':<10} | {'Det F1':<7}")
    print("-" * 78)

    for method, data in results.items():
        m = data["metrics"]
        label = name_mapping.get(method, method)
        row = {
            "method": label,
            "packet_delivery_ratio": m["packet_delivery_ratio"],
            "packet_loss_ratio": m["packet_loss_ratio"],
            "average_delay_ms": m["average_delay_ms"],
            "average_energy_remaining": m["average_energy_remaining"],
            "detection_f1": m["detection"]["f1"],
        }
        summary_rows.append(row)
        print(f"{label:<28} | {row['packet_delivery_ratio']:<7.3f} | {row['packet_loss_ratio']:<7.3f} | {row['average_delay_ms']:<10.2f} | {row['average_energy_remaining']:<10.2f} | {row['detection_f1']:<7.3f}")

    print("-" * 78)

    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(OUTPUT_DIR, "comparison_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"\n[+] Summary CSV saved -> {summary_path}")

    # Generate Full Suite of 10 Publication-Quality Graphs
    print("\n[*] Generating Full Suite of 10 Publication-Quality Graphs...")
    generated_graphs = generate_all_10_graphs(results, output_dir=OUTPUT_DIR, seed=42)
    for g in generated_graphs:
        print(f"    [+] Generated -> {g}")

    # Generate Patent Specification
    patent_file = save_patent_artifacts("data")
    print(f"\n[+] Formal Patent Specification generated -> {patent_file}")

    print("\n" + "=" * 78)
    print("[+] BENCHMARK COMPLETE! Launch the Cyber-Quantum Web Dashboard with:")
    print("    streamlit run dashboard/app.py")
    print("=" * 78)


if __name__ == "__main__":
    main()
