from pygame.image import load
from os.path import exists
from os import getenv
import requests

# Google Maps Roadmap Tiles API endpoints
CREATE_SESSION_URL = "https://tile.googleapis.com/tile/v1/createSession"
TILE_URL_TEMPLATE = "https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}"

# Get the API key from environment variables
API_KEY = getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

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
        return session_data.get("session"), session_data.get("tileWidth"), session_data.get("tileHeight")
    else:
        raise Exception(f"Failed to create session: {response.status_code}, {response.text}")

# Function to get tiles for a specific z, x, y tile coordinates
def get_tile(session, z, x, y):
    url = TILE_URL_TEMPLATE.format(z=z, x=x, y=y)
    params = {
        "session": session,
        "key": API_KEY,
        "orientation": 0
    }
    # Make the request
    response = requests.get(url, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'image' in content_type:
            with open(f"tile_{z}_{x}_{y}_0.png", "wb") as file:
                # Save the image
                file.write(response.content)
            print(f"Tile saved successfully. Named: tile_{z}_{x}_{y}_0.png")    
        else:
            print(f"Unexpected content type: {content_type}")
            try:
                print(f"Response JSON: {response.json()}")
            except ValueError:
                print("Response is not in JSON format.")
    else:
        print(f"Failed to fetch tile: {response.status_code}, {response.text}")

def request_tiles(session, tile_bounds, zoom):
    # Request tiles
    for x in range(tile_bounds['min_tile_x'], tile_bounds['max_tile_x'] + 1):
        for y in range(tile_bounds['min_tile_y'], tile_bounds['max_tile_y'] + 1):
            # Check if tile already exists
            if not exists(f"tile_{zoom}_{x}_{y}_0.png"):
                get_tile(session, zoom, x, y)
            
def load_tiles(session, zoom, tile_bounds):
    # Request tiles
    request_tiles(session, tile_bounds, zoom)
    # Load tiles into 2D array
    tile_array = []
    for y in range(tile_bounds['min_tile_y'], tile_bounds['max_tile_y'] + 1):
        tile_row = []
        for x in range(tile_bounds['min_tile_x'], tile_bounds['max_tile_x'] + 1):
            tile_row.append(load(f"tile_{zoom}_{x}_{y}_0.png"))
        tile_array.append(tile_row)   
    return tile_array
    
# Example usage
if __name__ == "__main__":
    session = create_session("roadmap")
    get_tile(session, 0, 0, 0, 0)