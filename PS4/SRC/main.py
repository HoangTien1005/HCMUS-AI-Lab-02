import os
import sys
from KB import KB
from utils import *

INPUT_FOLDER_PATH = os.path.join(sys.path[0], "input")
OUTPUT_FOLDER_PATH = os.path.join(sys.path[0], "output")

if not os.path.exists(INPUT_FOLDER_PATH):
    print("Input folder not found!")
    exit()

path, dirs, files = next(os.walk(INPUT_FOLDER_PATH))

if len(files) == 0: 
    print("No input files found!")
    exit()

if not os.path.exists(OUTPUT_FOLDER_PATH):
    os.makedirs(OUTPUT_FOLDER_PATH)

for file in files:
    lines = read_files(os.path.join(INPUT_FOLDER_PATH, file))    
    alpha, clauses = data_structuring(lines)
    kb = KB(clauses)
    status, clauses_arr = PL_Resolution(kb, alpha)
    write_files(os.path.join(OUTPUT_FOLDER_PATH, file), status, clauses_arr, kb)
    kb.clear()

