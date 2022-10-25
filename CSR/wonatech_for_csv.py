# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:28:27 2022

@author: user
"""
from loadexp import Dataloads, fileloads, build_data
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
from pathlib import Path
from tqdm import tqdm

# plt.style.use('science')
plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"


class LIB_tot(Dataloads):   
    
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.raw = pd.read_csv(self.file_path, skiprows= 10)
        
        
        
        


# raw, path, _, _ = fileloads(year_path, "csv")
# exp_obj = build_data(path, raw, LIB_tot)

f = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022\1025 csv test\New Folder\1012_NCMLTO_PVDF_nonactivation_078_DC.csv"

df = pd.read_csv(f, delimiter = ',', encoding = "cp949", skiprows = 10, index_col= 0, \
                 usecols = ["Index", "Cycle_No.", "Step_No.", 'Voltage(V)', '|Q|(Ah)'] )

# df.plot(y = "Voltage(V)", x = "|Q|(Ah)")

df.columns  = ["n", "step", "volt", "q"]

# test = df.groupby("Cycle_No.")
total_cycle = len(df.groupby("n"))

# tot_df = pd.DataFrame()
# for i in range(total_cycle):
#     j = i+1
#     cy = df[df.n == j]
#     (
      
      
      
#       df = pd.concat([cy[cy.step ==1].reset_index(drop = True), cy[cy.step ==3].reset_index(drop = True)] , axis = 1, ignore_index = True)
    
    
    
    


cycle1 = df[df.c == 1]
charge = cycle1[cycle1.s==1]
discharge = cycle1[cycle1.s ==3]


plt.plot(charge.q, charge.v)
plt.plot(discharge.q, discharge.v)
