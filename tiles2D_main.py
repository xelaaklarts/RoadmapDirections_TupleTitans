# Import required libraries
from tiles2D_request import load_tiles
from tiles2D_request import remove_tiles
from tiles2D_request import create_session
import tiles2D_conversion as conversion
import tiles2D_key_handler as key
import tiles2D_py_draw as py_draw

# Initialize constants
FPS = 120

# Main function
def main(latlng_list, map_type, detail, bounds_buffer, collisions, debug, auto_delete):
    
    # Set max detail
    max_detail = 4

    # Set detail to max detail if too high
    if detail > max_detail:
        print(f"Detail too high! Setting to {max_detail}.")
        detail = 3

    # Make session
    session, image_size = create_session(map_type)

    # Calculate the maximum zoom level
    # Add extra detail to increase zoom
    zoom = conversion.calculate_maximum_zoom_level(latlng_list, image_size, detail)

    # Get the tile bounds
    tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
        conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size, bounds_buffer)
    
    # Get pixel bounds
    delta_pixel = conversion.calculate_delta_tile_pixels_from_tile_bounds(tile_bounds, image_size)

    # Request tiles
    tile_array = load_tiles(session, zoom, tile_bounds, map_type)

    # Initialize pygame
    screen, clock, window_size = py_draw.initialize_pygame(
        conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds), image_size)
    
    # Initialize variables
    running = True
    screen_offset = (window_size[0] / 2 - delta_pixel[0] / 2, window_size[1] / 2 - delta_pixel[1] / 2)
    current_mouse_pos = (0,0)
    last_mouse_pos = (0,0)
    left_mouse_pressed = False
    middle_mouse_pressed = False
    right_mouse_pressed = False
    wheel_up_event = False
    wheel_down_event = False
    allow_point = True

    # Main loop
    while running:

        # Get events within frame
        events = key.event_list()
        left_mouse_pressed = key.is_left_mouse_pressed(left_mouse_pressed, events)
        middle_mouse_pressed = key.is_middle_mouse_pressed(middle_mouse_pressed, events)
        right_mouse_pressed = key.is_right_mouse_pressed(right_mouse_pressed, events)
        wheel_up_event = key.if_mousewheelup(events)
        wheel_down_event = key.if_mousewheeldown(events)
        current_mouse_pos = key.mouse_position(current_mouse_pos, events)

        # Check for quit event
        running = py_draw.check_if_running(events)

        # Keys within frame
        # Used in future for key events
        keys = key.keys_list()

        # Calculate the new screen offset based on mouse movement
        screen_offset = py_draw.calculate_draw_offset(
            screen_offset, last_mouse_pos, current_mouse_pos, tile_bounds, image_size, collisions, left_mouse_pressed)
        last_mouse_pos = current_mouse_pos

        # Get the latlng position of the mouse
        # Add to latlng_list if right mouse button is pressed
        if right_mouse_pressed and allow_point:
            point_latlng_postion = conversion.from_pixel_to_latlng(
                key.mouse_position(current_mouse_pos, events), tile_bounds, zoom, image_size, screen_offset)
            coordinate = (point_latlng_postion['lat'], point_latlng_postion['lng'])
            print(coordinate)
            latlng_list.append((point_latlng_postion['lat'], point_latlng_postion['lng']))
            # Get the tile bounds
            tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
                conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size, bounds_buffer)
            # Request tiles
            tile_array = load_tiles(session, zoom, tile_bounds, map_type)
            allow_point = False

        # Allow point to be added again
        # Ensure only one point is added per click
        if not right_mouse_pressed:
            allow_point = True

        # Check for zoom in
        if wheel_up_event:
            detail += 1
            if detail > max_detail:
                detail = max_detail
                print(f"Detail too high! Setting to {max_detail}.")
            else:
                zoom += 1
                screen_offset = (screen_offset[0] + (screen_offset[0] - window_size[0] / 2),
                                 screen_offset[1] + (screen_offset[1] - window_size[1] / 2))
                tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
                    conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size, bounds_buffer)
                # Request tiles
                tile_array = load_tiles(session, zoom, tile_bounds, map_type)
                print(f"Plus  key pressed. Zoom: {zoom}")

        # Check for zoom out
        if wheel_down_event:
            detail -= 1
            zoom -= 1
            if zoom < 0:
                zoom = 0
                detail = detail + 1
                print("Zoom too low! Setting to 0.")
            else:
                # Get the tile bounds
                screen_offset = (screen_offset[0] - (screen_offset[0] - window_size[0] / 2) / 2,
                                 screen_offset[1] - (screen_offset[1] - window_size[1] / 2) / 2)
                tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
                    conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size, bounds_buffer)
                # Request tiles
                tile_array = load_tiles(session, zoom, tile_bounds, map_type)
                print(f"Minus key pressed. Zoom: {zoom}")

        # Draw background
        py_draw.draw_background(screen, (200, 200, 200))

        # Draw tiles to screen
        py_draw.draw_tiles_to_screen(screen, tile_array, image_size, screen_offset)

        if debug:
        # Draw grid
            py_draw.draw_grid(screen, conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds),
                image_size, (0, 0, 0), 1, screen_offset)

        # Draw connecting lines
        py_draw.draw_connecting_lines(
            screen, latlng_list, zoom, tile_bounds, image_size , (255, 0, 0), 16, 0, (0, 0, 0), screen_offset)

        # Draw latlng first and last points
        py_draw.draw_first_and_last_latlng_points(
            screen, latlng_list, zoom, tile_bounds, image_size,
            (255, 0, 0), 14, (0, 0, 0), 2, (255, 255, 255), 30, 1, screen_offset)
        
        # Draw tile bounds
        py_draw.draw_tile_bounds(screen, tile_bounds, image_size, (0, 0, 0), 5, screen_offset)

        # Draw cursor circle
        py_draw.draw_cursor_circle(screen, 10, current_mouse_pos, left_mouse_pressed, events)

        # Debug mode
        if debug:
            # Draw degbug tile gen activation bounds
            py_draw.draw_activation_bounds(screen, window_size)

            # Draw debug center screen to 0,0 offset
            py_draw.draw_center_screen_to_0_0_offset(screen, window_size, screen_offset)

            # Draw debug center screen circle
            py_draw.draw_center_screen_circle(screen, window_size)
        
        # Update the display
        py_draw.update_screen()

        # Cap the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    py_draw.pygame_quit()

    # Remove tiles from file
    if auto_delete:
        remove_tiles()

# Beginning of the script
if __name__ == "__main__":

    # Call the main function
    main(latlng_list=conversion.from_txt_to_list("tiles2D_test_coordinates\campus_coord.txt"),
         map_type='satellite',
         detail=3,
         bounds_buffer=2,
         collisions=True,
         debug=False,
         auto_delete=False)

    ## NOTE TO SELF ##
    # Adding bounds and zooming out goes out of tile range
    # Add a zoomout cap based on additional bounds
    # Zoom feature does not account for bounds!! Please fix.
    # Zoom position struggles when zooming out because it does not account for aspect ratio change!
    # However the ratio change does not know which side was cut/added to
    # I should add a for loop that proloads tiles at all zoom levels before begining the program.
    # This will help counter initial lag spikes.
    # Make each route its own object
    # Add route class