# Import required libraries
from pygame import key
from pygame import event
# Stand for key down and key up events
# They apply to all mouse buttons
from pygame import MOUSEBUTTONUP
from pygame import MOUSEBUTTONDOWN
from pygame import MOUSEMOTION

# Get key event
def keys_list():
    return key.get_pressed()

# Get event list
def event_list():
    return event.get()

# Get mouse position
def mouse_position(current_mouse_pos, events):
    for event in events:
        if event.type == MOUSEMOTION:
            return event.pos
    return current_mouse_pos

# Get left mouse event
def is_left_mouse_pressed(left_mouse_pressed, events):
    for event in events:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:   
                left_mouse_pressed = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:   
                left_mouse_pressed = False
    return left_mouse_pressed

# Get middle mouse event
def is_middle_mouse_pressed(middle_mouse_pressed, events):
    for event in events:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 2:   
                middle_mouse_pressed = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 2:   
                middle_mouse_pressed = False
    return middle_mouse_pressed

# Get right mouse event
def is_right_mouse_pressed(right_mouse_pressed, events):
    for event in events:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:   
                right_mouse_pressed = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 3:   
                right_mouse_pressed = False
    return right_mouse_pressed

# Get mouse button up event
def if_mousewheelup(events):
    for event in events:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:   
                return True
            else:
                return False

# Get mouse button down event
def if_mousewheeldown(events):
    for event in events:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5:   
                return True
            else:
                return False