# Import required libraries
import tiles2D_conversion as conversion
import tiles2D_key_handler as key
import pygame

# Initializes pygame
def initialize_pygame(delta_tiles, image_size):
    pygame.init()
    # IMPORTANT: Windows display scale effects window size!
    screen_width = 1400
    screen_height = 800
    window_name = "Map Visualizer - Tuple Titans"
    pygame.display.set_caption(window_name)
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.mouse.set_visible(False) # Hide cursor here
    clock = pygame.time.Clock()
    return screen, clock, (screen_width, screen_height)

# Draws background to screen
def draw_background(screen, colour):
    screen.fill(colour)

# Draws grid to screen
def draw_grid(screen, delta_tiles, image_size, colour, thickness, screen_offset):
    for x in range(delta_tiles[0] + 1):
        pygame.draw.line(screen, colour, (x * image_size[0] + screen_offset[0], screen_offset[1]),
                         (x * image_size[0] + screen_offset[0], delta_tiles[1] * image_size[1] + screen_offset[1]), thickness)
    for y in range(delta_tiles[1] + 1):
        pygame.draw.line(screen, colour, (screen_offset[0], y * image_size[1] + screen_offset[1]),
                         (delta_tiles[0] * image_size[0] + screen_offset[0], y * image_size[1] + screen_offset[1]), thickness)

# Draws cursor circle to screen
def draw_cursor_circle(screen, cursor_size, current_mouse_pos, left_mouse_pressed, events):
    if left_mouse_pressed:
        pygame.draw.circle(screen, (255, 0, 0), (key.mouse_position(current_mouse_pos, events)[0], key.mouse_position(current_mouse_pos, events)[1]), cursor_size + 6)
    pygame.draw.circle(screen, (0, 0, 0), (key.mouse_position(current_mouse_pos, events)[0], key.mouse_position(current_mouse_pos, events)[1]), cursor_size + 3)
    pygame.draw.circle(screen, (255, 255, 255), (key.mouse_position(current_mouse_pos, events)[0], key.mouse_position(current_mouse_pos, events)[1]), cursor_size)

# Draws latlng points to screen
def draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, point_colour, point_size, outline_colour, outline_thickness, text_colour, font_size, font_outline_size, screen_offset):
    for latlng in latlng_list:
        point = conversion.from_latlng_to_pixel(latlng[0], latlng[1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, outline_colour, (int(point['pixel_x']) + screen_offset[0], int(point['pixel_y']) + screen_offset[1]), point_size + outline_thickness)
        pygame.draw.circle(screen, point_colour, (int(point['pixel_x']) + screen_offset[0], int(point['pixel_y']) + screen_offset[1]), point_size)

        # Draw point text if it exists
        if len(latlng) == 3:
            font = pygame.font.Font(None, font_size)
            text = font.render(latlng[2], True, text_colour)
            outline_font = pygame.font.Font(None, font_size + font_outline_size)
            outline_text = outline_font.render(latlng[2], True, outline_colour)
            screen.blit(outline_text, (int(point['pixel_x'] - outline_text.get_width() / 2) + screen_offset[0], int(point['pixel_y'] + outline_text.get_height()) + screen_offset[1]))
            screen.blit(text, (int(point['pixel_x'] - text.get_width() / 2) + screen_offset[0], int(point['pixel_y'] + text.get_height()) + screen_offset[1]))

# Draws first and last latlng points to screen
def draw_first_and_last_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, point_colour, point_size, outline_colour, outline_thickness, text_colour, font_size, font_outline_size, screen_offset):
    for latlng in [latlng_list[0], latlng_list[-1]]:
        point = conversion.from_latlng_to_pixel(latlng[0], latlng[1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, outline_colour, (int(point['pixel_x']) + screen_offset[0], int(point['pixel_y']) + screen_offset[1]), point_size + outline_thickness)
        pygame.draw.circle(screen, point_colour, (int(point['pixel_x']) + screen_offset[0], int(point['pixel_y']) + screen_offset[1]), point_size)

        # Draw point text if it exists
        if len(latlng) == 3:
            font = pygame.font.Font(None, font_size)
            text = font.render(latlng[2], True, text_colour)
            outline_font = pygame.font.Font(None, font_size + font_outline_size)
            outline_text = outline_font.render(latlng[2], True, outline_colour)
            screen.blit(outline_text, (int(point['pixel_x'] - outline_text.get_width() / 2) + screen_offset[0], int(point['pixel_y'] + outline_text.get_height()) + screen_offset[1]))
            screen.blit(text, (int(point['pixel_x'] - text.get_width() / 2) + screen_offset[0], int(point['pixel_y'] + text.get_height()) + screen_offset[1]))

# Draws connecting lines to screen
def draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size, line_colour, line_width, outline_thickness, outline_colour, screen_offset):
    for i in range(len(latlng_list) - 1):
        point1 = conversion.from_latlng_to_pixel(latlng_list[i][0], latlng_list[i][1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, line_colour, (int(point1['pixel_x']) + screen_offset[0], int(point1['pixel_y']) + screen_offset[1]), line_width/2)
        point2 = conversion.from_latlng_to_pixel(latlng_list[i + 1][0], latlng_list[i + 1][1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, line_colour, (int(point2['pixel_x']) + screen_offset[0], int(point2['pixel_y']) + screen_offset[1]), line_width/2)
        pygame.draw.line(screen, outline_colour, (int(point1['pixel_x']) + screen_offset[0], int(point1['pixel_y']) + screen_offset[1]),
                         (int(point2['pixel_x']) + screen_offset[0], int(point2['pixel_y']) + screen_offset[1]), line_width + outline_thickness)
        pygame.draw.line(screen, line_colour, (int(point1['pixel_x']) + screen_offset[0], int(point1['pixel_y']) + screen_offset[1]),
                         (int(point2['pixel_x']) + screen_offset[0], int(point2['pixel_y']) + screen_offset[1]), line_width)

# Draws tiles to screen
def draw_tiles_to_screen(screen, tile_array, image_size, screen_offset):
    for y, tile_row in enumerate(tile_array):
        for x, tile in enumerate(tile_row):
            screen.blit(pygame.transform.scale(tile, image_size), (x * image_size[0] + screen_offset[0], y * image_size[1] + screen_offset[1]))

# Draws tile bounds to screen
def draw_tile_bounds(screen, tile_bounds, image_size, colour, width, screen_offset):
    delta_pixel = conversion.calculate_delta_pixels_from_delta_tiles(conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds), image_size)
    pygame.draw.rect(screen, colour, (screen_offset[0], screen_offset[1], delta_pixel[0], delta_pixel[1]), width)

# Draws tile gen activation bounds to screen
# Debugging purposes only
def draw_activation_bounds(screen, window_size):
    pygame.draw.rect(screen, (0, 255, 0), (window_size[0]/4, window_size[1]/4, 2*window_size[0]/4, 2*window_size[1]/4), 5)

# Draws debug center screen circle to screen
def draw_center_screen_circle(screen, window_size):
    pygame.draw.circle(screen, (255, 0, 0), (window_size[0] / 2, window_size[1] / 2), 10)

# Draws debug center screen to 0,0 offset line to screen
def draw_center_screen_to_0_0_offset(screen, window_size, screen_offset):
    pygame.draw.line(screen, (0, 0, 0), (window_size[0]/2, window_size[1]/2), (screen_offset[0], screen_offset[1]), 5)

# Calculates the new screen offset based on mouse movement
# Does not allow the tiles to be dragged off screen!
# Collision detection is based on the tile bounds, screen offset, image size, and window size
def calculate_draw_offset(screen_offset, last_mouse_pos, current_mouse_pos, tile_bounds, image_size, collisions, left_mouse_pressed):

    # Mouse movement
    if left_mouse_pressed:
        delta_x = current_mouse_pos[0] - last_mouse_pos[0]
        delta_y = current_mouse_pos[1] - last_mouse_pos[1]
        last_mouse_pos = current_mouse_pos
        screen_offset =  (screen_offset[0] + delta_x, screen_offset[1] + delta_y)

    # Primary collision detection with center screen
    delta_tiles = conversion.calculate_delta_tiles_from_tile_bounds(tile_bounds)
    delta_tile_pixel = conversion.calculate_delta_pixels_from_delta_tiles(delta_tiles, image_size)
    window_size = get_window_size()
    if screen_offset[0] > window_size[0] / 2:
        screen_offset = (window_size[0] / 2, screen_offset[1])
    if screen_offset[1] > window_size[1] / 2:
        screen_offset = (screen_offset[0], window_size[1] / 2)
    if screen_offset[0] < window_size[0] / 2 - delta_tile_pixel[0]:
        screen_offset = (window_size[0] / 2 - delta_tile_pixel[0], screen_offset[1])
    if screen_offset[1] < window_size[1] / 2 - delta_tile_pixel[1]:
        screen_offset = (screen_offset[0], window_size[1] / 2 - delta_tile_pixel[1])

    # Secondary collision detection with window bounds
    if collisions:
        if screen_offset[0] > 0:
            screen_offset = (0, screen_offset[1])
        if screen_offset[1] > 0:
            screen_offset = (screen_offset[0], 0)
        if screen_offset[0] < window_size[0] - delta_tile_pixel[0]:
            screen_offset = (window_size[0] - delta_tile_pixel[0], screen_offset[1])
        if screen_offset[1] < window_size[1] - delta_tile_pixel[1]:
            screen_offset = (screen_offset[0], window_size[1] - delta_tile_pixel[1])
    return screen_offset

# Gets the window size
def get_window_size():
    return pygame.display.get_surface().get_size()

# Updates the display
def update_screen():
    pygame.display.flip()

# Quits pygame
def pygame_quit():
    pygame.quit()

# Checks if pygame is still running
def check_if_running(events):
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True