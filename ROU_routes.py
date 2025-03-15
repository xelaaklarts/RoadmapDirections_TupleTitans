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
from os import getenv

URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
API_KEY = getenv("API_KEY")

def get_route(start, dest):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
    }
    data = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": start[0],
                    "longitude": start[1]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": dest[0],
                    "longitude": dest[1]
                }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "IMPERIAL"
    }

    # Debugging: Print the headers and data
    # print("Headers:", headers)
    # print("Data:", data)

    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        routes = response.json()
        points = decode_polyline(routes['routes'][0]['polyline']['encodedPolyline'])
        return points
    else:
        print(f"Error: {response.status_code} - {response.text}")
        response.raise_for_status()

def decode_polyline(polyline_str):
    """Decodes a polyline that was encoded using the Google Maps method.
    See https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    """
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
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