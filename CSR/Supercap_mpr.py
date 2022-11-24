# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 17:20:28 2022

@author: user
"""

import os
import pandas as pd
from galvani import BioLogic
from loadexp import Dataloads, fileloads, build_data
import matplotlib.pyplot as plt
import numpy as np
from Supycap import Load_capacitor

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"



class Sep_csv(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        self.df = pd.read_csv(self.file_path)
        
        
        self.check_point = self.df.loc[0, "Time"]
        
        self.df["Time"] = self.df["Time"] - self.check_point
        
        
class Raw_mpr(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        
        mpr_file = BioLogic.MPRfile(str(self.file_path))
        self.raw = pd.DataFrame(mpr_file.data)
        
        cols = ["time/s", "control/mA", '<Ewe>/V', 'dQ/mA.h', 'half cycle' ]
        
        self.df = self.raw[cols]
        
        self.df.columns  = ["Time", "Curr", "Volt", "Cap", "num"]
        
        self.output_path = os.path.join(self.path, "supercap")
        
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        
        self.sep_path = os.path.join(self.path, "GCD_last")
        
        if not os.path.exists(self.sep_path):
            os.mkdir(self.sep_path)
        
    
    def get_info(self):
        
        self.appl_current = self.df.loc[0]["Curr"]
        
        return self.appl_current # unit : mA
    

        
        
    def get_separation(self):
        
        title = self.name
        self.cycles = self.df.num.unique()
        
        charge_dfs = []
        discharge_dfs = []
        cols = ["Time", "Volt"]
        tot_df = pd.DataFrame()
        # header_tot = []
        # discharge_caps = []
        
        for cy in self.cycles:
            if cy%2 == 1:
                dis = self.df[self.df.num == cy][cols]
                # dis.loc["Cap"] =  -dis.loc["Cap"]
                # dis.Cap = -dis.Cap
                discharge_dfs.append(dis)
                # discharge_dfs.append(self.df[self.df.num == cy])
            else:
                charge_dfs.append(self.df[self.df.num == cy])
                
        cy_nums = len(charge_dfs)
        
        
        
        for i, charge, discharge in zip(range(cy_nums), charge_dfs, discharge_dfs):
            
            cy_df = pd.concat([charge[cols].reset_index(drop = True), discharge[cols].reset_index(drop = True)], axis =0)
            
            if i == cy_nums -1:
                cy_df.to_csv(f"{self.sep_path}\\{title}_cycle_{i+1}.csv")
                
            
            # cy_df.to_csv(f"{self.path}\\{title}_cycle_{i+1}.csv")
            tot_df = pd.concat([tot_df, cy_df], axis = 0)
            
            # dc_point =  discharge.index[-1]
            # dc_cap = discharge.Cap.loc[dc_point]
            # discharge_caps.append(dc_cap)
            # header = [f"{title}_Qc{i+1}", f"{title}_Vc{i+1}", f"{title}_Qd{i+1}", f"{title}_{i+1}"]
            # header_tot += header
        tot_file = f"{self.output_path}\\{title}.txt"
        tot_df.to_csv(tot_file, index = False, sep = " ")
        
        return (tot_file, self.sep_path)
            
                

raw_list, path, _, _ = fileloads(year_path, '.mpr')
exp_obj = build_data(path, raw_list, Raw_mpr, False)                

for exp in exp_obj:
    tot_txt_file, sep_path = exp.get_separation()
    curr = exp.get_info()
    supercap = Load_capacitor(tot_txt_file, ESR_method =2, current = curr, cap_grav = False, cap_method = 2)
    supercap2 = Load_capacitor(tot_txt_file, ESR_method =2, current = curr, cap_grav = False, cap_method = 1)
    supercap.Check_analysis(begin = 1, end = len(exp.cycles)//2 -1)
    
    plt.title(f"{exp.name}")
    plt.show()
    supercap2.Check_analysis(begin = 1, end = len(exp.cycles)//2 -1)
    cap_results = np.array(supercap.cap_ls)
    cap_results2 = np.array(supercap2.cap_ls)
    plt.figure(figsize = (4, 3))
    plt.scatter(range(cap_results.shape[0]), cap_results*1000, marker = 'o', c = "r")
    plt.scatter(range(cap_results2.shape[0]), cap_results2*1000, marker = 'o', c = "b")
    plt.xlabel("number of cycles")
    plt.ylabel("Capacitance (mF)")
    plt.title(f"{exp.name}")
    plt.show()
    # supercap.Cap_vs_cycles()
    
    
sep_files = [_ for _ in os.listdir(sep_path) if _.endswith("csv")]

sep_obj = build_data(sep_path, sep_files, Sep_csv)

plt.style.use(['science', 'no-latex'])
for sep in sep_obj:
    plt.plot(sep.df.Time, sep.df.Volt)
    
plt.xlabel("Time (s)")    
plt.ylabel("Voltage (V)")

# f = exp_obj[0].get_separation()

# curr = exp_obj[0].get_info()


# supercap1 = Load_capacitor(f, ESR_method =2, current = curr, cap_grav = False)