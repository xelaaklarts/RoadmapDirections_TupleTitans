from pygame import mouse

def mouse_position():
    return mouse.get_pos()

def is_left_mouse_pressed():
    return mouse.get_pressed()[0]

def is_middle_mouse_pressed():
    return mouse.get_pressed()[1]

def is_right_mouse_pressed():
    return mouse.get_pressed()[2]