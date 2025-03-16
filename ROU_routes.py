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