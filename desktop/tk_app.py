import tkinter as tk
from tkinter import ttk
import tkintermapview
import requests

BACKEND = "http://127.0.0.1:8000"

class ShelterFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shelter Finder Desktop App")
        self.root.geometry("1200x800")
        self.user_marker = None

        # ---------- TOP BAR ----------
        top = ttk.Frame(root)
        top.pack(fill="x", padx=10, pady=10)

        self.address_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.address_var, width=50).pack(side="left", padx=5)
        ttk.Button(top, text="Search", command=self.search_address).pack(side="left", padx=5)
        ttk.Button(top, text="Use My Location", command=self.use_my_location).pack(side="left", padx=5)

        # ---------- SIDEBAR ----------
        self.results = tk.Listbox(root, width=40)
        self.results.pack(side="right", fill="y", padx=10, pady=10)

        # ---------- MAP ----------
        self.map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
        self.map_widget.pack(side="left", fill="both", expand=True)

        self.map_widget.set_position(40.0, -75.0)
        self.map_widget.set_zoom(6)

        self.shelter_markers = []
        self.route_line = None

    # ---------------------------------------------------------
    def clear_markers(self):
        for m in self.shelter_markers:
            m.delete()
        self.shelter_markers = []

        if self.route_line:
            self.route_line.delete()
            self.route_line = None

    # ---------------------------------------------------------
    def search_address(self):
        address = self.address_var.get()
        if not address:
            return

        res = requests.get(f"{BACKEND}/nearest", params={"address": address})
        shelters = res.json()
        print(shelters)

        self.display_results(shelters)

        # Center map 
        first = shelters[0]
        self.map_widget.set_position(first["lat"], first["lon"])
        self.map_widget.set_zoom(13)

        self.place_markers(shelters)

    # ---------------------------------------------------------
    def use_my_location(self):
        ip = requests.get("http://ip-api.com/json/").json()
        lat, lon = ip["lat"], ip["lon"]

    # Place user marker
        self.set_user_marker(lat, lon)

    # Move map to user
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(13)

    # Get shelters near user
        res = requests.get(f"{BACKEND}/nearest", params={"lat": lat, "lon": lon})
        shelters = res.json()

        self.display_results(shelters)
        self.place_markers(shelters)

    # ---------------------------------------------------------
    def display_results(self, shelters):
        self.results.delete(0, tk.END)
        self.shelters = shelters

        for s in shelters:
            txt = f"{s['name']} — {s['distance_km']} km"
            self.results.insert(tk.END, txt)

        self.results.bind("<<ListboxSelect>>", self.on_shelter_click)

    # ---------------------------------------------------------
    def place_markers(self, shelters):
        self.clear_markers()

        for s in shelters:
            marker = self.map_widget.set_marker(s["lat"], s["lon"], text=s["name"])
            self.shelter_markers.append(marker)

    # ---------------------------------------------------------
    def on_shelter_click(self, event):
        if not self.results.curselection():
            return

        index = self.results.curselection()[0]
        shelter = self.shelters[index]

        # Center on the shelter
        self.map_widget.set_position(shelter["lat"], shelter["lon"])
        self.map_widget.set_zoom(15)

        # Draw a route from user location (if known)
        try:
            ip = requests.get("http://ip-api.com/json/").json()
            my_lat, my_lon = ip["lat"], ip["lon"]

            if self.route_line:
                self.route_line.delete()

            self.route_line = self.map_widget.set_path([
                (my_lat, my_lon),
                (shelter["lat"], shelter["lon"])
            ])
        except:
            pass
    # -----------------------------------------------------
    def set_user_marker(self, lat, lon):
        if self.user_marker:
            self.user_marker.delete()

        self.user_marker = self.map_widget.set_marker(
            lat,
            lon,
            text="You Are Here",
            marker_color_circle="blue",
            marker_color_outside="white"
    )



# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ShelterFinderApp(root)
    root.mainloop()
