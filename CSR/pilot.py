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


n = 18

for i in range(2, n, 3):
    
    print(i)