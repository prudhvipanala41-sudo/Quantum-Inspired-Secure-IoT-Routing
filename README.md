# ⚛️ Quantum-Enhanced Secure Cluster-Based Routing & Optimization Framework for Heterogeneous IoT Networks

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Patent Ready](https://img.shields.io/badge/Patent_Filing-20_Claims_Drafted-green.svg)](data/patent_specification.md)
[![Quantum Framework](https://img.shields.io/badge/Quantum_Engine-QSAHE%20%7C%20QSE--FCM%20%7C%20Q--PSO-purple.svg)]()
[![Scale](https://img.shields.io/badge/Scale-1000_Nodes_%7C_500_Active-blueviolet.svg)]()
[![Graphs](https://img.shields.io/badge/Results-10_Publication_Graphs-brightgreen.svg)]()
[![Streamlit UI](https://img.shields.io/badge/Dashboard-Cyber_Quantum_UI-00f2fe.svg)]()

## 📌 Project Overview

This project presents a complete software-simulated **Quantum-Enhanced Secure Cluster-Based Routing and Optimization Framework for heterogeneous IoT networks**.

The system is designed to improve:

- IoT node clustering
- Cluster-head selection
- Secure routing
- Malicious-node detection
- Packet delivery
- Energy efficiency
- Network lifetime
- Routing optimization

The framework combines **quantum-inspired computation, machine learning, trust-based security, clustering algorithms, and routing optimization** within a single IoT simulation environment.

The complete network is configured for:

- **1000 total IoT nodes**
- **500 active/sample nodes during execution**
- Multiple cluster heads
- Malicious nodes
- Multi-hop communication
- Base-station communication
- Quantum-inspired clustering and routing
- Trust-based malicious-node filtering

The system also automatically produces a complete suite of **10 publication-quality result graphs** for experimental analysis.

---

# 🎯 Main Objective

The main objective of the project is to design a secure and energy-efficient IoT routing framework capable of selecting reliable cluster heads and routing packets through trustworthy nodes while avoiding malicious devices.

The proposed system combines:

**Quantum-inspired clustering → ML/Quantum Cluster-Head Selection → Trust Evaluation → Malicious-Node Detection → Quantum Routing Optimization → Packet Transmission → Performance Evaluation**

The framework attempts to improve overall IoT network performance in terms of:

- Packet Delivery Ratio
- Packet Loss Ratio
- End-to-End Delay
- Residual Energy
- Network Lifetime
- Routing Cost
- Malicious-Node Detection
- Cluster Quality
- Trustworthiness
- Energy Consumption

---

# 🏗️ Complete System Workflow

The execution of the framework follows the sequence below.

```text
IoT Node Generation
        ↓
Quantum Feature Representation
        ↓
Quantum-Based Clustering
        ↓
Cluster-Head Selection
        ↓
Trust Evaluation
        ↓
Malicious Node Detection
        ↓
Secure Route Discovery
        ↓
Quantum-Behaved PSO Routing Optimization
        ↓
Packet Transmission
        ↓
Energy Consumption Update
        ↓
Network Performance Evaluation
        ↓
Result Graph Generation
```

---

# 1️⃣ IoT Network Generation

The simulation begins by generating a heterogeneous IoT network containing **1000 virtual IoT nodes**.

Each IoT node contains several characteristics such as:

- X-coordinate
- Y-coordinate
- Initial energy
- Residual energy
- Distance from base station
- Trust value
- Packet-forwarding behavior
- Cluster assignment
- Cluster-head status
- Malicious/normal status

For efficient simulation, **500 nodes may be selected as active execution nodes** from the complete 1000-node network.

The main implementation is available in:

```text
simulation/node_generator.py
```

---

# 2️⃣ Quantum State Amplitude Hilbert Embedding — QSAHE

The classical IoT node information is transformed into a quantum-inspired state representation.

For node \(i\):

\[
\mathbf{x}_i =
[p_x,p_y,E,T,d_{bs}]^T
\]

where:

- \(p_x\) = X position
- \(p_y\) = Y position
- \(E\) = residual energy
- \(T\) = trust score
- \(d_{bs}\) = distance to base station

The node feature vector is normalized and mapped into a quantum state:

\[
|\psi(\mathbf{x}_i)\rangle
\]

The corresponding density matrix is calculated as:

\[
\rho_i =
|\psi_i\rangle
\langle\psi_i|
\]

This representation allows quantum-inspired similarity and fidelity measurements to be applied during clustering and trust analysis.

Implementation:

```text
quantum/quantum_embeddings.py
```

---

# 3️⃣ Quantum-Based IoT Clustering

Two main quantum-inspired clustering techniques are incorporated into the framework.

## Quantum Density-Matrix Fidelity K-Means — QDF-KMeans

Instead of using only classical Euclidean distance, the algorithm measures similarity between quantum state representations.

Cluster membership is determined using quantum-state fidelity.

This allows nodes with similar:

- Location
- Energy
- Trust
- Base-station distance
- Network behavior

to be grouped into suitable clusters.

## Quantum Superposition Entropic Fuzzy C-Means — QSE-FCM

QSE-FCM provides fuzzy cluster membership rather than assigning every node completely to a single cluster.

Quantum overlap state fidelity is used:

\[
D_Q(\psi_i,\phi_j)
=
1-
|\langle\psi_i|\phi_j\rangle|^2
\]

The algorithm also incorporates:

- Quantum fidelity
- Fuzzy memberships
- Von Neumann entropy
- Quantum coherence
- Quantum-inspired barrier tunneling

These techniques are intended to reduce local-optimum problems during cluster formation.

Implementation:

```text
quantum/quantum_clustering.py
```

---

# 4️⃣ Cluster-Head Selection

After forming clusters, suitable nodes must be selected as **Cluster Heads (CHs)**.

Cluster heads perform additional responsibilities such as:

- Collecting packets from member nodes
- Aggregating data
- Forwarding traffic
- Participating in routing
- Communicating with other cluster heads
- Forwarding information toward the base station

Cluster-head selection considers properties such as:

- Residual energy
- Trust score
- Distance
- Cluster position
- Connectivity
- Node stability

Two methods are supported.

## Classical Machine-Learning Selection

A Random Forest model can be used to determine whether a node is suitable to become a cluster head.

Implementation:

```text
ml/train_model.py
ml/predict_cluster_head.py
```

## Parameterized Quantum Variational Classifier — PQ-VQC

The proposed framework also incorporates a simulated **4-qubit Parameterized Quantum Circuit**.

The circuit uses:

- Hadamard gates
- \(R_y(\theta)\) rotations
- \(R_z(\phi)\) rotations
- Circular CNOT entanglement
- Pauli-Z expectation measurements

The quantum measurement:

\[
\langle
Z_0 \otimes
Z_1 \otimes
Z_2 \otimes
Z_3
\rangle
\]

is used as part of the cluster-head decision process.

Implementation:

```text
quantum/quantum_vqc_ch.py
```

---

# 5️⃣ Malicious Node Simulation

The IoT network supports malicious-node behavior so that the proposed security framework can be evaluated under attack conditions.

The system can simulate attacks such as:

### Blackhole Attack

A malicious node receives packets but intentionally drops them instead of forwarding them toward the destination.

### Grayhole Attack

A malicious node selectively drops packets, making the attack more difficult to detect.

### Sybil-Type Suspicious Behavior

Nodes may exhibit identity or behavior patterns inconsistent with legitimate network activity.

Attack implementation:

```text
security/attack.py
```

---

# 6️⃣ Quantum Trust Estimation

To prevent malicious nodes from participating in secure routes, every node is assigned a trust value.

The proposed **Quantum Density Matrix Trace Fidelity Trust Estimator (QDMTF-TE)** evaluates node forwarding behavior through a quantum-inspired representation.

The system uses concepts such as:

- Density matrices
- State fidelity
- Trace distance
- Quantum state purity
- Successful forwarding behavior
- Packet-drop behavior

Quantum-state purity is calculated as:

\[
\gamma =
\text{Tr}(\rho^2)
\]

Trace distance between a node state and trustworthy reference state is also evaluated.

Nodes with low trust scores can be classified as suspicious or malicious and removed from route selection.

Implementation:

```text
quantum/quantum_trust.py
security/trust.py
security/detection.py
```

---

# 7️⃣ Secure Route Discovery

After malicious nodes have been identified, the framework creates candidate routes between cluster heads and the base station.

Candidate paths may be generated using classical graph techniques such as:

- Dijkstra shortest path
- k-shortest paths
- Network connectivity graphs

Implementation:

```text
algorithms/shortest_path.py
simulation/network.py
```

The secure routing module attempts to avoid:

- Malicious nodes
- Low-energy nodes
- Untrustworthy nodes
- Excessively long paths
- High-delay paths

---

# 8️⃣ Quantum-Behaved Particle Swarm Routing — Q-PSO

The proposed framework uses **Quantum-Behaved Particle Swarm Optimization** to optimize route selection.

Unlike classical PSO, Q-PSO does not rely on the traditional particle velocity equation.

Instead, particle positions are updated using a quantum-inspired delta-potential-well model.

\[
X_{i,j}(t+1)
=
P_{i,j}(t)
\pm
\alpha(t)
|C_j(t)-X_{i,j}(t)|
\ln
\left(
\frac{1}{u}
\right)
\]

The routing optimization considers multiple objectives such as:

- Residual energy
- End-to-end delay
- Route distance
- Trust
- Threat risk
- Hop count
- Routing cost

This helps select routes that provide a suitable balance between energy efficiency, security, and network performance.

Implementation:

```text
quantum/quantum_pso_routing.py
```

Classical PSO is also available for benchmarking:

```text
optimization/pso.py
```

---

# 9️⃣ Packet Transmission Simulation

Once the secure route is selected, the simulation transmits packets through the IoT network.

For every transmission, the framework evaluates:

- Packet forwarding
- Packet drops
- Energy consumption
- Transmission delay
- Route availability
- Malicious-node involvement
- Successful packet reception

Energy levels are updated after transmission so that long-term network behavior and network lifetime can be evaluated.

Implementation:

```text
simulation/packet_simulation.py
```

---

# 🔟 Performance Evaluation

After packet transmission, the framework calculates important IoT networking metrics.

## Packet Delivery Ratio

\[
PDR =
\frac{\text{Successfully Delivered Packets}}
{\text{Total Packets Sent}}
\times 100
\]

Higher PDR indicates better routing reliability.

---

## Packet Loss Ratio

\[
PLR =
\frac{\text{Lost Packets}}
{\text{Total Packets Sent}}
\times 100
\]

Lower packet loss indicates better routing and security performance.

---

## Average End-to-End Delay

Measures the average time required for a packet to travel from the source node to its destination or base station.

---

## Residual Energy

Measures how much energy remains in the IoT nodes after communication.

Higher remaining energy indicates more energy-efficient routing.

---

## Network Lifetime

Represents how long the network remains operational before large numbers of nodes exhaust their energy.

---

## Malicious-Node Detection

Security performance is evaluated using:

- Accuracy
- Precision
- Recall
- F1-score

---

# 📊 Benchmark Paradigms

The software currently supports five routing and clustering configurations.

| Paradigm | Clustering Engine | Cluster Head Election | Routing Engine | Security Trust |
|---|---|---|---|---|
| **1. LEACH Baseline** | Spatial Random | Energy-Weighted Random | Dijkstra Shortest Path | None |
| **2. LEACH + PSO** | Spatial Random | Energy-Weighted Random | Classical PSO | None |
| **3. Proposed Classical** | Classical K-Means | Random Forest ML | Classical PSO | Classical Trust |
| **4. Quantum-Inspired** | Quantum Fidelity K-Means | Parameterized VQC | Quantum Q-PSO | Quantum Trace Fidelity |
| **5. Full Quantum Superposition** | QSE-FCM | Parameterized VQC | Quantum Q-PSO | Quantum Density Matrix |

These configurations allow different components of the proposed architecture to be evaluated independently.

---

# 📈 Publication-Quality Result Graphs

Running the complete framework generates **10 high-resolution graphs** stored inside:

```text
results/output/
```

## 1. Network Topology

```text
1_network_topology.png
```

Displays:

- IoT nodes
- Clusters
- Cluster heads
- Malicious nodes
- Base station
- Network distribution

---

## 2. Packet Delivery Ratio

```text
2_pdr_comparison.png
```

Compares PDR between supported routing paradigms.

---

## 3. Average Delay

```text
3_latency_delay_comparison.png
```

Shows average end-to-end packet transmission delay.

---

## 4. Residual Energy

```text
4_energy_residual_distribution.png
```

Displays residual node energy and network depletion characteristics.

---

## 5. Packet Loss and Throughput

```text
5_packet_loss_throughput.png
```

Evaluates packet loss and successful throughput under attack conditions.

---

## 6. Quantum Trust and Purity

```text
6_quantum_trust_purity_scatter.png
```

Shows the relationship between:

\[
\gamma = \text{Tr}(\rho^2)
\]

and quantum trust values.

---

## 7. Malicious-Node Detection

```text
7_security_detection_matrix.png
```

Displays:

- Accuracy
- Precision
- Recall
- F1-score

---

## 8. Q-PSO Convergence

```text
8_qpso_convergence_curve.png
```

Shows convergence behavior of Quantum-Behaved PSO against classical PSO.

---

## 9. Clustering Performance

```text
9_clustering_evaluation_metrics.png
```

Evaluates clustering performance using metrics including:

- Silhouette score
- Quantum coherence
- Cluster quality

---

## 10. Routing Pareto Front

```text
10_pareto_routing_tradeoff.png
```

Illustrates routing trade-offs between:

- Energy
- Delay
- Distance
- Security risk

---

# 🖥️ Streamlit Dashboard

The project contains an interactive dashboard for visualizing the simulation results.

Run:

```bash
streamlit run dashboard/app.py
```

The dashboard provides access to:

- Network topology
- Routing metrics
- Security results
- Quantum trust analysis
- Cluster information
- Q-PSO convergence
- Result graphs
- Performance comparisons

Dashboard implementation:

```text
dashboard/app.py
```

---

# 📜 Patent Specification Module

The project also contains a patent-document generation module.

The specification contains:

- Field of invention
- Background
- System architecture
- Mathematical methodology
- Quantum clustering
- Cluster-head election
- Trust evaluation
- Secure routing
- Industrial applicability
- Independent claims
- Dependent claims

A **20-claim patent specification** can be generated and stored as:

```text
data/patent_specification.md
```

Patent generation module:

```text
patent/patent_spec.py
```

---

# 📁 Complete Project Architecture

```text
secure-iot-routing/
│
├── algorithms/
│   ├── leach.py
│   └── shortest_path.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── patent_specification.md
│
├── matlab/
│
├── ml/
│   ├── generate_dataset.py
│   ├── train_model.py
│   └── predict_cluster_head.py
│
├── models/
│
├── optimization/
│   └── pso.py
│
├── patent/
│   └── patent_spec.py
│
├── quantum/
│   ├── quantum_embeddings.py
│   ├── quantum_clustering.py
│   ├── quantum_vqc_ch.py
│   ├── quantum_pso_routing.py
│   └── quantum_trust.py
│
├── results/
│   ├── metrics.py
│   ├── graphs.py
│   └── output/
│
├── security/
│   ├── attack.py
│   ├── trust.py
│   └── detection.py
│
├── simulation/
│   ├── node_generator.py
│   ├── clustering.py
│   ├── network.py
│   └── packet_simulation.py
│
├── main.py
├── pipeline.py
├── README.md
└── requirements.txt
```

---

# ⚙️ Technology Stack

The project mainly uses:

- Python 3.10+
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- SciPy
- NetworkX
- Streamlit

The framework combines ideas from:

- Internet of Things
- Wireless Sensor Networks
- Quantum Computing
- Quantum-Inspired Optimization
- Machine Learning
- Network Security
- Trust Management
- Cluster-Based Routing
- Swarm Intelligence

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Aneela-abc/Quantum-Inspired-Secure-IoT-Routing.git
```

Move into the project directory:

```bash
cd Quantum-Inspired-Secure-IoT-Routing
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Complete Project

Run:

```bash
python main.py
```

This executes the complete workflow including:

```text
Node Generation
      ↓
Quantum Feature Encoding
      ↓
Clustering
      ↓
Cluster-Head Selection
      ↓
Attack Simulation
      ↓
Trust Evaluation
      ↓
Malicious-Node Detection
      ↓
Secure Route Discovery
      ↓
Q-PSO Route Optimization
      ↓
Packet Transmission
      ↓
Performance Calculation
      ↓
Graph Generation
```

Generated outputs are stored inside:

```text
results/output/
```

---

# 🌐 Running the Dashboard

Use:

```bash
streamlit run dashboard/app.py
```

Streamlit will display a local URL such as:

```text
http://localhost:8501
```

Open it in your browser to explore the project results.

---

# 🔬 Main Research Contributions

The major contributions of the proposed framework are:

1. Quantum-state representation of heterogeneous IoT node characteristics.

2. Quantum fidelity-based IoT clustering.

3. Quantum Superposition Entropic Fuzzy C-Means clustering.

4. Parameterized Quantum Variational Classifier for cluster-head selection.

5. Quantum density-matrix-based trust evaluation.

6. Detection and avoidance of malicious IoT nodes.

7. Quantum-Behaved Particle Swarm Optimization for secure routing.

8. Multi-objective routing based on energy, delay, distance, trust, and threat risk.

9. Simulation of blackhole and grayhole attacks.

10. Integrated visualization and evaluation framework for IoT security and routing.

---

# 📌 Project Summary

The proposed framework integrates:

```text
1000 IoT Nodes
      +
Quantum State Encoding
      +
Quantum Clustering
      +
Quantum/ML Cluster-Head Selection
      +
Malicious Node Detection
      +
Quantum Trust Estimation
      +
Quantum-Behaved PSO
      +
Secure Multi-Hop Routing
      +
Energy-Aware Packet Simulation
      +
Performance Evaluation
```

The complete framework provides a unified environment for studying how **quantum-inspired clustering, optimization, and trust mechanisms can improve the security and efficiency of large-scale heterogeneous IoT routing networks**.

---


# 📄 License / Academic Use

This repository has been developed as part of an academic research and final year project.

The implementation may be used for:

- Academic demonstrations
- IoT networking research
- Quantum-inspired optimization experiments
- Security research
- Performance benchmarking
- Research paper development
