"""
Simulates packet transmission from source nodes to the Base Station
along a chosen route, tracking delivery status, delay, and energy
consumption. Also degrades node energy each round to allow
network-lifetime experiments.
"""

import numpy as np
import pandas as pd


ENERGY_PER_HOP = 0.5      # energy units consumed per hop for the forwarding node
DELAY_PER_HOP_MS = 4.0    # ms of delay per hop


def simulate_packet(route, G, node_lookup, seed=None):
    """
    Simulate a single packet traveling along `route`.

    A packet is dropped if any intermediate (non-source, non-BS) node
    is malicious and "rolls" a drop based on its drop_probability.

    Returns a dict describing the outcome.
    """
    rng = np.random.default_rng(seed)

    delay = 0.0
    energy_used = 0.0
    status = "Delivered"

    intermediate = [n for n in route if n != "BS"]
    for idx, node_id in enumerate(intermediate):
        delay += DELAY_PER_HOP_MS
        energy_used += ENERGY_PER_HOP

        row = node_lookup.get(node_id)
        if row is not None and row.get("is_malicious", False):
            drop_p = row.get("drop_probability", 0.0)
            if rng.random() < drop_p:
                status = "Dropped"
                break

    return {
        "source": route[0],
        "destination": "BS",
        "route": "->".join(str(n) for n in route),
        "status": status,
        "delay_ms": round(delay, 2),
        "energy_used": round(energy_used, 4),
        "hops": len(route) - 1,
    }


def run_packet_simulation(df, G, route_selector, n_packets=1000, seed=42):
    """
    Generate n_packets, each from a random source node, routed via
    route_selector(source, G) -> route (list of node ids incl. "BS").

    route_selector should be a function like:
        lambda src, G: pso_select_route(k_shortest_paths(G, src), G)[0]

    Returns a DataFrame of packet-level results.
    """
    rng = np.random.default_rng(seed)
    node_lookup = df.set_index("node_id").to_dict("index")

    node_ids = df["node_id"].tolist()
    results = []
    route_cache = {}

    for i in range(n_packets):
        src = int(rng.choice(node_ids))
        if src not in route_cache:
            route_cache[src] = route_selector(src, G)
        route = route_cache[src]

        if not route:
            results.append({
                "source": src, "destination": "BS", "route": "",
                "status": "No Route", "delay_ms": 0, "energy_used": 0, "hops": 0,
            })
            continue

        outcome = simulate_packet(route, G, node_lookup, seed=seed + i)
        results.append(outcome)

    return pd.DataFrame(results)


def apply_energy_drain(df, packet_df):
    """
    After a simulation round, subtract energy consumed from each node
    that appeared as an intermediate hop in any route.
    Returns updated df with reduced 'energy' column.
    """
    df = df.copy()
    drain = {nid: 0.0 for nid in df["node_id"]}

    for _, row in packet_df.iterrows():
        if not row["route"]:
            continue
        hops = [h for h in row["route"].split("->") if h != "BS"]
        per_hop_energy = row["energy_used"] / max(len(hops), 1)
        for h in hops:
            nid = int(h)
            if nid in drain:
                drain[nid] += per_hop_energy

    df["energy"] = df.apply(
        lambda r: max(0.0, r["energy"] - drain.get(r["node_id"], 0.0)), axis=1
    )
    return df


if __name__ == "__main__":
    from simulation.network import build_network_graph, ensure_connected
    from algorithms.shortest_path import k_shortest_paths, dijkstra_route

    df = pd.read_csv("data/nodes.csv")
    G = build_network_graph(df)
    G = ensure_connected(G, df)

    def dijkstra_selector(src, G):
        path, _ = dijkstra_route(G, src)
        return path

    packets = run_packet_simulation(df, G, dijkstra_selector, n_packets=200)
    print(packets["status"].value_counts())
    print(f"\nAverage delay: {packets['delay_ms'].mean():.2f} ms")
    packets.to_csv("data/results.csv", index=False)
