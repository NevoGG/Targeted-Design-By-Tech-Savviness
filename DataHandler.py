import openpyxl
import pandas as pd
import csv
import PostProcess
from PostProcess import *

SHEET_NAME = "data"
NEW_SHEET = "Sheet1"
MOTION_FOLDER_DIR = "data_output/mouse_motion_outputs/"
SUBJECT_NUM_DIR = "data_output/subj_num.txt"
EXCEL_DIR = "data_output/output.xlsx"
OUTPUT_DIR = "data_output/data_output.csv" # todo: enter output file


def get_subject_num():
    f = open(SUBJECT_NUM_DIR, 'r')
    subject_num_str = f.readline()
    f.close()
    return int(subject_num_str)


def set_subject_num(subject_num):
    f = open(SUBJECT_NUM_DIR, 'w')
    f.write(str(subject_num))
    f.close()


def write_to_csv(post_processed):
    print(post_processed)
    df = pd.read_csv(OUTPUT_DIR)
    df = df.append(post_processed, ignore_index=True)
    df.head(10)
    df.to_csv(OUTPUT_DIR, index = False)

