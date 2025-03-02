# Import required libraries
from request import load_tiles
from request import create_session
import py_draw
import conversion

# Constants
FPS = 60

# Main function
def main(latlng_list, map_type):
    # Make session
    session, image_size = create_session(map_type)

    # Calculate the minimum zoom level
    # Add extra zoom to increase accuracy
    zoom = conversion.calculate_maximum_zoom_level(latlng_list, image_size, 0)

    # Get the tile bounds
    tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
        conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size)

    # Request tiles
    tile_array = load_tiles(session, zoom, tile_bounds, map_type)

    # Initialize pygame
    screen, clock, screen_width, screen_height = py_draw.initialize_pygame(
        conversion.calculate_delta_tiles(tile_bounds), image_size)

    # Main loop
    running = True
    while running:
        running = py_draw.check_if_running()

        # Draw background
        py_draw.draw_background(screen, (255, 255, 255))

        # Draw tiles to screen
        py_draw.draw_tiles_to_screen(screen, tile_array, image_size)

        # Draw grid
        py_draw.draw_grid(screen, screen_width, screen_height, image_size)

        # Draw connecting outline lines 
        py_draw.draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size , (0, 0, 0), 11)

        # Draw connecting lines
        py_draw.draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size , (255, 0, 0), 6)

        # Draw latlng outline points
        py_draw.draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, (0, 0, 0), 8, (0, 0, 0), 24)

        # Draw latlng points
        py_draw.draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, (255, 0, 0), 4, (0, 0, 0), 24)
        
        # Update the display
        py_draw.update_screen()

        # Cap the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    py_draw.pygame_quit()

# Beginning of the script
if __name__ == "__main__":

    # Example latlng_list cities
    latlng_list1 = [
        (34.0522, -118.2437, "Los Angeles"),    # Los Angeles
        (37.7749, -122.4194, "San Francisco"),  # San Francisco
        (41.8781, -87.6298, "Chicago"),         # Chicago
        (40.7128, -74.0060, "New York City")    # New York City
    ]

    # Example latlng_list 30 Carlton 1
    latlng_list2 = [
        (43.00072978730011, -81.23937016482253, "One"),   # Point One
        (43.00042339276636, -81.2404807902414, "Two"),    # Point Two
        (42.9994065948314, -81.23998494646074, "Three"),  # Point Three
        (43.00019041833122, -81.23718438812998, "Four"),  # Point Four
        (43.00218259138162, -81.23817319573764, "five"),  # Point Five
        (43.00246718226428, -81.23715249106445, "Six"),   # Point Six
        (43.0017160461225, -81.23679524445441, "Seven")   # Point Seven
    ]

    # Example latlng_list Western University
    latlng_list3 = [
        (43.00602936065563, -81.2626887034016),     # Point One
        (43.005457938808725, -81.26464547108368),   # Point Two
        (43.00774527933711, -81.26578403298055),    # Point Three
        (43.007562814169994, -81.26658512578999),   # Point Four
        (43.00799976932445, -81.26992739018466),    # Point Five
        (43.007258055274754, -81.2699922030991),    # Point Six
        (43.00629302043631, -81.2703566291976),     # Point Seven
        (43.006107279776245, -81.27088670348355),   # Point Eight
        (43.0062647555907, -81.27177016070905),     # Point Nine
        (43.0066484499922, -81.2734772492384),      # Point Ten
        (43.00626081891621, -81.27484660781047),    # Point Eleven
        (43.00638195389022, -81.27517238263205),    # Point Twelve
        (43.006620185318695, -81.27537116060049),   # Point Thirteen
        (43.006620185318695, -81.27573558667208)    # Point Fourteen
    ]

    latlng_list4 = [
        (43.000829888040506, -81.23819051256874, "One"),    # Point One
        (43.000829888040506, -81.25035435025111, "Two"),     # Point Two
        (43.000829888040506, -81.25515292852671, "Three"),   # Point Three
        (43.000829888040506, -81.26182072047506, "Four"),    # Point Four
        (43.000829888040506, -81.26675879234801, "Five"),   # Point Five
        (43.000829888040506, -81.27521210166836, "Six"),    # Point Six
        (42.996157297508980, -81.27521210166836, "Seven")   # Point Seven
    ]

    # Change this to whatever latlng_list test case you want to use:
    # latlng_list1
    # latlng_list2
    # latlng_list3
    # latlng_list4
    current_list = latlng_list4

    # Call the main function
    main(current_list, 'roadmap')