# ⚛️ Quantum Secure IoT Routing - MATLAB 10-Graph Results Suite

This folder contains the complete, publication-quality **MATLAB (.m)** plotting engine for the Quantum-Enhanced Secure IoT Routing Project.

---

## 📁 MATLAB Scripts Overview

| Script | Generated Output | Description |
| :--- | :--- | :--- |
| **`generate_all_10_graphs.m`** | All 10 Figures (`.png` & `.fig`) | Master runner that compiles and saves all 10 figures to `results/output/` |
| **`plot_1_network_topology.m`** | `1_network_topology_matlab.png` | Voronoi cluster tessellation, VQC CHs with radio range circles, malicious nodes, and BS links |
| **`plot_2_pdr_scalability.m`** | `2_pdr_scalability_matlab.png` | PDR vs network scale (100 to 1000 nodes) with shaded 95% ($\pm 1\sigma$) confidence bands |
| **`plot_3_latency_cdf_boxplot.m`** | `3_latency_delay_matlab.png` | Dual-panel: Cumulative Distribution Function (ECDF) + grouped boxplot quartile distributions |
| **`plot_4_energy_lifetime_survival.m`** | `4_energy_residual_matlab.png` | Network lifetime survival curve with First Node Dead (FND) and Half Nodes Dead (HND) markers |
| **`plot_5_throughput_goodput.m`** | `5_packet_loss_matlab.png` | Dual-Y axis: Goodput (kbps) vs packet drop rate (%) under adversarial stress |
| **`plot_6_quantum_trust_phase_diagram.m`**| `6_quantum_trust_matlab.png` | Quantum trust phase manifold $T_Q(p_s, \gamma)$ mapped against density matrix purity $\gamma = \text{Tr}(\rho^2)$ |
| **`plot_7_roc_pr_security_curves.m`** | `7_security_detection_matlab.png`| Dual-panel ROC curve (AUC=0.994) + Precision-Recall trade-off matrix |
| **`plot_8_qpso_phase_space_convergence.m`**| `8_qpso_convergence_matlab.png`| Multi-objective Hamiltonian cost minimization + wave packet probability density $|\psi(x)|^2$ |
| **`plot_9_clustering_radar_metrics.m`** | `9_clustering_metrics_matlab.png`| Multi-attribute 5-axis Spider/Radar chart + 3D grouped benchmark (Silhouette, Coherence, etc.) |
| **`plot_10_pareto_3d_front.m`** | `10_pareto_front_matlab.png` | 3D non-dominated Pareto surface manifold (Distance vs Delay vs Energy vs Security Risk) |

---

## 🚀 How to Run in MATLAB

1. Open **MATLAB** (R2020a or newer recommended).
2. Set your MATLAB Current Working Directory to the `matlab/` folder or the project root.
3. In the MATLAB Command Window, run:

```matlab
% Run all 10 graph generators at once
generate_all_10_graphs

% Or run any individual graph function, e.g.:
plot_1_network_topology(readtable('../data/nodes.csv'), '../results/output')
plot_2_pdr_scalability('../results/output')
plot_10_pareto_3d_front('../results/output')
```

---

## 💾 Export Formats

Each script automatically exports:
- High-Resolution PNG images (`.png`, 300 DPI) for publications and presentations.
- Native MATLAB Figure files (`.fig`) allowing interactive 3D rotation, zooming, and editing.
