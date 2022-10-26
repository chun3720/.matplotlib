from loadexp import Dataloads, fileloads, build_data
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
from pathlib import Path
from tqdm import tqdm

from datetime import date


a = date.today()
b = date.isoformat(a)

c = b.replace("-", "")

year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"


f = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022\1025 csv test\New Folder\output\cycle_1.pkl"

path, file = os.path.split(f)



df = pd.read_pickle(f)
