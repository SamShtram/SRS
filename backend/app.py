import os
import sys
import json
import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from geopy.geocoders import Nominatim

# Allow relative imports if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# -----------------------------
# Enable CORS so frontend can call backend
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load shelters JSON
# -----------------------------
SHELTER_FILE = os.path.join("..", "data", "shelters.json")

with open(SHELTER_FILE, "r", encoding="utf-8") as f:
    SHELTERS = json.load(f)

# -----------------------------
# Geocoder
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
# Haversine Distance Formula
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -----------------------------
# /nearest — supports:
# ?address=city OR ?lat=xx&lon=yy
# -----------------------------
@app.get("/nearest")
def nearest_shelters(address: str = None, lat: float = None, lon: float = None, limit: int = 10):

    # CASE 1 — Address search
    if address:
        lat, lon = geocode_address(address)
        if lat is None:
            return {"error": "Address not found or could not be geocoded."}

    # CASE 2 — Coordinates provided by browser geolocation
    elif lat is not None and lon is not None:
        lat = float(lat)
        lon = float(lon)

    # CASE 3 — Nothing provided
    else:
        return {"error": "You must provide either address= or lat= & lon= parameters."}

    # Compute distances to every shelter
    results = []
    for s in SHELTERS:
        distance = haversine(lat, lon, s["lat"], s["lon"])
        results.append({
            "id": s["id"],
            "name": s["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "capacity": s["capacity"],
            "risk_level": s["risk_level"],
            "distance_km": round(distance, 2)
        })

    # Sort by nearest first
    results.sort(key=lambda x: x["distance_km"])

    return results[:limit]


@app.get("/")
def index():
    return {"status": "Shelter Finder API running"}
