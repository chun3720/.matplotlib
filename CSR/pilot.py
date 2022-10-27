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