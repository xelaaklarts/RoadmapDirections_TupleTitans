# Import required libraries
from pygame.image import load
from os.path import exists
from os import getenv, makedirs
import requests
import shutil

# Google Maps Roadmap Tiles API endpoints
CREATE_SESSION_URL = "https://tile.googleapis.com/tile/v1/createSession"
TILE_URL_TEMPLATE = "https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}"

# Get the API key from environment variables
API_KEY = getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

tiles_directory = "tiles"
if not exists(tiles_directory):
    makedirs(tiles_directory)

# Function to create a new session token
def create_session(map_type):
    params = {
        "key": API_KEY,
        "mapType": map_type
    }
    response = requests.post(CREATE_SESSION_URL, params=params)
    if response.status_code == 200:
        session_data = response.json()
        print(f"Session created successfully: {session_data}")
        return session_data.get("session"), (session_data.get("tileWidth"), session_data.get("tileHeight"))
    else:
        raise Exception(f"Failed to create session: {response.status_code}, {response.text}")

# Function to get tiles for a specific z, x, y tile coordinates
# Note google claims that tile requests are free
def get_tile(session, z, x, y, map_type):
    url = TILE_URL_TEMPLATE.format(z=z, x=x, y=y)
    if map_type == 'roadmap':
        params = {
            "session": session,
            "key": API_KEY,
            "orientation": 0
        }
    elif map_type == 'satellite':
        params = {
            "session": session,
            "key": API_KEY
        }
    else:
        print("Unsupported map type. Please use 'roadmap' or 'satellite'.")
    
    # Make the request
    response = requests.get(url, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'image' in content_type:
            with open(f"tiles\\tile_{z}_{x}_{y}_0_{map_type}.png", "wb") as file:
                # Save the image
                file.write(response.content)
            print(f"Tile saved successfully. Named: tile_{z}_{x}_{y}_0_{map_type}.png")    
        else:
            print(f"Unexpected content type: {content_type}")
            try:
                print(f"Response JSON: {response.json()}")
            except ValueError:
                print("Response is not in JSON format.")
    else:
        print(f"Failed to fetch tile: {response.status_code}, {response.text}")

# Function to request tiles for a given tile bounds
def request_tiles(session, tile_bounds, zoom, map_type):
    # Request tiles
    for x in range(tile_bounds['min_tile_x'], tile_bounds['max_tile_x'] + 1):
        for y in range(tile_bounds['min_tile_y'], tile_bounds['max_tile_y'] + 1):
            # Check if tile already exists
            if not exists(f"tiles\\tile_{zoom}_{x}_{y}_0_{map_type}.png"):
                get_tile(session, zoom, x, y, map_type)

# Function to load tiles into a 2D array            
def load_tiles(session, zoom, tile_bounds, map_type):
    # Request tiles
    request_tiles(session, tile_bounds, zoom, map_type)
    # Load tiles into 2D array
    tile_array = []
    for y in range(tile_bounds['min_tile_y'], tile_bounds['max_tile_y'] + 1):
        tile_row = []
        for x in range(tile_bounds['min_tile_x'], tile_bounds['max_tile_x'] + 1):
            tile_row.append(load(f"tiles\\tile_{zoom}_{x}_{y}_0_{map_type}.png"))
        tile_array.append(tile_row)   
    return tile_array

def remove_tiles():
    shutil.rmtree("tiles")
    
# Example use
# Print world map
# Will not work if API key is not set
if __name__ == "__main__":
    session = create_session('satellite')
    get_tile(session[0], 15, 6294, 13288, 'satellite')