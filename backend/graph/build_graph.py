def build_graph():
    nodes = ["A", "B", "C", "S1", "S2", "S3"]

    edges = [
        {"from": "A", "to": "B", "weight": 3},
        {"from": "B", "to": "C", "weight": 4},
        {"from": "C", "to": "S1", "weight": 2},
        {"from": "B", "to": "S2", "weight": 5},
        {"from": "A", "to": "S3", "weight": 10}
    ]

    graph = {node: [] for node in nodes}
    for edge in edges:
        graph[edge["from"]].append((edge["to"], edge["weight"]))

    return graph, nodes, edges
