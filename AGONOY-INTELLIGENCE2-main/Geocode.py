from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivy_garden.mapview import MapView, MapMarker, MapLayer
from kivy.graphics import Color, Line
import requests

KV = """
BoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Campus Map Search"
        elevation: 10

    MDTextField:
        id: search_field
        hint_text: "Search for a building..."
        mode: "rectangle"
        size_hint_x: 0.9
        pos_hint: {"center_x": 0.5}
        on_text_validate: app.search_place(self.text)

    MapView:
        id: mapview
        lat: 16.93804   # ISU Cauayan campus center
        lon: 121.76454
        zoom: 15
"""

class PolylineLayer(MapLayer):
    def __init__(self, points, **kwargs):
        super().__init__(**kwargs)
        self.points = points

    def reposition(self):
        mapview = self.parent
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0, 1)  # red line
            line_points = []
            for lat, lon in self.points:
                x, y = mapview.get_window_xy_from(lat, lon, mapview.zoom)
                line_points.extend([x, y])
            if line_points:
                Line(points=line_points, width=2)

class CampusMapApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def search_place(self, query):
        """Search for building/place using OpenStreetMap (Nominatim)."""
        url = f"https://nominatim.openstreetmap.org/search"
        params = {"q": query + " ISU Cauayan", "format": "json", "limit": 1}
        try:
            r = requests.get(url, params=params, headers={"User-Agent": "KivyApp"}).json()
            if not r:
                Snackbar(text="Place not found").open()
                return

            place = r[0]
            lat, lon = float(place["lat"]), float(place["lon"])

            # Add marker for search result
            mapview = self.root.ids.mapview
            mapview.add_widget(MapMarker(lat=lat, lon=lon))

            # Assume fixed "your location" (replace with GPS later)
            start_lat, start_lon = 16.9340, 121.7600  # e.g., Cauayan city proper

            # Fetch route
            coords = self.get_route(start_lat, start_lon, lat, lon)
            if coords:
                mapview.add_layer(PolylineLayer(coords))
                Snackbar(text=f"Shortest path to {query} displayed").open()
            else:
                Snackbar(text="Could not fetch route").open()

        except Exception as e:
            print("Search error:", e)
            Snackbar(text="Error while searching").open()

    def get_route(self, start_lat, start_lon, end_lat, end_lon):
        """Fetch shortest route from OSRM API."""
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
        try:
            response = requests.get(url).json()
            coords = response["routes"][0]["geometry"]["coordinates"]
            return [(lat, lon) for lon, lat in coords]
        except Exception as e:
            print("Route error:", e)
            return []

if __name__ == "__main__":
    CampusMapApp().run()
