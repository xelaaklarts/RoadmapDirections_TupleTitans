import pygame
import conversion

def initialize_pygame():
    pygame.init()
    screen_width = 2*256
    screen_height = 2*256
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    return screen, clock, screen_width, screen_height

# Draws grid to screen
def draw_grid(screen, width, height):
    # Draw vertical lines
    for x in range(0, width, 256):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height), 2)

    # Draw horizontal lines
    for y in range(0, height, 256):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), 2)

def draw_latlng_points(screen, latlng_list, zoom, tile_bounds, image_size):
    point_colour = (255, 0, 0)
    text_colour = (0, 0, 0)
    for latlng in latlng_list:
        point = conversion.from_latlng_to_pixel(latlng[0], latlng[1], zoom, tile_bounds, image_size)
        pygame.draw.circle(screen, point_colour, (int(point['pixel_x']), int(point['pixel_y'])), 5)

        # Draw point text if it exists
        if len(latlng) == 3:
            font = pygame.font.Font(None, 24)
            text = font.render(latlng[2], True, text_colour)
            screen.blit(text, (int(point['pixel_x'] - text.get_width() / 2), int(point['pixel_y'] + text.get_height() / 2)))

def draw_tiles_to_screen(screen, tile_array):
    for y, tile_row in enumerate(tile_array):
        for x, tile in enumerate(tile_row):
            screen.blit(tile, (x * 256, y * 256))

def update_screen():
    pygame.display.flip()

def pygame_quit():
    pygame.quit()

def check_if_running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
