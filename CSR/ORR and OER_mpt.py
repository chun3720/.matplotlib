# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:36:11 2022

@author: user
"""

from loadexp import fileloads, build_data, Dataloads, GUI_load
from typing import List
import pandas as pd
import os, re
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
# import scienceplots

plt.style.use(['science', 'no-latex'])

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"



def set_figure(leg, xlabel, ylabel, show = True):
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if show:
        plt.show()

class EC_measurement(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        method_dict = {'Constant Current\n' : "GCD", 'Cyclic Voltammetry\n' : "CV",
                       "Linear Sweep Voltammetry\n": "LSV"}
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
                
            
                
        elif self.method == "LSV":
            self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = "\t", header = 0\
                                  , usecols = ["time/s", "control/V", "Ewe/V", "<I>/mA"])


        # self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = '\t', header = 0)
        
        

        # check = self.df["cycle number"].value_counts().to_dict()
        # _check = sorted(list(check.keys()))
        # if len(check) != 1:
        #     key = _check[-2]
        #     filt = self.df[self.df["cycle number"] == key]
        #     self.df = filt.reset_index(drop = True)

        # num = self.df["cycle number"].loc[0]
        # to_delete = f'_{int(num)}'

        # if self.name[-2:] == to_delete:
        #     self.name = self.name[:-2]
        
        self.df["<I>/mA"] /= 0.2376

        if self.method == 'GCD':
            pass


        elif self.method == 'CV':
            # self.df.drop(columns = ['mode', 'ox/red', 'error', 'counter inc.', 'P/W'], inplace = True)
            t1, v1 = self.df[["time/s", "control/V"]].loc[1]
            t2, v2 = self.df[["time/s", "control/V"]].loc[2]

            self.scan_rate =  abs(round((v2-v1) / (t2-t1) , 2))
            if self.name.endswith("_CV"):
                self.name = self.name[:-6]
                
                
                
            check = self.df["cycle number"].unique()
            
            end_cycle = check[-2]
            
            self.end_df = self.df[self.df["cycle number"] == end_cycle]
            
        
        
            
            
            
            

    def __str__(self):
        return self.name

    def __len__(self):

        return len(self.name)



    def get_plot(self, path: str):

        # output_path = f'{path}\\output\\'
        output_path = os.path.join(path, "output")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        if self.method == "GCD":
            
            pass

        elif self.method  == "CV":
            pass
            # rate = self.scan_rate
            # rate  *= 1000
            # label = str(rate) + ' mV/s'
            # plt.plot(self.df["Ewe/V"], self.df["<I>/mA"], label = self.name + ', ' + label)

            # leg = plt.legend()
            # for line, text in zip(leg.get_lines(), leg.get_texts()):
            #     text.set_color(line.get_color())
            # plt.xlabel("Voltage (V)")
            # plt.ylabel("Current (mA)")

        plt.show()

    



def get_export(exp_objs: List[EC_measurement], path: str, conversion):
    
    output_path = os.path.join(path, "output")

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    LSVs, CVs = [], []
    for item in exp_objs:
        if item.method == "LSV":
            LSVs.append(item)

        elif item.method == "CV":
            CVs.append(item)


    if CVs:
        cv2export = os.path.join(output_path, "CV_tot.xlsx")
        with pd.ExcelWriter(cv2export) as writer:

            
            for i, cv in enumerate(CVs):
                
                cols = ["Ewe/V", "<I>/mA"]
                if conversion:
                    cv_df = cv.end_df.copy()
                    cv_df["Ewe/V"] += float(conversion)
                    (
                     cv_df[cols]
                     .to_excel(writer, startcol = 2*i, index = False, header = [f'V_{i}_shift', cv.name])
                     )
                    
                    
                else:
                    (
                     cv.end_df[cols]
                     .to_excel(writer, startcol = 2*i, index = False, header = [f'V_{i}', cv.name])
                     )
                    
        
        
    if LSVs:
        lsv2export = os.path.join(output_path, "LSV_tot.xlsx")
        with pd.ExcelWriter(lsv2export) as writer:
            
            for i, lsv in enumerate(LSVs):
                
                
                cols = ["Ewe/V", "<I>/mA"]
                
                if conversion:
                    lsv_df = lsv.df.copy()
                    lsv_df["Ewe/V"] += float(conversion)
                    (
                     lsv_df[cols]
                     .to_excel(writer, startcol = 2*i, index = False, header = [f'V_{i}_shift', lsv.name])
                     )
                else:
                    (
                        lsv.df[cols]
                        .to_excel(writer, startcol = 2*i, index = False, header = [f"V_{i}", lsv.name])
                        
                        )
                
                


def get_multiplot(exp_objs: List[EC_measurement], path: str, conversion):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'm', 'gray', 'brown','darkcyan',
                  'skyblue', 'hotpink', 'dodgerblue']
    n = len(color_list)
    LSVs, CVs = [], []

    for item in exp_objs:
        if item.method == "LSV":
            LSVs.append(item)

        elif item.method == "CV":
            CVs.append(item)


    if CVs:

        for i, cv in enumerate(CVs):
            rate = cv.scan_rate * 1000
            speed = f'{rate} mV/s'
            label = f'{cv.name}, {speed}'
            if conversion:
                cv_df = cv.end_df[["Ewe/V", "<I>/mA"]].copy()
                cv_df["Ewe/V"] = cv_df["Ewe/V"] + float(conversion)
                plt.plot(cv_df["Ewe/V"], cv_df["<I>/mA"], label = label, color = color_list[i%n])
            else:
                
                plt.plot(cv.end_df["Ewe/V"], cv.end_df["<I>/mA"], label = label, color = color_list[i%n])

        leg = plt.legend(fontsize = 'xx-small')
        if conversion:
            set_figure(leg, "Voltage (V vs. RHE)", 'Current Density (mA/cm$^2$)')
        else:
            set_figure(leg, "Voltage (V vs. Ag/AgCl)", 'Current Density (mA/cm$^2$)')
            
            
    if LSVs:
        for i, lsv in enumerate(LSVs):
            
            if conversion:
                lsv_df = lsv.df.copy()
                lsv_df["Ewe/V"] = lsv_df["Ewe/V"] + float(conversion)
                plt.plot(lsv_df["Ewe/V"], lsv_df["<I>/mA"])
            
            else:
                plt.plot(lsv.df["Ewe/V"], lsv.df["<I>/mA"])
            
        
        if conversion:
            set_figure(leg, "Voltage (V vs. RHE)", 'Current Density (mA/cm$^2$)')
        else:
            set_figure(leg, "Voltage (V vs. Ag/AgCl)", 'Current Density (mA/cm$^2$)')
            



def main(py_path: str):

    raw_list, path, _, _ = fileloads(py_path, '.mpt')
    exp_obj = build_data(path, raw_list, EC_measurement, False)
    # for exp in exp_obj:

    #     exp.get_calculation()
    #     exp.get_plot(path)
        # exp.get_drop()
        
    shift = input("type conversion shift for voltage, ex) V_RHE = V_AgAgCl + shift : (Enter for skip)\n")
    

    get_multiplot(exp_obj, path, shift)
    get_export(exp_obj, path, shift)
    
    return exp_obj


if __name__ == "__main__":
    plt.style.use(['science', 'no-latex'])
    
    py_path = GUI_load(True)

    exp_obj = main(py_path)


# for test
# raw_list, path, _, _ = fileloads(year_path, '.mpt')
# exp_obj = build_data(path, raw_list, EC_measurement)

# for exp in exp_obj:
#     exp.get_calculation()
#     exp.get_plot(path)
#     exp.get_drop()

# get_multiplot(exp_obj, path)
# get_export(exp_obj, path)
