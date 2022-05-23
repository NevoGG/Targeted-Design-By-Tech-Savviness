import sys
import time
from tkinter import *
from tkinter import ttk
from BinaryClassification import *
import webbrowser

import openpyxl
import pandas as pd
import csv
import  TechSavvyDesign

import PostProcess
from PostProcess import *
from DataHandler import *
from LearningModule import *

TERMS_TEXT = "*I agree to the terms of service"
CONTENT_TEXT = "I agree to recieve sales & special offers via email"
NEWSLETTER_TEXT = "Sign me up for the FakeCorp newsletter"
BACKSPACE_KEYCODE = 8
ERROR_TXT = "Something went wrong, please fill form properly"
FAKE_LOGO = "assets/fake_logo.png"

WEIGHTS_DIR = "data_output/weights.csv"
DATA_DIR = "data_output/data_output.csv"
BACKSPACE_PRESSED = "backspace pressed"
FORM_MISTAKES_NUM = "form mistakes"
LEFT_CLICKS_MADE = "left clicks num"
TOTAL_TIME_MOUSE = "total time mouse"
KEYS_PRESSED = "keys pressed"
TOTAL_TIME_KEYS = "total time keys"
EXIT_TIME = "exit time"
TIMESTAMPS = "timestamps"
START_TIME = "start time"
MOUSE_COORDS = "mouse coords"
START_BUTTON_TXT = "Click here to start"
START_X = 630
START_Y = 300
Y_DIFF = 30
X_DIFF = 150
THRESHOLD = 7


class Form:
    keyword_dict = {num: 0 for num in range(1, 300)}  # dictionary of all keycodes.
    data_collection = dict
    has_started = bool
    left_mouse_clicked_time = int

    # UI objects:
    window = Tk()
    top_lvl = Toplevel()
    logo = PhotoImage(file=FAKE_LOGO)

    # interactive:
    first_name_box = Entry(window, bg="White")
    last_name_box = Entry(window)
    email_box = Entry(window)
    password_box_1 = Entry(window, show="*", bg="White")
    password_box_2 = Entry(window, show="*")
    age_slider = Scale(window, from_=5, to=90, orient=HORIZONTAL, background="white")
    terms_var = IntVar()
    terms_checkbox = Checkbutton(window, text=TERMS_TEXT, variable=terms_var, background="white")
    content_var = IntVar()
    content_checkbox = Checkbutton(window, text=CONTENT_TEXT, variable=content_var, background="white")

    # labels:
    logo_label = Label(window, image=logo, width=190, height=75)
    name_label = Label(window, text="*First Name", background="white")
    last_name_label = Label(window, text="*Last Name", background="white")
    email_label = Label(window, text="*Email", background="white")
    password_label = Label(window, text="*Password:", background="white")
    password2_label = Label(window, text="*Re enter password:", background="white")
    error_label = Label(window, text="", bg="white")

    def __init__(self):
        self.left_mouse_clicked_time = 0
        self.keyword_dict = {num: 0 for num in range(1, 300)}  # dictionary of all keycodes.
        self.data_collection = {
            BACKSPACE_PRESSED: 0,
            FORM_MISTAKES_NUM: 0,
            LEFT_CLICKS_MADE: 0,
            TOTAL_TIME_MOUSE: 0,
            KEYS_PRESSED: 0,
            TOTAL_TIME_KEYS: 0,
            START_TIME: 0,
            EXIT_TIME: 0,
            MOUSE_COORDS: []
        }

    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)

    def motion(self, event):
        x, y = event.x, event.y
        self.data_collection[MOUSE_COORDS].append({"xpos": x, "ypos": y, TIMESTAMPS: Form.current_milli_time()})

    def mouse_clicked(self, event):
        self.left_mouse_clicked_time = Form.current_milli_time()

    def on_mouse_up(self, event):
        self.data_collection[LEFT_CLICKS_MADE] += 1
        self.data_collection[TOTAL_TIME_MOUSE] += Form.current_milli_time() - self.left_mouse_clicked_time

    def log_key_pressed(self, event):
        key_code = event.keycode
        time_stamp = Form.current_milli_time()
        if self.keyword_dict.get(key_code) == 0:
            self.keyword_dict[key_code] = time_stamp

    def log_key_released(self, event):
        key_code = event.keycode
        time_stamp = Form.current_milli_time()
        if self.keyword_dict.get(key_code) != 0:
            self.data_collection[KEYS_PRESSED] += 1
            self.data_collection[TOTAL_TIME_KEYS] += time_stamp - self.keyword_dict.get(
                key_code)  # add duration of key press
            self.keyword_dict[key_code] = 0
            if key_code == BACKSPACE_KEYCODE:  # increment backspace uses
                self.data_collection[BACKSPACE_PRESSED] += 1

    def submit_form(self):
        is_fn = (self.first_name_box.get() != "")
        is_ln = (self.last_name_box.get() != "")
        is_email = (self.email_box.get() != "")
        is_password1 = (self.password_box_1.get() != "")
        is_password2 = (self.password_box_2.get() != "")
        is_terms = (self.terms_var.get())
        is_form_full = bool(is_fn and is_ln and is_email and is_password1 and is_password2 and is_terms)
        are_passwords_identical = (self.password_box_1.get() == self.password_box_2.get())
        if is_form_full and are_passwords_identical:
            self.data_collection[EXIT_TIME] = self.current_milli_time()
            self.window.destroy()
        else:
            self.error_label.config(text=ERROR_TXT)
            self.data_collection[FORM_MISTAKES_NUM] += 1

    def init_objects(self):
        self.logo_label.place(x=START_X + 45, y=START_Y - Y_DIFF * 4)
        self.window.title("Sign Up Form")
        self.window.attributes("-fullscreen", True)
        self.window.geometry("1000x1000")
        self.window.configure(background="white")
        self.name_label.place(x=START_X, y=START_Y)
        self.last_name_label.place(x=START_X, y=START_Y + Y_DIFF)
        self.email_label.place(x=START_X, y=START_Y + Y_DIFF * 2)
        self.email_label.place(x=START_X, y=START_Y + Y_DIFF * 3)
        self.password_label.place(x=START_X, y=START_Y + Y_DIFF * 5)
        self.password2_label.place(x=START_X,y=START_Y + Y_DIFF * 6)
        # set interactive objects location:
        self.first_name_box.place(x=START_X + X_DIFF, y=START_Y)
        self.last_name_box.place(x=START_X + X_DIFF, y=START_Y + Y_DIFF)
        self.email_box.place(x=START_X + X_DIFF, y=START_Y + Y_DIFF * 2)
        self.age_slider.place(x=START_X + X_DIFF, y=START_Y + Y_DIFF * 3)
        self.password_box_1.place(x=START_X + X_DIFF, y=START_Y + Y_DIFF * 5)
        self.password_box_2.place(x=START_X + X_DIFF, y=START_Y + Y_DIFF * 6)
        self.terms_checkbox.place(x=START_X, y=START_Y + Y_DIFF * 7)
        self.content_checkbox.place(x=START_X, y=START_Y + Y_DIFF * 8)
        submit_btn = ttk.Button(self.window, text="Submit", command=self.submit_form)
        submit_btn.place(x=START_X + 100, y=START_Y + Y_DIFF * 9)
        self.error_label.place(x=START_X, y=START_Y + Y_DIFF * 10)

    def init_binding(self):
        self.window.bind('<Motion>', self.motion)
        self.window.bind("<ButtonPress-1>", self.mouse_clicked)
        self.window.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.window.bind("<KeyPress>", self.log_key_pressed)
        self.window.bind("<KeyRelease>", self.log_key_released)

    def init(self):
        self.data_collection[START_TIME] = round(time.time() * 1000)
        self.init_objects()
        self.init_binding()
        self.window.mainloop()

    def get_raw_data(self):
        return self.data_collection




