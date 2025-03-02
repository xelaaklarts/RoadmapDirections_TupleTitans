import math

def from_latlng_to_point(lat, lng, zoom, image_size):
    mercator = -math.log(math.tan((0.25 + lat / 360) * math.pi))
    return {
        'x': image_size * (lng / 360 + 0.5) * 2 ** zoom,
        'y': image_size / 2 * (1 + mercator / math.pi) * 2 ** zoom
    }

def from_latlng_to_pixel(lat, lng, zoom, tile_bounds, image_size):
    point = from_latlng_to_point(lat, lng, zoom, image_size)
    tile_x = point['x'] // image_size
    tile_y = point['y'] // image_size
    offset_x = point['x'] % image_size
    offset_y = point['y'] % image_size
    return {
    'pixel_x' : (tile_x - tile_bounds['min_tile_x']) * image_size + offset_x,
    'pixel_y' : (tile_y - tile_bounds['min_tile_y']) * image_size + offset_y
    }

def from_latlng_to_tile_coord(lat, lng, zoom, image_size):
    point = from_latlng_to_point(lat, lng, zoom, image_size)

    return {
        'x': int(point['x'] / image_size),
        'y': int(point['y'] / image_size),
        'z': zoom
    }

# Calculate max zoom level that is able to encompass all latlng coordinates
def calculate_maximum_zoom_level(latlng_list, image_size):
    latlng_bounds = find_coordinate_bounds_from_list(latlng_list)
    latlng_list = [(latlng_bounds['min_lat'], latlng_bounds['min_lng']),
                   (latlng_bounds['max_lat'], latlng_bounds['max_lng'])]

    coordinate_bounds = find_coordinate_bounds_from_list(latlng_list)

    # Calculate RELATIVE the maximum zoom level
    # This is independant of tile location
    max_zoom = int(math.floor(math.log2(image_size / (coordinate_bounds['max_lng'] - coordinate_bounds['min_lng']))))

    # Add 1 to the zoom level to ensure that the entire area is covered when accounting for tile location
    return max_zoom + 1

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
def calculate_tile_bounds_given_coordinate_bounds(latlng_bounds, zoom, image_size):
    latlng_list = [(latlng_bounds['min_lat'], latlng_bounds['min_lng']),
                   (latlng_bounds['max_lat'], latlng_bounds['max_lng'])]

    coordinate_bounds = find_coordinate_bounds_from_list(latlng_list)

    return {
        'min_tile_x': from_latlng_to_tile_coord(coordinate_bounds['min_lat'], coordinate_bounds['min_lng'], zoom, image_size)['x'],
        'max_tile_x': from_latlng_to_tile_coord(coordinate_bounds['max_lat'], coordinate_bounds['max_lng'], zoom, image_size)['x'],
        # Note: The y-coordinates are inverted in tile coordinates
        'min_tile_y': from_latlng_to_tile_coord(coordinate_bounds['max_lat'], coordinate_bounds['min_lng'], zoom, image_size)['y'],
        'max_tile_y': from_latlng_to_tile_coord(coordinate_bounds['min_lat'], coordinate_bounds['max_lng'], zoom, image_size)['y'],
        'zoom': zoom
    }