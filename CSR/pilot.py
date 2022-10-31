# from loadexp import Dataloads, fileloads, build_data
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



file = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022\1027 newenw\1012_NCMLTO_PVDF_activation_077\split\cycle_2.pqt"


path = Path(file)


file2 = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1028 ecsa drying condition\60 VAC\1\output\60 VAC@1_summary.xlsx"


path2 = Path(file2)



