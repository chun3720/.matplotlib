# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:07:06 2022

@author: user
"""

from loadexp import *

import pandas as pd
import os
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
    
    
    def export_Load(self):
        
        return self.raw.loc["평균", "Load"]
    
    def export_Str(self):
        
        return self.raw.loc["평균", "Specific strength"]
    
    def export_Stiff(self):
        
        return self.raw.loc["평균", "Stiffness"]
    
    def export_Strain(self):
        
        return self.raw.loc["평균", "Strain"]
        
        
        
        
       

def get_export(exp_obj, path):
    
    output_path = f'{path}\\output\\'

    if not os.path.exists(output_path):
        os.mkdir(output_path)
        
    
    exp_name = []
    lin_density = []
    length = []
    load = []
    specific_str = []
    stiff = []
    strain = []
    tough = []
    
    
    for exp in exp_obj:
        
        full = exp.get_data()
        exp_name.append(exp.name[:-16])
        lin_density.append(full[0])
        length.append(full[1])
        load.append(full[2])
        specific_str.append(full[3])
        stiff.append(full[4])
        strain.append(full[5])
        tough.append(full[6])
        
               
    
    header = ["선형밀도 (tex)", "길이 (mm)", "Load (N)", "Specific strength (N/tex)", "Stiffness (N/tex)",
              "Strain (%)", "Toughness (mJ)"]
    
    d = {header[0] : lin_density, 
         header[1] : length,
         header[2] : load,
         header[3] : specific_str,
         header[4] : stiff,
         header[5] : strain,
         header[6] : tough
         
         }
    
    df_raw = pd.DataFrame(data = d, index = exp_name)

    
    with pd.ExcelWriter(f'{output_path}\\data_tot.xlsx') as writer:
        df_raw.to_excel(writer)
        
        
        
        
def get_load_plot(exp_obj, path):
    output_path = f'{path}\\output\\'
    Load = []
    Strs = []
    Stifs = []
    Strains = []
    names = []
    
        
    for exp in exp_obj:
    
        names.append(exp.name[:-16])
        Load.append( float(exp.export_Load() ) )
        Strs.append(float(exp.export_Str() ) )
        Stifs.append(float(exp.export_Stiff() ) )
        Strains.append( float(exp.export_Strain() )   )
              

    df = pd.DataFrame ({"Load (N)" :  Load,
                        "Specific Strength (N/Tex)" : Strs,
                        "Stiffness (N/Tex)" : Stifs,
                        "Strain (%)" : Strains,
                        # }, index = range(len(Load)))    
                        }, index = names)

    
    
    # names = ["EtOH", "DP/EtOH/1:50", "Water", "Acetone", "DMSO"]
    
    angle = 30
   
    ax1 = sns.barplot(x = df.index, y = "Load (N)", data = df)
    ax1.set_xticklabels(names, fontsize = 8, rotation = angle)
    plt.savefig(f"{output_path}Load.png", dpi = 300)
    # plt.title("220727")
    plt.show()

    ax2 = sns.barplot(x = df.index, y = "Specific Strength (N/Tex)", data = df)
    ax2.set_xticklabels(names, fontsize = 8, rotation = angle)
    plt.savefig(f"{output_path}Strength.png", dpi = 300)
    plt.show()
    
    ax3 = sns.barplot(x = df.index, y = "Stiffness (N/Tex)", data = df)
    ax3.set_xticklabels(names, fontsize = 8, rotation = angle)
    plt.savefig(f"{output_path}Stiffness.png", dpi = 300)
    plt.show()
    
    ax4 = sns.barplot(x = df.index, y = "Strain (%)", data = df)
    ax4.set_xticklabels(names, fontsize = 8, rotation = angle)
    plt.savefig(f"{output_path}Strain.png", dpi = 300)
    plt.show()
    
   
    ax = df.plot(kind = "bar",  y = "Specific Strength (N/Tex)", color = 'k')
    plt.ylabel("S.S (N/Tex)")
    h = df["Specific Strength (N/Tex)"]
    plt.ylim(0, max(h)*1.5)
    
    ax5 = df.plot(kind = "bar",  y = "Stiffness (N/Tex)", secondary_y = True, ax = ax, color = 'r', align = 'edge')
    plt.ylabel("Stiffness (N/Tex)")
    ax.set_xticklabels(names, fontsize = 8, rotation = angle)
    k = df["Stiffness (N/Tex)"]
    plt.ylim(0, max(k)*1.5)
    plt.savefig(f"{output_path}doubleY.png", dpi = 300)
    
    
    


raw_list, path, _, _ = fileloads(year_path, '.csv')
exp = build_data(path, raw_list, Strength)

get_export(exp, path)

get_load_plot(exp, path)




