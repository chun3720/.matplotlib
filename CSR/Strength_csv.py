# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:07:06 2022

@author: user
"""
import os



import sys
from pathlib import Path
curr_path = os.getcwd()
parent_path = Path(curr_path).parent
sys.path.append(str(parent_path))

# from CSR import loadexp

from CSR.loadexp import *

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


year_path = r"D:\Researcher\JYCheon\DATA\Strength"




class Strength(Dataloads):
    
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)      
        self.raw = pd.read_csv(self.file_path, skiprows= 1, index_col = 0, encoding = "cp949")   
        
    def get_data(self):      
        avg = self.raw.loc["평균"]
        var = self.raw.loc["편차"]       
        ans = [a + ' ± ' + b if float(b) != 0 else a for a, b in zip(avg, var) ]
            
        return ans
    
    def get_avg(self):
        
        return self.raw.loc["평균"]
    


def get_export(exp_obj, path):
    
    output_path = os.path.join(path, "output")
    
    # output_path = f'{path}\\output\\'

    if not os.path.exists(output_path):
        os.mkdir(output_path)
      
    names, d = [], []
    
    header = ["선형 밀도 (tex)", "길이 (mm)", "Load (N)", "Specific Strength (N/tex)",
                  "Stiffness (N/tex)",  "Strain (%)", "Toughness (mJ)" ]
                  
    for exp in exp_obj:
        names.append(exp.name[:-16])
        d.append(exp.get_data())
    file2write = os.path.join(output_path, "data_tot.xlsx")
    with pd.ExcelWriter(file2write) as writer:
        pd.DataFrame(data = d, columns = header, index = names).to_excel(writer)
        


def get_graph(exp_obj, path):
    output_path = os.path.join(path, "output")
    
    names = []

    df = pd.DataFrame()
    
    for exp in exp_obj:
        names.append(exp.name[:-16])
        df = pd.concat([df, exp.get_avg()], axis = 1, ignore_index =  True)       
    
    df = df.T.set_index(pd.Index(names))   
    
    df.columns = ["선형 밀도 (tex)", "길이 (mm)", "Load (N)", "Specific Strength (N/tex)",
                  "Stiffness (N/tex)",  "Strain (%)", "Toughness (mJ)" ]                
    
    df1 = df[ ["Load (N)", "Specific Strength (N/tex)", "Stiffness (N/tex)",  "Strain (%)"]  ].astype(float)
    
  
    angle = 30
    
    for col in df1.columns:
        
        ax = sns.barplot(x = df.index, y = col, data = df1)
        ax.set_xticklabels(names, fontsize = 8, rotation = angle)
        file2fig = os.path.join(output_path, f"{col[:8]}.png")
        plt.savefig(file2fig, dpi = 300)
        plt.show()
        
   
    ax = df1.plot(kind = "bar",  y = "Specific Strength (N/tex)", color = 'k')
    plt.ylabel("S.S (N/tex)")
    h = df1["Specific Strength (N/tex)"]
    plt.ylim(0, max(h)*1.5)
    
    ax5 = df1.plot(kind = "bar",  y = "Stiffness (N/tex)", secondary_y = True, ax = ax, color = 'r', align = 'edge')
    plt.ylabel("Stiffness (N/tex)")
    ax.set_xticklabels(names, fontsize = 8, rotation = angle)
    k = df1["Stiffness (N/tex)"]
    plt.ylim(0, max(k)*1.5)
    file2doubleY = os.path.join(output_path, "doubleY.png")
    plt.savefig(file2doubleY, dpi = 300)
    
    
 
def main(date_path = year_path):
    plt.style.use(["science", "no-latex"])

    raw_list, path, _, _ = fileloads(date_path, '.csv')
    exp = build_data(path, raw_list, Strength)
    
    get_export(exp, path)
    
    get_graph(exp, path)
    
if __name__ == "__main__":
    
    main()


