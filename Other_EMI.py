# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:27:12 2022

@author: jycheon
"""

from loadexp import *
import pandas as pd
import os
import string
import numpy as np
from matplotlib import pyplot as plt
# plt.style.use('science')
year_path = "D:\\Researcher\\JYCheon\\DATA\\EMI"

class EMI_builder(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.df = pd.read_csv(self.file_path, skiprows = 8, encoding = "utf-8", sep = ' ' )
        self.df.columns = ["Frequency", "s11r", "s11i", "s21r", "s21i", "s12r", "s12i", "s22r", "s22i"]
        #convert Frequency (Hz) to GHz
        self.df["Frequency"] = self.df["Frequency"]/10**9
        
    def __str__(self):
        return self.name.replace("_", "-")
    
    def get_name(self):
        return self.name
        
        
    def get_calc(self):
        self.df["SE"] = 20*np.log10(1/np.sqrt(self.df["s21r"]**2 + self.df["s21i"]**2))
        self.df["SER"] = -10*np.log10(1-(self.df["s11r"]**2+ self.df["s11i"]**2))
        self.df["SEA"] = -10*np.log10((self.df["s21r"]**2+self.df["s21i"]**2)/(1-(self.df["s11r"]**2 + self.df["s11i"]**2)))
        
    def get_plot(self):
        
        plt.plot(self.df["Frequency"], self.df["SE"], "black", label = "$SE_{total}$")
        plt.plot(self.df["Frequency"], self.df["SEA"], "b", label = "$SE_{reflection}$")
        plt.plot(self.df["Frequency"], self.df["SER"], "r", label = "$SE_{absorption}$")
        plt.title(EMI_builder.__str__(self), fontsize = 10)
        plt.ylabel("Shielding effectiveness [dB]")
        plt.xlabel("Frequency (GHz)")
        plt.grid(visible = True, which = "major", axis = "y", color = "gray", linewidth = 0.5)
        plt.grid(visible = True, which = "minor", axis = "y", color = "gray", linestyle = '--', linewidth = 0.2)
        plt.legend(fontsize = 8)
        plt.show()

 
def get_export(path, exp):
    output_path = path + 'output\\'
    
    try:
        os.mkdir(output_path)    
    except FileExistsError:
        pass        
    for i in range(len(exp)):
        # writer = pd.ExcelWriter()
        # writer.close()
        with pd.ExcelWriter(output_path + exp[i].get_name() + '_corrected.xlsx') as writer:
            exp[i].df.to_excel(writer, sheet_name = 'corrected')


def main(default_path = year_path):
    
    raw_list, path, _ , _ = fileloads(default_path, '.s2p')
    exp_data = build_data(path, raw_list, EMI_builder)
    
    for exp in exp_data:
        exp.get_calc()
        exp.get_plot()
        
    get_export(path, exp_data)
    
if __name__ == "__main__":
    main()