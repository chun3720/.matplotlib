# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:36:11 2022

@author: user
"""

from loadexp import fileloads, build_data, Dataloads, progress_bar
import pandas as pd
import os, re
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


plt.style.use(['science', 'no-latex'])

year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"

def add_median_labels(ax, fmt='.1f'):
    lines = ax.get_lines()
    boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
    lines_per_box = int(len(lines) / len(boxes))
    for median in lines[4:len(lines):lines_per_box]:
        x, y = (data.mean() for data in median.get_data())
        # choose value depending on horizontal or vertical plot orientation
        value = x if (median.get_xdata()[1] - median.get_xdata()[0]) == 0 else y
        text = ax.text(x, y, f'{value:{fmt}}', ha='center', va='center',
                       fontweight='bold', color='black')
        # create median-colored border around white text for contrast
        # text.set_path_effects([
        #     path_effects.Stroke(linewidth=3, foreground=median.get_color()),
        #     path_effects.Normal(),
        # ])

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
        method_dict = {'Constant Current\n' : "GCD", 'Cyclic Voltammetry\n' : "CV"}
        self.method = ''
        
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            self.method = method_dict[lines[3]]
            h = re.findall('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', lines[1])

        self.header = int(h[0])     
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
            
            if self.name.endswith("_CstC"):
                self.name = self.name[:-8]
                
            
        elif self.method == 'CV':
            self.df.drop(columns = ['mode', 'ox/red', 'error', 'counter inc.', 'P/W'], inplace = True)
            t1, v1 = self.df[["time/s", "control/V"]].loc[1]
            t2, v2 = self.df[["time/s", "control/V"]].loc[2]
            
            self.scan_rate =  round((v2-v1) / (t2-t1) , 2)
            if self.name.endswith("_CV"):
                self.name = self.name[:-6]
            
    def __str__(self):
        return self.name
    
    def __len__(self):
        
        return len(self.name)
    
    def get_calculation(self):
        """
        Calculate capacitance for GCD measurement without considering IR drop.
        Applied current is already provided by object initialization.
        
        Args:
            None
            
        Returns: A real number representing capacitance.
        """
        
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
                    n = self.df.shape[0]
                    T2, V2 = self.df[["time/s", "<Ewe>/V"]].loc[n-1]
       
                
                self.max_point = np.array([T1, T2])
                self.half_point = np.array([V1, V2])
                self.slope = (T2- T1) /  (V1-V2)
                self.cap_result = self.Is * self.slope
            except:
                pass

        else:
            return None
        
    def get_condition(self):
        curr = round(self.appl_current, 2)
        return f'{curr} {self.appl_unit}'
        
    def get_capacitance(self):

        if self.cap_result < 1 and self.cap_unit =='F':
            self.cap_result *= 1000
            self.cap_unit = 'mF'
            
        if self.cap_result < 0.1 and self.cap_unit == 'mF':
            self.cap_result *= 1000
            self.cap_unit = 'uF'
            
        return  f'{round(self.cap_result, 2)} {self.cap_unit}'
                
        
    def get_plot(self, path):
        
        output_path = f'{path}\\output\\'
        
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        if self.method == "GCD":
            
            Is = self.get_condition()
            label = f'{self.name}, {Is}'
            plt.subplot(211)
            plt.plot(self.df["time/s"], self.df["<Ewe>/V"], '--', color = 'gray', label = label)
    
            cap_label = self.get_capacitance()
            try:
                plt.plot(self.max_point, self.half_point, 'r-', label = cap_label)
            except:
                pass
    
            leg = plt.legend(fontsize = 'xx-small')
            set_figure(leg, "Time (s)", "Voltage (V)", False)
            plt.subplot(212)
            plt.plot(self.df_charge["Capacity/mA.h"], self.df_charge["<Ewe>/V"], 'b-')
            plt.plot(self.df_discharge["Capacity/mA.h"], self.df_discharge["<Ewe>/V"], 'b-')
            plt.xlabel("Capacity (mAh)")
            plt.ylabel('Voltage (V)')
            plt.subplots_adjust(hspace = 0.5)
            plt.savefig(f'{output_path}{self.name}.png', dpi = 300)    
        
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
        
    def get_drop(self):
        
        def get_slope(time, voltage, sep):
            temp_X = np.array(time)
            temp_Y = np.array(voltage)
            dx, dy = [], []
            for i in range(0, len(temp_X), sep):
                dx.append(temp_X[i])
                dy.append(temp_Y[i])
            
            dydx = np.diff(dy)/np.diff(dx)
            
            return dydx
      
        
        if self.method == "GCD":
            X = self.df_discharge["time/s"]
            Y = self.df_discharge["<Ewe>/V"]

            try:
                dydx = get_slope(X, Y, 5)
                # plt.hist(medians)
                
                self.caps_mF = -self.Is*1000/dydx
                ax = sns.boxplot(y = self.caps_mF, color = 'white')
                sns.stripplot(y = self.caps_mF, color = 'red', alpha = 0.3, edgecolor = 'red', linewidth = 1)
                add_median_labels(ax)
                plt.ylabel("Capacitance (mF)")
                plt.title(f"{self.name}", fontsize = 10)
                plt.show()
                # sns.displot(self.caps_mf, kde=  True, bins = 5 )
                # plt.show()
                
            except:
                pass

def get_capacity_tot(exp_obj, cols):
    
    return pd.concat([exp_obj.df_charge[cols].reset_index(drop = True)
              ,exp_obj.df_discharge[cols].reset_index(drop = True) ]
              ,axis = 1, ignore_index = True)
     
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
    
    GCD_list, cap_list, cap_unit, Is_list = [] , [], [], []   
    
    for gcd in GCDs:
        GCD_list.append(gcd.name)
        Is_list.append(gcd.get_condition())
        cap_list.append(round(gcd.cap_result, 2))
        cap_unit.append(gcd.cap_unit)
    
    d = {"Capacitance (I*dt/dV)": cap_list, "unit": cap_unit, "Current": Is_list}
    df1 = pd.DataFrame(data = d, index = GCD_list)
    
    gcd_pkl_file = f'{output_path}\\GCD_tot.pkl'    
    # gcd_tot_xl = f'{output_path}\\GCD_tot.xlsx'
    # with pd.ExcelWriter(f'{output_path}\\GCD_tot.xlsx') as writer:
    n= len(GCDs)
    progress_bar(0, n)
    gcd_tot_df = pd.DataFrame()
    gcd_header_tot = []
    for i, gcd in enumerate(GCDs):
        cols = ["time/s", "<Ewe>/V"]
        header = [f"time_{i}", gcd.name]
        # (
        #  gcd.df[cols]
        #   .to_excel(writer, startcol = 2*i, index = False, header = header)
         
        #  )
        gcd_header_tot += header
        gcd_tot_df = pd.concat([gcd_tot_df, gcd.df[cols]], axis = 1, ignore_index = True)
        progress_bar(i+1, n)
        gcd_tot_df.columns = gcd_header_tot
        gcd_tot_df.to_pickle(gcd_pkl_file)
        # df1.to_excel(writer, sheet_name = 'Summary')
        
    pkl_file = f'{output_path}\\Capacity_tot.pkl'    
    capacity_xl = f'{output_path}\\Capacity_tot.xlsx'
    # with pd.ExcelWriter(f'{output_path}\\Capacity_tot.xlsx') as writer:
        
    n= len(GCDs)
    progress_bar(0, n)
    tot_df = pd.DataFrame()
    header_tot = []
    for i, gcd in enumerate(GCDs):
        
        cols = ["Capacity/mA.h", "<Ewe>/V"]
        header = [ f'Charge_{i}', f'V_{i}', f'Discharge_{i}',gcd.name ]
        capacity_df = get_capacity_tot(gcd, cols)
        # (
        #     capacity_df
        #     .to_excel(writer, startcol = 4*i, index = False, header = header)
        #     )
        header_tot += header
        tot_df = pd.concat([tot_df, capacity_df], axis = 1, ignore_index = True)
        progress_bar(i+1, n)
    
    tot_df.columns = header_tot
    tot_df.to_pickle(pkl_file)
    # tot_df.to_excel(capacity_xl, index = False)

    if CVs:
        
        with pd.ExcelWriter(f'{output_path}\\CV_tot.xlsx') as writer:
        
            n= len(GCDs)
            progress_bar(0, n)
            for i, cv in enumerate(CVs):
                cols = ["Ewe/V", "<I>/mA"]
                (
                 cv.df[cols]
                 .to_excel(writer, startcol = 2*i, index = False, header = [f'V_{i}', cv.name])
                 )
                progress_bar(i+1, n)
    
    
def get_multiplot(exp, path):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'm', 'gray', 'brown','darkcyan', 
                  'skyblue', 'hotpink', 'dodgerblue']
    n = len(color_list)
    GCDs, CVs = [], []
    
    for item in exp:
        if item.method == "GCD":
            GCDs.append(item)
        
        elif item.method == "CV":
            CVs.append(item)

    for i, gcd in enumerate(GCDs):
        condition = gcd.get_condition()
        label = f'{gcd.name}, {condition}'
        plt.plot(gcd.df['time/s'], gcd.df['<Ewe>/V'], label = label, color = color_list[i%n])
    
    leg = plt.legend(fontsize = 'xx-small')
    set_figure(leg, "Time (s)", "Voltage (V)")
   
    
    for i, gcd in enumerate(GCDs):
        
        plt.plot(gcd.df_charge["Capacity/mA.h"], gcd.df_charge["<Ewe>/V"], label = gcd.name, color = color_list[i%n])
        plt.plot(gcd.df_discharge["Capacity/mA.h"], gcd.df_discharge["<Ewe>/V"], color = color_list[i%n])
    
    leg = plt.legend(fontsize = 'xx-small')
    set_figure(leg, "Capacity (mAh)", 'Voltage (V)')
    
    if CVs:
        
        for i, cv in enumerate(CVs):
            rate = cv.scan_rate * 1000
            speed = f'{rate} mV/s'
            label = f'{cv.name}, {speed}'
            plt.plot(cv.df["Ewe/V"], cv.df["<I>/mA"], label = label, color = color_list[i%n])
            
        leg = plt.legend(fontsize = 'xx-small')
        set_figure(leg, "Voltage (V)", 'Current (mA)')
       


def main(py_path):
    
    raw_list, path, _, _ = fileloads(py_path, '.mpt')
    exp_obj = build_data(path, raw_list, EC_measurement)
    for exp in exp_obj:
        exp.get_calculation()
        # exp.get_plot(path)
        # exp.get_drop()
            
    get_multiplot(exp_obj, path)
    get_export(exp_obj, path)
    
    
if __name__ == "__main__":
    plt.style.use(['science', 'no-latex'])
    
    main(year_path)


# for test
# raw_list, path, _, _ = fileloads(year_path, '.mpt')
# exp_obj = build_data(path, raw_list, EC_measurement)

# for exp in exp_obj:
#     exp.get_calculation()
#     exp.get_plot(path)
#     exp.get_drop()
    
# get_multiplot(exp_obj, path)
# get_export(exp_obj, path)
