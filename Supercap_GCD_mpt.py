# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:36:11 2022

@author: user
"""

from loadexp import *
import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
# import shutil
# from loadexp_0318 import *
plt.style.use(['science', 'no-latex'])

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"

class EC_measurement(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        method_dict = {'Constant Current\n' : "GCD", 'Cyclic Voltammetry\n' : "CV"}
        self.method = ''
        
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            self.method = method_dict[lines[3]]
            header = lines[1][18:20]    

        self.header = int(header)     
        self.df = pd.read_csv(self.file_path, skiprows = self.header-1, sep = '\t', header = 0)
        
        check = self.df["cycle number"].value_counts().to_dict()
        _check = sorted(list(check.keys()))
        if len(check) != 1:
            key = _check[-2]
            filt = self.df[self.df["cycle number"] == key]
            self.df = filt.reset_index(drop = True)
        
        num = self.df["cycle number"].loc[0]
        to_delete = f'_{int(num)}'
        
        if self.name[-2:] == to_delete:
            self.name = self.name[:-2]

        if self.method == 'GCD':            
            self.df.drop(columns = ['mode', 'ox/red', 'error', 'Ns changes','counter inc.', 'P/W'], inplace = True)
            self.appl_current = self.df["control/mA"].loc[0]
            self.appl_unit = self.df.columns[2].split("/")[1]
            self.cap_result = 0
            self.cap_unit  = 'F'
            self.origin  = self.df["time/s"].loc[0]
            self.df["time/s"] -= self.origin
            
            if self.appl_unit =="mA":
                self.Is = self.appl_current /1000
                
            elif self.appl_unit == "uA":
                self.Is = self.appl_current /1000000
            
            self.max = self.df["<Ewe>/V"].idxmax()
            self.df_charge = self.df.loc[:self.max]
            self.df_discharge = self.df.loc[self.max+1:]
            self.name = self.name.replace("_02_CstC", "")
            
        elif self.method == 'CV':
            self.df.drop(columns = ['mode', 'ox/red', 'error', 'counter inc.', 'P/W'], inplace = True)
            t1, v1 = self.df[["time/s", "control/V"]].loc[1]
            t2, v2 = self.df[["time/s", "control/V"]].loc[2]
            
            self.scan_rate =  round((v2-v1) / (t2-t1) , 2)
            self.name = self.name.replace("_01_CV", "")
            

    def get_calculation(self):
        
        if self.method == "GCD":
            
            try:
        
                k = self.df_charge.shape[0]
                T1, V1 = self.df_charge[["time/s", "<Ewe>/V"]].loc[k-1]
    
                if V1 > 2.4:
                    idx_list = self.df_discharge[self.df_discharge["<Ewe>/V"] < 1.5].index
                    T2, V2 = self.df_discharge[["time/s", "<Ewe>/V"]].loc[idx_list[0]]
                else:
                ###
                    # for 1V calculation
                    n = self.df_discharge.shape[0]
                    T2, V2 = self.df_discharge.loc[n-1]

                self.max_point = np.array([T1, T2])
                self.half_point = np.array([V1, V2])
                self.slope = (T2- T1) /  (V1-V2)
                self.cap_result = self.Is * self.slope
                
                return True
            
            except:
                return None

        
        else:
            return None
        
    def get_condition(self):
        
        return f'{self.appl_current} {self.appl_unit}'
        
    def get_capacitance(self):

        if self.cap_result < 1 and self.cap_unit =='F':
            self.cap_result *= 1000
            self.cap_unit = 'mF'
            
        if self.cap_result < 0.1 and self.cap_unit == 'mF':
            self.cap_result *= 1000
            self.cap_unit = 'uF'
            
        res = f'{round(self.cap_result, 2)} {self.cap_unit}'
        return res
                
        
    def get_plot(self, path):
        
        output_path = f'{path}\\output\\'
        
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        if self.method == "GCD":
            # Is = str(self.appl_current) + ' ' + self.appl_unit
            Is = self.get_condition()
            # label = self.name + ', ' + Is
            label = f'{self.name.replace("_CstC", "")}, {Is}'
            plt.subplot(211)
            plt.plot(self.df["time/s"], self.df["<Ewe>/V"], '--', color = 'gray', label = label)
    
            cap_label = self.get_capacitance()
            try:
                plt.plot(self.max_point, self.half_point, 'r-', label = cap_label)
            except:
                pass
    
            leg = plt.legend(fontsize = 'xx-small')
            for line, text in zip(leg.get_lines(), leg.get_texts()):
                text.set_color(line.get_color())

            plt.xlabel('Time (s)')
            # plt.xticks(fontsize = 11)
            plt.ylabel('Voltage (V)')
            # plt.yticks(fontsize = 11)
            
            plt.subplot(212)
            plt.plot(self.df_charge["Capacity/mA.h"], self.df_charge["<Ewe>/V"], 'b-')
            plt.plot(self.df_discharge["Capacity/mA.h"], self.df_discharge["<Ewe>/V"], 'b-')
            plt.xlabel("Capacity (mAh)")
            plt.ylabel('Voltage (V)')
            plt.savefig(f'{output_path}{self.name}.png')    
        
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
        
        
def get_export(exp, path):
    # output_path = path + "output\\"
    output_path = f'{path}\\output\\'
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)    
    
    GCDs = []
    CVs = []
    for item in exp:
        if item.method == "GCD":
            GCDs.append(item)
        
        elif item.method == "CV":
            CVs.append(item)
    
    GCD_list = []
    cap_list = []
    cap_unit = []
    Is_list = []
    
    for gcd in GCDs:
        GCD_list.append(gcd.name)
        Is_list.append(gcd.get_condition())
        cap_list.append(round(gcd.cap_result, 2))
        cap_unit.append(gcd.cap_unit)
    
    d = {"Capacitance (I*dt/dV)": cap_list, "unit": cap_unit, "Current": Is_list}
    df1 = pd.DataFrame(data = d, index = GCD_list)
    
    
    with pd.ExcelWriter(f'{output_path}\\GCD_tot.xlsx') as writer:
        n= len(GCDs)
        progress_bar(0, n)
        for i, gcd in enumerate(GCDs):
            cols = ["time/s", "<Ewe>/V"]
            (
             gcd.df[cols].rename(columns = {"time/s" : f"time_{i}", "<Ewe>/V" : gcd.name})
             .to_excel(writer, startcol = 2*i, index = False)
             )
            progress_bar(i+1, n)
        df1.to_excel(writer, sheet_name = 'Summary')
        
        
    with pd.ExcelWriter(f'{output_path}\\Capacity_tot.xlsx') as writer:
        
        n= len(GCDs)
        progress_bar(0, n)
        for i, gcd in enumerate(GCDs):
            
            cols = ["Capacity/mA.h", "<Ewe>/V"]
            (
                pd.concat([gcd.df_charge[cols].reset_index(drop = True)
                          ,gcd.df_discharge[cols].reset_index(drop = True) ]
                          ,axis = 1, ignore_index = True)
                .to_excel(writer, startcol = 4*i, index = False, 
                          header = [ f'Charge_{i}', f'V_{i}', f'Discharge_{i}',gcd.name ])
                )
            
            progress_bar(i+1, n)
                
            

    if CVs:
        
        with pd.ExcelWriter(f'{output_path}\\CV_tot.xlsx') as writer:
        
            n= len(GCDs)
            progress_bar(0, n)
            for i, cv in enumerate(CVs):
                cols = ["Ewe/V", "<I>/mA"]
                (
                 cv.df[cols].rename(columns = {"Ewe/V": f'V_{i}', "<I>/mA": cv.name.replace("_CV", "")})
                 .to_excel(writer, startcol = 2*i, index = False)
                 )
                progress_bar(i+1, n)

    
    
def get_multiplot(exp, path):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'm', 'gray', 'brown','darkcyan', 
                  'skyblue', 'hotpink', 'dodgerblue']
    # color_list = ["k"] + list(mcolors.TABLEAU_COLORS.values()) + ["b", "m", "g", "gray"]
    # color_list.remove('#17becf')
    n = len(color_list)
    GCDs = []
    CVs = []

    for item in exp:
        if item.method == "GCD":
            GCDs.append(item)
        
        elif item.method == "CV":
            CVs.append(item)

    for i, gcd in enumerate(GCDs):
        condition = gcd.get_condition()
        exp_name = gcd.name
        label = f'{exp_name}, {condition}'
        plt.plot(gcd.df['time/s'], gcd.df['<Ewe>/V'], label = label, color = color_list[i%n])
    
    leg = plt.legend(fontsize = 'xx-small')
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.show() 
    
    for i, gcd in enumerate(GCDs):
        
        plt.plot(gcd.df_charge["Capacity/mA.h"], gcd.df_charge["<Ewe>/V"], label = gcd.name, color = color_list[i%n])
        plt.plot(gcd.df_discharge["Capacity/mA.h"], gcd.df_discharge["<Ewe>/V"], color = color_list[i%n])
    
    leg = plt.legend(fontsize = 'xx-small')
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlabel("Capacity (mAh)")
    plt.ylabel('Voltage (V)')
    plt.show()
    
    if CVs:
        # for i in range(len(CVs)):
        for i, cv in enumerate(CVs):
            rate = cv.scan_rate * 1000
            # speed = str(rate) + ' mV/s'
            speed = f'{rate} mV/s'
            # label = CVs[i].name + ', ' + speed
            label = f'{cv.name}, {speed}'
            plt.plot(cv.df["Ewe/V"], cv.df["<I>/mA"], label = label, color = color_list[i%n])
            
        leg = plt.legend(fontsize = 'xx-small')
        for line, text in zip(leg.get_lines(), leg.get_texts()):
            text.set_color(line.get_color())
        
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (mA)")
        plt.show()
        
def main(date_path = year_path):
    raw_list, path, _, _ = fileloads(date_path, '.mpt')
    exp_obj = build_data(path, raw_list, EC_measurement)
    
    
    # for i in range(len(exp_obj)):
    for exp in exp_obj:
        exp.get_calculation()
        exp.get_plot(path)
        
    get_multiplot(exp_obj, path)
    get_export(exp_obj, path)

if __name__ == "__main__":
    main()

