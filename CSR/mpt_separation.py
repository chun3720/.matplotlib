# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 16:01:48 2022

@author: user
"""

import re, os
import pandas as pd
from loadexp import Dataloads, fileloads, build_data
# from pathlib import Path
import numpy as np




raw = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1101 NCMLTO PVDF pouch GB fab-2\1101 NCMLTO PVDF pouch GB fab LT10ET50 1103 wo 5kg.mpt"

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"



class EC_measurement(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        method_dict = {'Constant Current\n' : "GCD", 'Cyclic Voltammetry\n' : "CV"}
        self.method = ''
        
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            self.method = method_dict[lines[3]]
            h = re.findall('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', lines[1])

        self.header = int(h[0])     
        
        if self.method == "GCD":
            self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = "\t", header = 0\
                                  , usecols = ["time/s", "control/mA", '<Ewe>/V', 'Capacity/mA.h', 'cycle number' ])
        
        elif self.method == "CV":
            self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = "\t", header = 0\
                                  , usecols = ["time/s", "control/V", "Ewe/V", "<I>/mA", "cycle number"])
                
        self.df.columns = ["Time", "Curr", "Volt", "Cap", "num"]
        
        
    def get_separation(self):
        
        title = self.name
        cycles = self.df.num.unique()
        cols = ["Cap", "Volt"]
        tot_df = pd.DataFrame()
        header_tot = []
        discharge_caps = []
        for i, cycle in enumerate(cycles):
            df = self.df[self.df.num == cycle]
            # sep_dfs.append(self.df[self.df.num == cycle])
            
            charge = df[df.Curr >0]
            discharge = df[df.Curr < 0]
            cy_df = pd.concat([charge[cols].reset_index(drop = True), discharge[cols].reset_index(drop = True)], axis =1)
            tot_df = pd.concat([tot_df, cy_df], axis = 1)
            
            dc_point =  discharge.index[-1]
            dc_cap = discharge.Cap.loc[dc_point]
            discharge_caps.append(dc_cap)
            # print(dc_cap)
            
            
            header = [f"{title}_Qc{i+1}", f"{title}_Vc{i+1}", f"{title}_Qd{i+1}", f"{title}_{i+1}"]
            header_tot += header
            
            
        tot_df.columns = header_tot
        # print(tot_df)
            
            
        return (tot_df, discharge_caps)
            
        
def get_report(exp_obj, path):
    
    tot_df = pd.DataFrame()
    
    output_path = f"{path}\\output\\"
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    tot_caps = []
    for exp in exp_obj:
        exp_df, exp_caps = exp.get_separation()
        tot_df = pd.concat([tot_df, exp_df], axis = 1)
        tot_caps += exp_caps
        
    
    report_file = f"{output_path}\\Capacity_tot.pkl"
    
    tot_df.to_pickle(report_file)
    
    tot_caps = np.array(tot_caps)
    
    loading = 16 # mg
    
    dc_caps_specific = tot_caps * 1000 / loading
    
    dc_caps_df = pd.DataFrame(dc_caps_specific)
    dc_caps_df.to_csv(f"{output_path}\\cycles.csv")

        
        
    
        
        
raw_list, path, _, _ = fileloads(year_path, '.mpt')
exp_obj = build_data(path, raw_list, EC_measurement)                
                

get_report(exp_obj, path)

# 
# file_object = Path(raw)

# path = file_object.parent
# file = file_object.name

# exp_obj = EC_measurement(path, file)

# dfs = exp_obj.get_separation()
