# R stuff setup:
import openpyxl
import pandas as pd
import numpy as np
# from form_ui import *

TOTAL_TIME_MOUSE = "total time mouse"
KEYS_PRESSED = "keys pressed"
TOTAL_TIME_KEYS = "total time keys"
EXIT_TIME = "exit time"

BACKSPACE_PRESSED = "backspace pressed"
FORM_MISTAKES_NUM = "form mistakes"
LEFT_CLICKS_MADE = "left clicks num"
AVG_TIME_PER_CLICK = "avg time per click"
AVG_TIME_PER_KEY = "avg press time per key"
TOTAL_TIME = "total time"
TOTAL_DISTANCE_MOUSE = "total mouse distance"
MAX_VELOCITY = "max velocity"
TIMESTAMPS = "timestamps"
START_TIME = "start time"
MOUSE_COORDS = "mouse coords"

#constants:
VELOCITY_TIME_CONST = 100  # miliseconds
NORM_THRESHOLD = 1

"""
:param mouse_coords: a pandas DataFrame object
:param test_num: number of test subject
"""


def calc_avg_click_time(mouse_clicks, mouse_time):
    return mouse_clicks / mouse_time


def calc_avg_key_time(key_pressed, key_time):
    return key_pressed / key_time


def get_total_distance_moved(mouse_coords):
    total_dist = 0
    for i in range(len(mouse_coords) - 1):
        this_coord = [[mouse_coords[i]["xpos"]], [mouse_coords[i]["ypos"]]]
        next_coord = [[mouse_coords[i + 1]["xpos"]], [mouse_coords[i + 1]["ypos"]]]
        dist_vector = np.subtract(this_coord, next_coord)
        dist_norm = np.linalg.norm(dist_vector)
        if dist_norm > NORM_THRESHOLD:
            total_dist += np.linalg.norm(dist_vector)
    return total_dist


"""calculates max velocity of mouse movement per time constant """


def get_max_velocity(mouse_coords):
    max_velocity = 0
    cur_velocity = 0
    i = 0
    while i < len(mouse_coords) - 50:
        start = i
        while mouse_coords[i][TIMESTAMPS] - mouse_coords[start][TIMESTAMPS] < VELOCITY_TIME_CONST:
            i += 1
        dist_moved_in_time_span = get_total_distance_moved(mouse_coords[start:i+1])
        cur_velocity = dist_moved_in_time_span / VELOCITY_TIME_CONST
        if max_velocity < cur_velocity:
            max_velocity = cur_velocity
    return max_velocity


def process_raw_data(raw_collected):
    result_map = {
        BACKSPACE_PRESSED: raw_collected[BACKSPACE_PRESSED],
        FORM_MISTAKES_NUM: raw_collected[FORM_MISTAKES_NUM],
        LEFT_CLICKS_MADE: raw_collected[LEFT_CLICKS_MADE],
        AVG_TIME_PER_CLICK: calc_avg_click_time(raw_collected[LEFT_CLICKS_MADE],
                                                raw_collected[TOTAL_TIME_MOUSE]),
        AVG_TIME_PER_KEY: calc_avg_key_time(raw_collected[KEYS_PRESSED],
                                            raw_collected[TOTAL_TIME_KEYS]),
        TOTAL_TIME: raw_collected[EXIT_TIME] - raw_collected[START_TIME],
        TOTAL_DISTANCE_MOUSE: get_total_distance_moved(raw_collected[MOUSE_COORDS]),
        MAX_VELOCITY: get_max_velocity(raw_collected[MOUSE_COORDS])
    }
    return result_map
