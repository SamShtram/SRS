import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from pydantic import BaseModel
from graph.build_graph import build_graph
from graph.dijkstra import dijkstra
from graph.hazard import apply_hazard_penalties
from graph.capacity import apply_capacity_penalty
import json

app = FastAPI()

# Load shelter data once on startup
with open("data/shelters.json", "r") as f:
    SHELTERS = json.load(f)


class RequestInput(BaseModel):
    user_location: str
    crisis_type: str   # "flood" | "wildfire" | "hurricane" | etc.


@app.post("/recommend")
def recommend_shelters(data: RequestInput):
    graph, nodes, edges = build_graph()

    hazard_penalties = apply_hazard_penalties(data.crisis_type, edges)
    capacity_penalties = apply_capacity_penalty(SHELTERS)

    for edge in edges:
        edge_id = (edge["from"], edge["to"])
        base = edge["weight"]
        hazard = hazard_penalties.get(edge_id, 0)
        capacity = capacity_penalties.get(edge_id, 0)
        edge["weight"] = base + hazard + capacity

    results = dijkstra(graph, data.user_location)

    ranked = []
    for shelter in SHELTERS:
        sid = shelter["id"]
        if sid in results:
            ranked.append({
                "shelter_id": sid,
                "name": shelter["name"],
                "location": shelter["location"],
                "capacity": shelter["capacity"],
                "risk_level": shelter["risk_level"],
                "cost": results[sid]
            })

    ranked.sort(key=lambda x: x["cost"])

    return {
        "status": "success",
        "user_location": data.user_location,
        "crisis_type": data.crisis_type,
        "ranked_shelters": ranked
    }
