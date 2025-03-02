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
    session, image_width, image_height = create_session(map_type)

    # Temporary fix for image size
    # Ensures that the image is square for now
    image_size = image_height

    # Initialize pygame
    screen, clock, screen_width, screen_height = py_draw.initialize_pygame()

    # Calculate the minimum zoom level
    zoom = conversion.calculate_maximum_zoom_level(latlng_list, image_size)

    # Get the tile bounds
    tile_bounds = conversion.calculate_tile_bounds_given_coordinate_bounds(
        conversion.find_coordinate_bounds_from_list(latlng_list), zoom, image_size)

    # Request tiles
    tile_array = load_tiles(session, zoom, tile_bounds)

    # Main loop
    running = True
    while running:
        running = py_draw.check_if_running()

        # Draw tiles to screen
        py_draw.draw_tiles_to_screen(screen, tile_array)

        # Draw grid
        # py_draw.draw_grid(screen, screen_width, screen_height)

        # Draw connecting lines
        py_draw.draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size , (255, 0, 0), 9)

        # Draw latlng outline points
        py_draw.draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, (0, 0, 0), 8, (0, 0, 0), 24)

        # Draw latlng points
        py_draw.draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, (255, 0, 0), 5, (0, 0, 0), 24)
        
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
        (37.7749, -122.4194, "San Francisco"),  # San Francisco
        (34.0522, -118.2437, "Los Angeles"),    # Los Angeles
        (40.7128, -74.0060, "New York City"),   # New York City
        (41.8781, -87.6298, "Chicago")          # Chicago
    ]
    
    # Example latlng_list 30 Carlton
    latlng_list2 = [
        (43.0012504080768, -81.24015792478556, "One"),     # Point One
        (43.00123079203837, -81.23852177737326, "Two"),    # Point Two
        (43.00002243199465, -81.24010428060811, "Three"),  # Point Three
        (43.00024754206482, -81.23878458158435, "Four")    # Point Four
    ]

    latlng_list3 = [
        (43.00072978730011, -81.23937016482253, "One"),   # Point One
        (43.00042339276636, -81.2404807902414, "Two"),    # Point Two
        (42.9994065948314, -81.23998494646074, "Three"),  # Point Three
        (43.00019041833122, -81.23718438812998, "Four"),  # Point Four
        (43.00218259138162, -81.23817319573764, "five"),  # Point Five
        (43.00246718226428, -81.23715249106445, "Six"),   # Point Six
        (43.0017160461225, -81.23679524445441, "Seven")  # Point Seven
    ]

    # Change this to whatever latlng_list you want to use
    current_list = latlng_list3

    # Call the main function
    main(current_list, 'roadmap')