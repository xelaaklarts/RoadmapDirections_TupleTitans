# Import required libraries
from request import load_tiles
from request import create_session
import py_draw
import conversion
# Remove key_handler import in future
import key_handler as key

# Initialize constants
FPS = 120

# Main function
def main(latlng_list, map_type, detail, buffer=0):
    # Make session
    session, image_size = create_session(map_type)

    # Calculate the minimum zoom level
    # Add extra zoom to increase accuracy
    zoom = conversion.calculate_maximum_zoom_level(latlng_list, image_size, detail)

    # Get the tile bounds
    tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
        conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size, buffer)

    # Request tiles
    tile_array = load_tiles(session, zoom, tile_bounds, map_type)

    # Initialize pygame
    # Access screen width and height later for scaling
    screen, clock, window_size = py_draw.initialize_pygame(
        conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds), image_size)
    
    # Initialize variables
    running = True
    screen_offset = (0,0)
    current_mouse_pos = (0,0)
    last_mouse_pos = (0,0)

    # Main loop
    while running:
        # Check for quit event
        running = py_draw.check_if_running()

        # Calculate the new screen offset based on mouse movement
        # NOTE MOVE THIS OUT OF MAIN
        current_mouse_pos = key.mouse_position()
        screen_offset = py_draw.calculate_draw_offset(screen_offset, last_mouse_pos, current_mouse_pos, tile_bounds, image_size)
        last_mouse_pos = current_mouse_pos

        # Get the window size
        window_size = py_draw.get_window_size()

        # Draw background
        py_draw.draw_background(screen, (255, 255, 255))

        # Draw tiles to screen
        py_draw.draw_tiles_to_screen(screen, tile_array, image_size, screen_offset)

        # Draw grid
        # py_draw.draw_grid(screen, conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds), image_size, (0, 0, 0), 1, screen_offset)

        # Draw connecting lines
        py_draw.draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size , (255, 0, 0), 16, 0, (0, 0, 0), screen_offset)

        # Draw latlng first and last points
        py_draw.draw_first_and_last_latlng_points(
            screen, latlng_list, zoom, tile_bounds, image_size, (255, 0, 0), 14, (0, 0, 0), 2, (255, 255, 255), 30, 1, screen_offset)

        # Draw debug circle
        py_draw.draw_cursor_circle(screen, 10)

        # Draw tile gen activation bounds
        # py_draw.draw_activation_bounds(screen, window_size)
        
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
        (43.00072978730011, -81.23937016482253, "Start"), # Point One
        (43.00042339276636, -81.2404807902414, "Two"),    # Point Two
        (42.9994065948314, -81.23998494646074, "Three"),  # Point Three
        (43.00019041833122, -81.23718438812998, "Four"),  # Point Four
        (43.00218259138162, -81.23817319573764, "five"),  # Point Five
        (43.00246718226428, -81.23715249106445, "Six"),   # Point Six
        (43.0017160461225, -81.23679524445441, "END")     # Point Seven
    ]

    # Example latlng_list Western University
    latlng_list3 = [
        (43.00602936065563, -81.2626887034016, "Start"),           # Point One
        (43.005457938808725, -81.26464547108368),                  # Point Two
        (43.00774527933711, -81.26578403298055),                   # Point Three
        (43.007562814169994, -81.26658512578999),                  # Point Four
        (43.00799976932445, -81.26992739018466),                   # Point Five
        (43.007258055274754, -81.2699922030991),                   # Point Six
        (43.00629302043631, -81.2703566291976),                    # Point Seven
        (43.006107279776245, -81.27088670348355),                  # Point Eight
        (43.0062647555907, -81.27177016070905),                    # Point Nine
        (43.0066484499922, -81.2734772492384),                     # Point Ten
        (43.00626081891621, -81.27484660781047),                   # Point Eleven
        (43.00638195389022, -81.27517238263205),                   # Point Twelve
        (43.006620185318695, -81.27537116060049),                  # Point Thirteen
        (43.006620185318695, -81.27573558667208, "Destination")    # Point Fourteen
    ]

    # Example latlng_list London L Shape
    latlng_list4 = [
        (43.000829888040506, -81.23819051256874, "One"),     # Point One
        (43.000829888040506, -81.25035435025111, "Two"),     # Point Two
        (43.000829888040506, -81.25515292852671, "Three"),   # Point Three
        (43.000829888040506, -81.26182072047506, "Four"),    # Point Four
        (43.000829888040506, -81.26675879234801, "Five"),    # Point Five
        (43.000829888040506, -81.27521210166836, "Six"),     # Point Six
        (42.996157297508980, -81.27521210166836, "Seven")    # Point Seven
    ]

    # Change this to whatever latlng_list test case you want to use:
    # latlng_list1 Cities
    # latlng_list2 30 Carlton
    # latlng_list3 Western University
    # latlng_list4 London L Shape
    # Call the main function
    # DO NOT SET DETAIL HIGHER THAN 3!! :)
    main(latlng_list3, 'satellite', 3, 1)

    ### Note To Self ###
    ### after dragging is added, add an appropriate screen size