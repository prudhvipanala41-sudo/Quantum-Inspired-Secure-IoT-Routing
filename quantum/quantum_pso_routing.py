"""
Quantum-Behaved Delta-Well Swarm Optimization (Q-PSO / QBDW-SO) for Secure IoT Routing.

In contrast to classical Newtonian PSO which tracks explicit velocities and suffers from
premature velocity stagnation in discrete network graphs, Q-PSO models each particle
as a quantum wave packet bound in a 1D delta potential well centered at a local attractor point.
Position evolution is governed by the Schrödinger wave function collapse.
"""

import numpy as np


def quantum_route_cost(route, G, weights=None):
    """
    Computes the Quantum Multi-Objective Hamiltonian Cost of a candidate routing path.
    Cost incorporates:
    - Energy Depletion Index
    - Quantum Trust Trace Fidelity
    - Multi-hop Propagation Delay
    - Geometric Link Distance
    - Malicious Node Security Penalty
    """
    if weights is None:
        weights = {
            "energy": 0.30,
            "distance": 0.20,
            "delay": 0.15,
            "packet_loss": 0.15,
            "security": 0.20,
        }

    intermediate = [n for n in route if n != "BS"]
    if not intermediate:
        return float("inf")

    energies = [G.nodes[n].get("energy", 50.0) for n in intermediate]
    trusts = [G.nodes[n].get("trust", 1.0) for n in intermediate]
    malicious_flags = [G.nodes[n].get("is_malicious", False) for n in intermediate]

    # 1. Energy cost (normalized against 100 max)
    avg_energy = np.mean(energies)
    energy_cost = 1.0 - (avg_energy / 100.0)

    # 2. Geometric path distance
    total_distance = sum(
        G[route[i]][route[i + 1]].get("weight", 10.0) for i in range(len(route) - 1)
    )
    distance_norm = min(total_distance / 200.0, 1.0)

    # 3. Hop delay
    delay_norm = min(len(route) / 10.0, 1.0)

    # 4. Quantum Trust fidelity penalty
    avg_trust = np.mean(trusts)
    packet_loss_risk = 1.0 - avg_trust

    # 5. Security threat penalty
    security_risk = np.mean(malicious_flags) if malicious_flags else 0.0

    cost = (
        weights["energy"] * energy_cost
        + weights["distance"] * distance_norm
        + weights["delay"] * delay_norm
        + weights["packet_loss"] * packet_loss_risk
        + weights["security"] * security_risk
    )
    return float(cost)


def qpso_select_route(candidate_routes, G, weights=None, n_particles=20, n_iterations=30, seed=42):
    """
    Quantum-Behaved Swarm Optimization (Q-PSO) over candidate routes.

    Equations:
        Attractor: P_{i,j} = phi * pbest_{i,j} + (1 - phi) * gbest_j
        Mean Best: C_j = (1/M) * sum_i pbest_{i,j}
        Position:  X_{i,j}(t+1) = P_{i,j} +/- alpha * |C_j - X_{i,j}(t)| * ln(1/u)
    """
    if not candidate_routes:
        return None, None, []

    rng = np.random.default_rng(seed)
    n_routes = len(candidate_routes)

    # Precompute candidate route costs
    costs = np.array([quantum_route_cost(r, G, weights) for r in candidate_routes])

    # Initial particle state preference vectors
    positions = rng.uniform(0.0, 1.0, (n_particles, n_routes))
    personal_best_pos = positions.copy()
    personal_best_cost = np.array([
        costs[np.argmax(positions[i])] for i in range(n_particles)
    ])

    global_best_idx = np.argmin(personal_best_cost)
    global_best_pos = personal_best_pos[global_best_idx].copy()
    global_best_cost = personal_best_cost[global_best_idx]

    alpha_max, alpha_min = 1.0, 0.4
    cost_history = [float(global_best_cost)]

    for t in range(n_iterations):
        # Dynamic quantum contraction-expansion coefficient
        alpha = alpha_max - ((alpha_max - alpha_min) * (t / n_iterations))

        # Compute Mean Best Position (Mbest)
        mbest = np.mean(personal_best_pos, axis=0)

        for i in range(n_particles):
            # Stochastic quantum attractor
            phi = rng.uniform(0.0, 1.0, n_routes)
            p_attr = phi * personal_best_pos[i] + (1.0 - phi) * global_best_pos

            u = rng.uniform(1e-7, 1.0, n_routes)
            sign = rng.choice([-1.0, 1.0], size=n_routes)

            # Quantum delta-potential well wave function collapse
            positions[i] = p_attr + sign * alpha * np.abs(mbest - positions[i]) * np.log(1.0 / u)
            positions[i] = np.clip(positions[i], 0.0, 1.0)

            # Evaluate route cost from collapsed state
            chosen_route_idx = np.argmax(positions[i])
            current_cost = costs[chosen_route_idx]

            # Update personal best
            if current_cost < personal_best_cost[i]:
                personal_best_cost[i] = current_cost
                personal_best_pos[i] = positions[i].copy()

                # Update global best
                if current_cost < global_best_cost:
                    global_best_cost = current_cost
                    global_best_pos = positions[i].copy()

        cost_history.append(float(global_best_cost))

    best_idx = np.argmax(global_best_pos)
    best_route = candidate_routes[best_idx]
    return best_route, float(costs[best_idx]), cost_history


if __name__ == "__main__":
    import networkx as nx

    G = nx.Graph()
    G.add_node(0, energy=90, trust=0.98, is_malicious=False)
    G.add_node(1, energy=85, trust=0.95, is_malicious=False)
    G.add_node(2, energy=20, trust=0.30, is_malicious=True)
    G.add_node("BS", is_bs=True)

    G.add_edge(0, 1, weight=10.0)
    G.add_edge(1, "BS", weight=15.0)
    G.add_edge(0, 2, weight=8.0)
    G.add_edge(2, "BS", weight=8.0)

    candidates = [
        [0, 1, "BS"],  # Secure, high-energy path
        [0, 2, "BS"],  # Short but malicious path
    ]

    best_route, best_cost, hist = qpso_select_route(candidates, G)
    print("=== QUANTUM-BEHAVED SWARM OPTIMIZATION TEST ===")
    print(f"Optimal Quantum Route: {best_route}")
    print(f"Optimal Hamiltonian Cost: {best_cost:.4f}")
    print(f"Convergence history: {[round(h, 4) for h in hist[:5]]} ...")
