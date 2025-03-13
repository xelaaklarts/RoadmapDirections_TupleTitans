import requests
import os

class RoutesClient:
    def __init__(self, API_KEY: str):
        self.API_KEY = API_KEY
        self.url = "https://routes.googleapis.com/directions/v2:computeRoutes"

API_KEY = os.getenv("RoutesAPIKey")  # Replace with actual environment variable name
url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
}

data = {
    "origin": {"location": {"latLng": {"latitude": 37.417670, "longitude": -122.0827784}}},
    "destination": {"location": {"latLng": {"latitude": 37.417670, "longitude": -122.079595}}},
    "travelMode": "DRIVE",
    "routingPreferences": "TRAFFIC_AWARE",
    "computeAlternativeRoutes": True,
    "units": "METRIC",
    "languageCode": "en-US",
    "routeModifiers": {
        "avoidTolls": True, 
        "avoidHighways": False, 
        "avoidFerries": True
    }
}

def get_routes():
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        response.raise_for_status()
        
def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    while index < len(polyline_str):
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0
            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break
            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append((lat / 1e5, lng / 1e5))
    return coordinates

if __name__ == "__main__":
    print(f"API_KEY: {API_KEY}")  # Debugging
    routes = get_routes()
    if routes:
        location = decode_polyline(routes['routes'][0]['polyline']['encodedPolyline'])
        print(location)