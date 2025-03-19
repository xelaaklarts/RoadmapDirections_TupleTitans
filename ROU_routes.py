# import requests
# import os

# class RoutesClient:
#     def __init__(self, API_KEY: str):
#         self.API_KEY = API_KEY
#         self.url = "https://routes.googleapis.com/directions/v2:computeRoutes"

# API_KEY = os.getenv("API_KEY")  # Replace with actual environment variable name
# url = "https://routes.googleapis.com/directions/v2:computeRoutes"

# def get_routes(start, dest):
#     headers = {
#     "Content-Type": "application/json",
#     "X-Goog-Api-Key": API_KEY,
#     "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
#     }

#     data = {
#         "origin": {"location": {"latLng": {"latitude": start[0], "longitude": start[1]}}},
#         "destination": {"location": {"latLng": {"latitude": dest[0], "longitude": dest[1]}}},
#         "travelMode": "DRIVE",
#         "routingPreferences": "TRAFFIC_AWARE",
#         "computeAlternativeRoutes": True,
#         "units": "METRIC",
#         "languageCode": "en-US",
#         "routeModifiers": {
#             "avoidTolls": True, 
#             "avoidHighways": False, 
#             "avoidFerries": True
#         }
#     }
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         response.raise_for_status()
        
# def decode_polyline(polyline_str):
#     index, lat, lng = 0, 0, 0
#     coordinates = []
#     changes = {'latitude': 0, 'longitude': 0}

#     while index < len(polyline_str):
#         for unit in ['latitude', 'longitude']:
#             shift, result = 0, 0
#             while True:
#                 byte = ord(polyline_str[index]) - 63
#                 index += 1
#                 result |= (byte & 0x1f) << shift
#                 shift += 5
#                 if not byte >= 0x20:
#                     break
#             if (result & 1):
#                 changes[unit] = ~(result >> 1)
#             else:
#                 changes[unit] = (result >> 1)

#         lat += changes['latitude']
#         lng += changes['longitude']
#         coordinates.append((lat / 1e5, lng / 1e5))
#     return coordinates

# if __name__ == "__main__":
#     print(f"API_KEY: {API_KEY}")  # Debugging
#     routes = get_routes()
#     if routes:
#         location = decode_polyline(routes['routes'][0]['polyline']['encodedPolyline'])
#         print(location)

import requests
import json
import os

API_KEY = os.getenv("RoutesAPIKey")  #Ensure this is set correctly
if not API_KEY:
    raise ValueError("API Key is missing. Set it in environment variables.")

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

def getResponse(oriLat, oriLong, destLat, destLong):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.legs.distanceMeters,routes.legs.duration,routes.legs.steps.navigationInstruction"
    }

    data = {
        "origin": {"location": {"latLng": {"latitude": oriLat, "longitude": oriLong}}},
        "destination": {"location": {"latLng": {"latitude": destLat, "longitude": destLong}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",  #Fixed field name
        "computeAlternativeRoutes": True,
        "units": "METRIC",
        "languageCode": "en-US",
        "routeModifiers": {
            "avoidTolls": True, 
            "avoidHighways": False, 
            "avoidFerries": True
        }
    }
    print(json.dumps(data, indent=2))  #Debugging JSON structure
    response = requests.post(url, headers=headers, json=data)
    return response.json()
    
def findOptimalRoute():
    try:
        print("Sending request with data:")
        directions = getResponse(37.417670, -122.0827784, 37.417670, -121.079595)

        #Extract trip details
        if "routes" in directions and directions["routes"]:
            route = directions["routes"][0]  #Assuming first route is optimal

            for leg in route.get("legs", []):
                distance_m = leg.get("distanceMeters", "Unknown distance")
                distance_km = round(distance_m/1000, 2)

                duration_s = int(leg.get("duration", "Unknown duration").replace("s", ""))
                hours = duration_s//3600
                minutes = (duration_s%3600)//60
                duration_final = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

                print(f"Total Distance: {distance_km} km")
                print(f"Total Duration: {duration_final}")
                print("\nNavigation Instructions:")
                steps = leg.get("steps", [])
                for i, step in enumerate(steps):
                    instruction = step.get("navigationInstruction", {})
                    print(f"- {instruction}")
                    # If it's the last step, add a "You have arrived" message
                    if i == len(steps) - 1:
                        print("You have reached your final destination!")
        else:
            print("No route found!")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    routes = findOptimalRoute()
    if routes:
        print(routes)