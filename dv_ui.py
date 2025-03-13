# import sys module 
import pygame 
import sys 

def dv_ui(eval, dt):
    # pygame.init() will initialize all 
    # imported module 
    pygame.init() 

    clock = pygame.time.Clock() 

    # it will display on screen 
    screen = pygame.display.set_mode([600, 500]) 
    pygame.display.set_caption("Maps - Tuple Titans")
    background = pygame.image.load("dv_background.png")

    # basic font for user typed 
    base_font = pygame.font.Font(None, 32) 
    starting = '' 
    destination = ''

    words = ['Starting Address: ', 'Starting City: ', 'NEXT', 'Destination Address: ', 'Destination City: ', 'GO']
    dtype = 0
    if dt == 1:
        dtype = 3

    # create rectangle 
    starting_rect = pygame.Rect(20, 60, 140, 32) 
    destination_rect = pygame.Rect(20, 200, 140, 32)
    finish_rect = pygame.Rect(20, 448, 90, 32)
    if dt == 1: 
        finish_rect = pygame.Rect(20, 448, 64, 32)

    # colour_active stores colour(lightskyblue3) which 
    # gets active when input box is clicked by user 
    colour_active = pygame.Color('white') 

    # colour_passive store colour(chartreuse4) which is 
    # colour of input box. 
    colour_passive = pygame.Color('azure3') 

    colour1 = colour_passive
    colour2 = colour_passive 
    colour3 = pygame.Color('green')

    active1 = False
    active2 = False

    while True: 
        events = pygame.event.get()
        key_events = pygame.key.get_pressed()

        for event in events: 

        # if user types QUIT then the screen will close 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if starting_rect.collidepoint(event.pos): 
                    active1 = True
                else: 
                    active1 = False
                if destination_rect.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
                if finish_rect.collidepoint(event.pos):
                    eval = True # DO SOMETHING WITH THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


            if event.type == pygame.KEYDOWN: 
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
                    # get text input from 0 to -1 i.e. end. 
                    if active1:
                        starting = starting[:-1] 
                    elif active2:
                        destination = destination[:-1]
                elif event.key == pygame.K_RETURN:
                    if active1: 
                        active1 = False
                    elif active2:
                        active2 = False
                # Unicode standard is used for string 
                # formation 

                else: 
                    if active1:	
                        starting += event.unicode
                    elif active2:
                        destination += event.unicode
        
        # it will set background colour of screen 
        screen.fill((255, 255, 255)) 
        screen.blit(background, (0,0))

        if active1: 
            colour1 = colour_active 
        else: 
            colour1 = colour_passive 

        if active2: 
            colour2 = colour_active 
        else: 
            colour2 = colour_passive 
            
        # draw rectangle and argument passed which should 
        # be on screen 
        pygame.draw.rect(screen, colour1, starting_rect) 
        pygame.draw.rect(screen, (0,0,0), starting_rect, 2) 

        pygame.draw.rect(screen, colour2, destination_rect)
        pygame.draw.rect(screen, (0,0,0), destination_rect, 2)

        pygame.draw.rect(screen, colour3, finish_rect)
        pygame.draw.rect(screen, (0,0,0), finish_rect, 2)

        starting_render = base_font.render(starting, True, (0,0,0)) 
        destination_render = base_font.render(destination, True, (0,0,0))
        text1 = base_font.render(words[dtype], True, (0,0,0))
        text2 = base_font.render(words[dtype+1], True, (0,0,0))
        text3 = base_font.render(words[dtype+2], True, (0,0,0))

        # render at position stated in arguments 
        screen.blit(starting_render, (starting_rect.x+5, starting_rect.y+5)) 
        screen.blit(text1, (20, 20))

        screen.blit(destination_render, (destination_rect.x+5, destination_rect.y+5)) 
        screen.blit(text2, (20, 160))

        screen.blit(text3, (34, 454))
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        starting_rect.w = max(100, starting_render.get_width()+10) 
        destination_rect.w = max(100, destination_render.get_width()+10) 

        # display.flip() will update only a portion of the 
        # screen to updated, not full area 
        pygame.display.flip() 
        
        # clock.tick(60) means that for every second at most 
        # 60 frames should be passed. 
        clock.tick(60) 

        if eval == True: 
            z = [starting, destination]
            return z