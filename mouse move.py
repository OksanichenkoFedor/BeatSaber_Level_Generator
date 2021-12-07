import ctypes
import random
import time
import math


def move_mouse(pos):
    x_pos, y_pos = pos
    screen_size = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    x = 65536 * x_pos / screen_size[0] + 1
    y = 65536 * y_pos / screen_size[1] + 1
    return ctypes.windll.user32.mouse_event(32769, int(x), int(y), 0, 0)



def random_movement(top_left_corner, bottom_right_corner, min_speed=100, max_speed=200):
    '''speed is in pixels per second'''



    x_bound = top_left_corner[0], bottom_right_corner[0]
    y_bound = top_left_corner[1], bottom_right_corner[1]



    pos = (random.randrange(*x_bound),
                    random.randrange(*y_bound))



    speed = min_speed + random.random()*(max_speed-min_speed)
    direction = 2*math.pi*random.random()



    def get_new_val(min_val, max_val, val, delta=0.01):
        new_val = val + random.randrange(-1,2)*(max_val-min_val)*delta
        if new_val<min_val or new_val>max_val:
            return get_new_val(min_val, max_val, val, delta)
        return new_val



    steps_per_second = 35.0
    while True:
        move_mouse(pos)
        time.sleep(1.0/steps_per_second)



        speed = get_new_val(min_speed, max_speed, speed)
        direction+=random.randrange(-1,2)*math.pi/5.0*random.random()



        new_pos = (int(round(pos[0]+speed*math.cos(direction)/steps_per_second)),
               int(round(pos[1]+speed*math.sin(direction)/steps_per_second)))



        while new_pos[0] not in range(*x_bound) or new_pos[1] not in range(*y_bound):
            direction  = 2*math.pi*random.random()
            new_pos = (int(round(pos[0]+speed*math.cos(direction)/steps_per_second)),
               int(round(pos[1]+speed*math.sin(direction)/steps_per_second)))
        pos=new_pos
time.sleep(5)
random_movement((300,300),(600,600))