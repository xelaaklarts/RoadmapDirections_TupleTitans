# Import required libraries
import math

# Converts latlng coordinates to mercator coordinates
def from_latlng_to_point(lat, lng, zoom, image_size):
    mercator = -math.log(math.tan((0.25 + lat / 360) * math.pi))
    return {
        'x': image_size[0] * (lng / 360 + 0.5) * 2 ** zoom,
        'y': image_size[1] / 2 * (1 + mercator / math.pi) * 2 ** zoom
    }

# Converts latlng coordinates to pixel coordinates
def from_latlng_to_pixel(lat, lng, zoom, tile_bounds, image_size):
    point = from_latlng_to_point(lat, lng, zoom, image_size)
    tile_x = point['x'] // image_size[0]
    tile_y = point['y'] // image_size[1]
    offset_x = point['x'] % image_size[0]
    offset_y = point['y'] % image_size[1]
    return {
    'pixel_x' : (tile_x - tile_bounds['min_tile_x']) * image_size[0] + offset_x,
    'pixel_y' : (tile_y - tile_bounds['min_tile_y']) * image_size[1] + offset_y
    }

# Converts pixel coordinates to latlng coordinates
def from_pixel_to_latlng(pixel, tile_bounds, zoom, image_size, screen_offset):
    # Adjust pixel position with draw offset
    adjusted_pixel_x = pixel[0] - screen_offset[0]
    adjusted_pixel_y = pixel[1] - screen_offset[1]
    
    # Calculate the tile position
    tile_x = adjusted_pixel_x // image_size[0] + tile_bounds['min_tile_x']
    tile_y = adjusted_pixel_y // image_size[1] + tile_bounds['min_tile_y']
    
    # Calculate the offset within the tile
    offset_x = adjusted_pixel_x % image_size[0]
    offset_y = adjusted_pixel_y % image_size[1]
    
    # Calculate the point in the world coordinates
    point = {
        'x': tile_x * image_size[0] + offset_x,
        'y': tile_y * image_size[1] + offset_y
    }
    
    # Convert the point to latlng
    lng = point['x'] / (image_size[0] * 2 ** zoom) * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * point['y'] / (image_size[1] * 2 ** zoom)))))
    
    return {
        'lat': lat,
        'lng': lng
    }

# Converts latlng mercator coordinates to tile coordinates
def from_latlng_to_tile_coord(lat, lng, zoom, image_size):
    point = from_latlng_to_point(lat, lng, zoom, image_size)

    return {
        'x': int(point['x'] / image_size[0]),
        'y': int(point['y'] / image_size[1]),
        'z': zoom
    }

# Calculate max zoom level that is able to encompass all latlng coordinates
def calculate_maximum_zoom_level(latlng_list, image_size, extra_zoom):
    latlng_bounds = find_coordinate_bounds_from_list(latlng_list)
    latlng_list = [(latlng_bounds['min_lat'], latlng_bounds['min_lng']),
                   (latlng_bounds['max_lat'], latlng_bounds['max_lng'])]

    coordinate_bounds = find_coordinate_bounds_from_list(latlng_list)

    # Calculate RELATIVE the maximum zoom level
    # This is independant of tile location
    # Note this only accounts for the x-axis
    max_zoom = int(math.floor(math.log2(image_size[0] / (coordinate_bounds['max_lng'] - coordinate_bounds['min_lng']))))

    # Add 1 to the zoom level to ensure that the entire area is covered when accounting for tile location
    return max_zoom + extra_zoom + 1

# Finds the bounds of a list of latlng coordinates
def find_coordinate_bounds_from_list(latlng_list):
    min_lat = min(latlng_list, key=lambda x: x[0])[0]
    max_lat = max(latlng_list, key=lambda x: x[0])[0]
    min_lng = min(latlng_list, key=lambda x: x[1])[1]
    max_lng = max(latlng_list, key=lambda x: x[1])[1]

    return {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lng': min_lng,
        'max_lng': max_lng
    }

# Calculates the tile bounds given a list of latlng coordinates and zoom
def calculate_tile_bounds_given_coordinate_bounds(latlng_bounds, zoom, image_size, buffer):
    latlng_list = [(latlng_bounds['min_lat'], latlng_bounds['min_lng']),
                   (latlng_bounds['max_lat'], latlng_bounds['max_lng'])]

    coordinate_bounds = find_coordinate_bounds_from_list(latlng_list)

    return {
        'min_tile_x': from_latlng_to_tile_coord(coordinate_bounds['min_lat'], coordinate_bounds['min_lng'], zoom, image_size)['x'] - buffer,
        'max_tile_x': from_latlng_to_tile_coord(coordinate_bounds['max_lat'], coordinate_bounds['max_lng'], zoom, image_size)['x'] + buffer,
        # Note: The y-coordinates are inverted in tile coordinates
        'min_tile_y': from_latlng_to_tile_coord(coordinate_bounds['max_lat'], coordinate_bounds['min_lng'], zoom, image_size)['y'] - buffer,
        'max_tile_y': from_latlng_to_tile_coord(coordinate_bounds['min_lat'], coordinate_bounds['max_lng'], zoom, image_size)['y'] + buffer,
        'zoom': zoom
    }

# Calculates the total number of tiles given the tile bounds
def calculate_delta_tiles_from_tile_bounds(tile_bounds):
    return (tile_bounds['max_tile_x'] - tile_bounds['min_tile_x'] + 1), (tile_bounds['max_tile_y'] - tile_bounds['min_tile_y'] + 1)

# Calculates the total number of pixels given the tile bounds and image size
def calculate_delta_tile_pixels_from_tile_bounds(tile_bounds, image_size):
    return (tile_bounds['max_tile_x'] - tile_bounds['min_tile_x'] + 1) * image_size[0], (tile_bounds['max_tile_y'] - tile_bounds['min_tile_y'] + 1) * image_size[1]

# Calculates the total number of pixels given the delta tiles and image size
def calculate_delta_pixels_from_delta_tiles(delta_tiles, image_size):
    return delta_tiles[0] * image_size[0], delta_tiles[1] * image_size[1]

def from_txt_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    result = []
    for line in lines:
        parts = line.strip().split(',')
        lat = float(parts[0])
        lng = float(parts[1])
        if len(parts) == 3:
            label = parts[2]
            result.append((lat, lng, label))
        else:
            result.append((lat, lng))
    return result