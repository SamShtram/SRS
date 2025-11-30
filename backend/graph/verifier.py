from graph.build_graph import build_graph
from graph.dijkstra import dijkstra
from graph.hazard import apply_hazard_penalties
from graph.capacity import apply_capacity_penalty
import json

def verify():
    graph, nodes, edges = build_graph()

    with open("data/shelters.json", "r") as f:
        shelters = json.load(f)

    hazards = apply_hazard_penalties("flood", edges)
    capacity = apply_capacity_penalty(shelters)

    print("Original edges:")
    for e in edges:
        print(e)

    for e in edges:
        base = e["weight"]
        e["weight"] = base + hazards.get((e["from"], e["to"]), 0)
        e["weight"] += capacity.get((e["from"], e["to"]), 0)

    print("\nEdges after penalties:")
    for e in edges:
        print(e)

    print("\nDijkstra from A:")
    results = dijkstra(graph, "A")
    print(results)

if __name__ == "__main__":
    verify()
