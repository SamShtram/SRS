import os
import sys
import json
import math
from fastapi import FastAPI
from pydantic import BaseModel
from geopy.geocoders import Nominatim

# Allow relative imports if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# -----------------------------
# Load shelters JSON
# -----------------------------
SHELTER_FILE = os.path.join("..", "data", "shelters.json")

with open(SHELTER_FILE, "r", encoding="utf-8") as f:
    SHELTERS = json.load(f)


# -----------------------------
# Address → Latitude/Longitude
# -----------------------------
geolocator = Nominatim(user_agent="shelter_finder_app")

def geocode_address(address: str):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None


# -----------------------------
# Haversine Distance (km)
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -----------------------------
# GET /nearest
# Supports:
#   - /nearest?address=Philadelphia
#   - /nearest?lat=39.9&lon=-75.1
# -----------------------------
@app.get("/nearest")
def nearest_shelters(address: str = None, lat: float = None, lon: float = None, limit: int = 10):
    # CASE 1 — Using address
    if address:
        lat, lon = geocode_address(address)
        if lat is None:
            return {"error": "Address not found or could not be geocoded."}

    # CASE 2 — Using coordinates directly
    elif lat is not None and lon is not None:
        lat = float(lat)
        lon = float(lon)

    # CASE 3 — Missing both
    else:
        return {"error": "You must provide either 'address' OR 'lat' and 'lon' parameters."}

    # Compute distances
    results = []
    for s in SHELTERS:
        d = haversine(lat, lon, s["lat"], s["lon"])
        results.append({
            "id": s["id"],
            "name": s["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "capacity": s["capacity"],
            "risk_level": s["risk_level"],
            "distance_km": round(d, 2)
        })

    # Sort by distance
    results.sort(key=lambda x: x["distance_km"])

    return results[:limit]


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def index():
    return {"status": "Shelter Finder API is running."}
