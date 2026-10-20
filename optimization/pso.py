"""
Particle Swarm Optimization for secure, energy-efficient route
selection among a set of candidate routes.

Since routes are discrete objects (sequences of node IDs), we apply
PSO over the *objective weight space* is unnecessary here -- instead
we use a simpler and more transportable approach for a discrete
candidate set: PSO particles represent a soft "preference vector"
over candidate routes, which converges to selecting the
lowest-cost route. This keeps the true multi-objective PSO spirit
(swarm search minimizing a weighted cost function) while remaining
well-defined over the discrete route set produced by k_shortest_paths.
"""

import numpy as np


def route_cost(route, G, weights=None):
    """
    Compute the weighted multi-objective cost of a route.

    Cost = w1*energy_cost + w2*distance + w3*delay + w4*packet_loss_risk + w5*security_risk

    - energy_cost: inverse of average remaining energy along the route (lower energy = higher cost)
    - distance: total path distance (sum of edge weights)
    - delay: proportional to hop count (each hop ~ fixed delay unit)
    - packet_loss_risk: inverse of average trust along intermediate nodes
    - security_risk: fraction of intermediate nodes flagged malicious
    """
    if weights is None:
        weights = {"energy": 0.30, "distance": 0.20, "delay": 0.15,
                   "packet_loss": 0.15, "security": 0.20}

    intermediate = [n for n in route if n != "BS"]
    if not intermediate:
        return float("inf")

    energies = [G.nodes[n].get("energy", 50) for n in intermediate]
    trusts = [G.nodes[n].get("trust", 1.0) for n in intermediate]
    malicious_flags = [G.nodes[n].get("is_malicious", False) for n in intermediate]

    avg_energy = np.mean(energies)
    energy_cost = 1 - (avg_energy / 100)  # low energy -> high cost

    total_distance = sum(
        G[route[i]][route[i + 1]]["weight"] for i in range(len(route) - 1)
    )
    # normalize distance roughly against a typical max path length
    distance_norm = min(total_distance / 200, 1.0)

    delay_norm = min(len(route) / 10, 1.0)  # more hops -> more delay

    avg_trust = np.mean(trusts)
    packet_loss_risk = 1 - avg_trust

    security_risk = np.mean(malicious_flags) if malicious_flags else 0.0

    cost = (
        weights["energy"] * energy_cost
        + weights["distance"] * distance_norm
        + weights["delay"] * delay_norm
        + weights["packet_loss"] * packet_loss_risk
        + weights["security"] * security_risk
    )
    return cost


def pso_select_route(candidate_routes, G, weights=None, n_particles=20, n_iterations=30, seed=42):
    """
    Runs a PSO search over the candidate route set. Each particle
    holds a continuous "preference score" per candidate route;
    the particle's chosen route is argmax(preference). Particles
    are pulled toward the best-known route (global best) and their
    own best each iteration, mimicking classic PSO dynamics, while
    always evaluating true route cost via route_cost().

    Returns (best_route, best_cost, cost_history)
    """
    if not candidate_routes:
        return None, None, []

    rng = np.random.default_rng(seed)
    n_routes = len(candidate_routes)

    # Precompute true cost for each candidate (deterministic cost function)
    costs = np.array([route_cost(r, G, weights) for r in candidate_routes])

    # Particle positions = preference vector over routes
    positions = rng.uniform(0, 1, (n_particles, n_routes))
    velocities = rng.uniform(-0.1, 0.1, (n_particles, n_routes))

    personal_best_pos = positions.copy()
    personal_best_cost = np.array([
        costs[np.argmax(positions[i])] for i in range(n_particles)
    ])

    global_best_idx = np.argmin(personal_best_cost)
    global_best_pos = personal_best_pos[global_best_idx].copy()
    global_best_cost = personal_best_cost[global_best_idx]

    w, c1, c2 = 0.6, 1.4, 1.4  # inertia, cognitive, social coefficients
    cost_history = [global_best_cost]

    for _ in range(n_iterations):
        r1 = rng.uniform(0, 1, (n_particles, n_routes))
        r2 = rng.uniform(0, 1, (n_particles, n_routes))

        velocities = (
            w * velocities
            + c1 * r1 * (personal_best_pos - positions)
            + c2 * r2 * (global_best_pos - positions)
        )
        positions = positions + velocities
        positions = np.clip(positions, 0, 1)

        chosen_idx = np.argmax(positions, axis=1)
        current_costs = costs[chosen_idx]

        improved = current_costs < personal_best_cost
        personal_best_cost[improved] = current_costs[improved]
        personal_best_pos[improved] = positions[improved]

        best_particle = np.argmin(personal_best_cost)
        if personal_best_cost[best_particle] < global_best_cost:
            global_best_cost = personal_best_cost[best_particle]
            global_best_pos = personal_best_pos[best_particle].copy()

        cost_history.append(global_best_cost)

    best_route_idx = np.argmax(global_best_pos)
    best_route = candidate_routes[best_route_idx]

    return best_route, costs[best_route_idx], cost_history


if __name__ == "__main__":
    import pandas as pd
    from simulation.network import build_network_graph, ensure_connected
    from algorithms.shortest_path import k_shortest_paths

    df = pd.read_csv("data/nodes.csv")
    G = build_network_graph(df)
    G = ensure_connected(G, df)

    src = int(df["node_id"].iloc[0])
    candidates = k_shortest_paths(G, src, k=5)

    best_route, best_cost, history = pso_select_route(candidates, G)
    print(f"PSO best route from {src}: {best_route}")
    print(f"Cost: {best_cost:.4f}")
