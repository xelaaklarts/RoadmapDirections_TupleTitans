# Import required libraries
from request import load_tiles
from request import remove_tiles
from request import create_session
import py_draw
import conversion
# Remove key_handler import in future
import key_handler as key

# Initialize constants
FPS = 120

# Main function
def main(latlng_list, map_type, detail, buffer):
    if detail > 4:
        print("Detail too high! Setting to 4.")
        detail = 4

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
    released = True

    # Main loop
    while running:
        # Check for quit event
        running = py_draw.check_if_running()

        # Calculate the new screen offset based on mouse movement
        # NOTE MOVE THIS OUT OF MAIN
        current_mouse_pos = key.mouse_position()
        screen_offset = py_draw.calculate_draw_offset(screen_offset, last_mouse_pos, current_mouse_pos, tile_bounds, image_size)
        last_mouse_pos = current_mouse_pos

        # Get the latlng position of the mouse
        # Add to latlng_list if right mouse button is pressed
        if key.is_right_mouse_pressed() and released:
            point_latlng_postion = conversion.from_pixel_to_latlng(key.mouse_position(), tile_bounds, zoom, image_size, screen_offset)
            coordinate = (point_latlng_postion['lat'], point_latlng_postion['lng'])
            print(coordinate)
            latlng_list.append((point_latlng_postion['lat'], point_latlng_postion['lng']))
            released = False
        # Ensures that only one point is added per click
        elif not key.is_right_mouse_pressed():
            released = True

        # Get the window size
        # This was used by activation bounds debug
        # window_size = py_draw.get_window_size()

        # Draw background
        py_draw.draw_background(screen, (255, 255, 255))

        # Draw tiles to screen
        py_draw.draw_tiles_to_screen(screen, tile_array, image_size, screen_offset)

        # Draw grid
        py_draw.draw_grid(screen, conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds), image_size, (0, 0, 0), 1, screen_offset)

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

    # Remove tiles from file
    remove_tiles()

# Beginning of the script
if __name__ == "__main__":

    # Load latlng list from file
    latlng_list = conversion.from_txt_to_list("!Lshape_coord.txt")

    # Call the main function
    main(latlng_list, 'satellite', 0, 0)