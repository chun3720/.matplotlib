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


class LIB_csv(Dataloads):  
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.df = pd.read_parquet(self.file_path) 
        self.X, self.Y  = self.df.columns[0], self.df.columns[1]
        self.null = self.df[self.df[self.X] == 0].index
        self.df = self.df.drop(self.null)
        self.min = self.df[self.Y].idxmin()
        self.max = self.df[self.Y].idxmax()
        self.positive = None
        self.negative = None
    
    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def df_indexing(self):
        if self.df.iloc[0, 1] > self.df.iloc[3, 1]:
            self.negative = self.df.loc[:self.min]
            self.positive = self.df.loc[self.min+1 :]  
        else:
            self.positive = self.df.loc[:self.max]
            self.negative = self.df.loc[self.max +1 :]
            
    def get_name(self):
        return self.name
              
    def get_discharge(self):
        return self.df.loc[self.max]
        
    def get_charge(self):
        return self.df.loc[self.min]
    
    def GCD_plot(self, color):
        plt.plot(self.negative[self.X], self.negative[self.Y], color, label = LIB_csv.__str__(self))
        plt.plot(self.positive[self.X], self.positive[self.Y], color )

f = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022\1011 LYM\test1\split\cycle2.pqt"

path, file = os.path.split(f)

exp = LIB_csv(path, file)

x, y = exp.df.columns
# exp.df.plot(x= x, y = y)

exp.df_indexing()

# exp.positive.plot(x = x, y = y)
