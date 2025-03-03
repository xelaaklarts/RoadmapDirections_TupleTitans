from pygame import mouse
from pygame import key
from pygame import K_KP_PLUS
from pygame import K_KP_MINUS

def mouse_position():
    return mouse.get_pos()

def is_left_mouse_pressed():
    return mouse.get_pressed()[0]

def is_middle_mouse_pressed():
    return mouse.get_pressed()[1]

def is_right_mouse_pressed():
    return mouse.get_pressed()[2]

def is_plus_pressed():
    return key.get_pressed()[K_KP_PLUS]

def is_minus_pressed():
    return key.get_pressed()[K_KP_MINUS]