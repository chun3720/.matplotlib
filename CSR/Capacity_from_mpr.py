# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:19:55 2022

@author: user
"""
import os
import pandas as pd
from galvani import BioLogic
from loadexp import Dataloads, fileloads, build_data
import matplotlib.pyplot as plt
import numpy as np

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"

class Raw_mpr(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        
        mpr_file = BioLogic.MPRfile(str(self.file_path))
        self.raw = pd.DataFrame(mpr_file.data)
        
        cols = ["time/s", "control/mA", '<Ewe>/V', 'dQ/mA.h', 'half cycle' ]
        
        self.df = self.raw[cols]
        
        self.df.columns  = ["Time", "Curr", "Volt", "Cap", "num"]
        
        
        
    def get_separation(self):
        
        title = self.name
        cycles = self.df.num.unique()
        
        charge_dfs = []
        discharge_dfs = []
        cols = ["Cap", "Volt"]
        tot_df = pd.DataFrame()
        header_tot = []
        discharge_caps = []
        
        for cy in cycles:
            if cy%2 == 1:
                dis = self.df[self.df.num == cy][cols]
                # dis.loc["Cap"] =  -dis.loc["Cap"]
                dis.Cap = -dis.Cap
                discharge_dfs.append(dis)
                # discharge_dfs.append(self.df[self.df.num == cy])
            else:
                charge_dfs.append(self.df[self.df.num == cy])
                
        cy_nums = len(charge_dfs)
        
        for i, charge, discharge in zip(range(cy_nums), charge_dfs, discharge_dfs):
            
            cy_df = pd.concat([charge[cols].reset_index(drop = True), discharge[cols].reset_index(drop = True)], axis =1)
            tot_df = pd.concat([tot_df, cy_df], axis = 1)
            
            dc_point =  discharge.index[-1]
            dc_cap = discharge.Cap.loc[dc_point]
            discharge_caps.append(dc_cap)
            header = [f"{title}_Qc{i+1}", f"{title}_Vc{i+1}", f"{title}_Qd{i+1}", f"{title}_{i+1}"]
            header_tot += header
            
                
        tot_df.columns = header_tot

        
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
    hdf_file = f"{output_path}\\Capacity_tot.hdf5"
    tot_df.to_pickle(report_file)
    tot_df.to_hdf(hdf_file, key = "tot_df", mode = "w")
    tot_caps = np.array(tot_caps)
    
    loading = 16 # mg
    
    dc_caps_specific = tot_caps * 1000 / loading
    
    indx = [_ +1 for _ in range(len(dc_caps_specific))]
    dc_caps_df = pd.DataFrame({"cycles": indx, "Capacity (mAh/g)" : dc_caps_specific})
    # dc_caps_df = pd.DataFrame(dc_caps_specific, index = range(len(dc_caps_specific)))
    dc_caps_df.to_csv(f"{output_path}\\cycles.csv")
    dc_caps_df.to_excel(f"{output_path}\\Cycle_tot.xlsx", index = "cycles" )
    
    cols = tot_df.columns
    
    for i in range(0, len(cols), 2):
        plt.plot(tot_df[cols[i]], tot_df[cols[i+1]])
        
    plt.show()
    
    dc_caps_df.plot.scatter(x = "cycles", y = "Capacity (mAh/g)")
    
    plt.show()
    
    
        
        
def main(date_path = year_path):
    
    raw_list, path, _, _ = fileloads(date_path, '.mpr')
    exp_obj = build_data(path, raw_list, Raw_mpr)                
                    
    
    get_report(exp_obj, path)
    
    
if __name__ == "__main__":
    main(year_path)
        
        
        
  