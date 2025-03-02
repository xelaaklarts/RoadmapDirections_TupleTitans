# Import required libraries
import pygame
import conversion

# Initializes pygame
def initialize_pygame():
    pygame.init()
    screen_width = 2*256
    screen_height = 2*256
    window_name = "Map Visualizer - Tuple Titans"
    pygame.display.set_caption(window_name)
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    return screen, clock, screen_width, screen_height

# Draws background to screen
def draw_background(screen, colour):
    screen.fill(colour)

# Draws grid to screen
def draw_grid(screen, width, height):
    # Draw vertical lines
    for x in range(0, width, 256):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height), 2)

    # Draw horizontal lines
    for y in range(0, height, 256):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), 2)

# Draws latlng points to screen
def draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size, point_colour, point_size, text_colour, font_size):
    for latlng in latlng_list:
        point = conversion.from_latlng_to_pixel(latlng[0], latlng[1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, point_colour, (int(point['pixel_x']), int(point['pixel_y'])), point_size)

        # Draw point text if it exists
        if len(latlng) == 3:
            font = pygame.font.Font(None, font_size)
            text = font.render(latlng[2], True, text_colour)
            screen.blit(text, (int(point['pixel_x'] - text.get_width() / 2), int(point['pixel_y'] + text.get_height())))

def draw_connecting_lines(screen, latlng_list, zoom, tile_bounds, image_size, line_colour, line_width):
    for i in range(len(latlng_list) - 1):
        point1 = conversion.from_latlng_to_pixel(latlng_list[i][0], latlng_list[i][1], zoom, tile_bounds, image_size)
        point2 = conversion.from_latlng_to_pixel(latlng_list[i + 1][0], latlng_list[i + 1][1], zoom, tile_bounds, image_size)
        pygame.draw.line(screen, line_colour, (int(point1['pixel_x']), int(point1['pixel_y'])),
                         (int(point2['pixel_x']), int(point2['pixel_y'])), line_width)

# Draws tiles to screen
def draw_tiles_to_screen(screen, tile_array):
    for y, tile_row in enumerate(tile_array):
        for x, tile in enumerate(tile_row):
            screen.blit(tile, (x * 256, y * 256))

# Updates the display
def update_screen():
    pygame.display.flip()

# Quits pygame
def pygame_quit():
    pygame.quit()

# Checks if pygame is still running
def check_if_running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
