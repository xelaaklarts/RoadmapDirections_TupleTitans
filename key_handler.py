from pygame import mouse

def mouse_position():
    return mouse.get_pos()

def is_mouse_pressed():
    return mouse.get_pressed()[0]