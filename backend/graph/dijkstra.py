import heapq

def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    dist[start] = 0

    pq = [(0, start)]

    while pq:
        current_cost, node = heapq.heappop(pq)

        if current_cost > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_cost = current_cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return dist
