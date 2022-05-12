# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:44:33 2022

@author: user
"""

from loadexp import *
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['science', 'no-latex'])
year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2021\Raw"


class DLC_builder(Dataloads):
    dlc_current = []
    dlc_rate = []
    
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            header = lines[1][18:20]  
            
        self.header = int(header)
        self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = '\t', header = 0)
        

        self.df.drop(columns = ['mode', 'ox/red', 'error', 'counter inc.', 'P/W', 'Unnamed: 12' ], inplace = True)
        t1, v1 = self.df[["time/s", "control/V"]].loc[1]
        t2, v2 = self.df[["time/s", "control/V"]].loc[2]
        
        self.scan_rate =  (v2-v1) / (t2-t1) 
        self.scan_rate_unit = "V/s"
        
    def shift_to_OCP(self):
        self.ocp = self.df["Ewe/V"].loc[0]
        self.df["Ewe/V"] -= self.ocp
        
    def get_rate(self):
        """
        convert scan rate to mV/s
        """
        self.rate = round(self.scan_rate *1000)
        DLC_builder.dlc_rate.append(int(self.rate))
        
    def get_dlc(self):
        cols = ["Ewe/V", "<I>/mA"]
        self.filt = self.df[self.df["Ewe/V"] < 0].index
        self.dlc = self.df[cols].drop(self.filt)
        k = self.dlc.shape[0]
        self.point = (self.dlc["<I>/mA"].loc[0] - self.dlc["<I>/mA"].loc[k-1]) /2
        # self.min = self.dlc.loc[2: "Ewe/V"].idxmin()
        # self.point = (self.dlc.loc[0, '<I>/mA'] - self.dlc.loc[self.min, '<I>/mA'])/2
        DLC_builder.dlc_current.append(self.point)
        
    def dlc_fit(self):
        self.X = np.array(DLC_builder.dlc_rate)
        self.Y = np.array(DLC_builder.dlc_current)
        n = len(self.X)
        A = np.vstack((self.X, np.ones(n))).T
        XX, resid, _, _ = np.linalg.lstsq(A, self.Y, rcond = None)
        self.slope, self.intercept = XX
        
    def get_dlc_result(self):
        dlc_rs = pd.DataFrame({'Scan rate (mV/s)' : self.X, 'DLC current (mA)' : self.Y, 'Fitted (mA)' : self.slope*self.X})
        dlc_rs.set_index('Scan rate (mV/s)', inplace = True)
        dlc_rs.loc[5, 'Total Capacitance (uF)'] = self.slope*1000000
        dlc_rs.loc[5, 'Length Capacitance (uF/cm)'] = self.slope*1000000/3
        return dlc_rs
    
    def dlc_plot(self):
        plt.scatter(self.X, self.Y)
        length_cap = int(self.slope * 1000000/3)
        label = f'{length_cap} uF/cm'
        plt.plot(self.X, self.slope*self.X + self.intercept, 'r-', label = label)
        plt.legend()
            
        
def get_plot(exp_obj, exp_name):
    
    for exp in exp_obj:
        exp.shift_to_OCP()
        exp.get_rate()
        exp.get_dlc()
        plt.plot(exp.df["Ewe/V"], exp.df["<I>/mA"])
        plt.title(exp_name)
        plt.xlabel('Potential (V vs. OCP)')
        plt.xlim(-0.06, 0.06)
        plt.ylabel('Current (mA)')
        
    plt.show()
    
def get_DLCplot(path, exp_obj, exp_name):
    
    output_path = os.path.join(path, 'output\\')
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    exp_obj[-1].dlc_fit()
    dlc_df = exp_obj[-1].get_dlc_result()
    exp_obj[-1].dlc_plot()
    plt.title(exp_name)
    plt.xlabel('Scan Rate (mV/s)')
    plt.xlim(0, 60)
    plt.ylabel('DLC Current (mA)')
    
    plt.savefig(f'{output_path}{exp_name}.png', dpi = 300)
    plt.plot()
    
    return dlc_df
    
def get_export(path, exp_obj, dlc_df, exp_name):
    output_path = os.path.join(path, "output\\")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with pd.ExcelWriter(f'{output_path}{exp_name}_summary.xlsx') as writer:
        for i, exp in enumerate(exp_obj):
            label = f'{exp.rate} mV/s'
            exp.df[["Ewe/V", "<I>/mA"]].to_excel(writer, sheet_name = 'CV', startcol = 2*i, index = False, header = [f'{i}', label])
        dlc_df.to_excel(writer, sheet_name = 'DLC')
    

def main(date_path = year_path):
        
    raw_list, path_dir, exp_name, exp_title = fileloads(date_path, '.mpt')
    exp_obj = build_data(path_dir, raw_list, DLC_builder)
    
    get_plot(exp_obj, exp_name)
    dlc_df = get_DLCplot(path_dir, exp_obj, exp_name)
    get_export(path_dir, exp_obj, dlc_df, exp_name)


if __name__ == "__main__":
    main()