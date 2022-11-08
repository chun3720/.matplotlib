# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:28:27 2022

@author: user
"""
from pathlib import Path
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from loadexp import Dataloads, fileloads, build_data


# plt.style.use('science')
plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"

class LIB_cyc(Dataloads):
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.raw = pd.read_csv(self.file_path, skiprows= 10, delimiter = ',', encoding = "cp949", index_col = 0, usecols = ["Index", "Cycle_No.", "Dischg.Q(Ah)", 'Dischg.Q_s(Ah/g)'])
        self.raw.columns = ["num", "Q", "Q_s"]
        self.raw["mass"] = self.raw.Q/self.raw.Q_s
    


class LIB_tot(Dataloads):   
    
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.raw = pd.read_csv(self.file_path, skiprows= 10, delimiter = ',', encoding = "cp949", index_col = 0, usecols = ["Index", "Cycle_No.", "Step_No.", 'Voltage(V)', '|Q|(Ah)'])
        self.raw.columns = ["num", "step", "volt", "cap"]
        self.cycle_tot = len(self.raw.groupby("num"))
        
    def get_separation(self, mass):
        self.raw["cap"] = self.raw["cap"] / mass
        output_path = os.path.join(self.path, "split")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
            
        idx, caps = [], []
        for i in range(self.cycle_tot):
            j = i + 1
            cy = self.raw[self.raw.num == j]
            
            cy.to_parquet(f"{output_path}\\cycle_{j}.pqt")
            steps = cy.step.unique()

            
            non_rest_steps = []
            
            for s in steps:
                check_point = cy[cy.step == s].index[-1]
                cap_at_check_point = cy.cap.loc[check_point]
                
                if cap_at_check_point != 0:
                    non_rest_steps.append(s)
            
                # print(non_rest_steps)
            try:
                c_step, d_step = non_rest_steps
                # print(steps)
                # dc_point = cy[cy.step == steps[2]].index[-1] if len(steps) == 4 else cy[cy.step == steps[3]].index[-1]
                dc_point = cy[cy.step ==d_step].index[-1]
                idx.append(j)
                caps.append(cy.cap.loc[dc_point])
            except:
                print(f"Error! Skip {j}th cycle and the thereafter data ")
                pass
            
        d = {"Cycle": idx, "Specific Capacity (Ah/g)" : np.array(caps)}
        df1 = pd.DataFrame(data = d, index = idx)      
        df1.plot(x = "Cycle", y = "Specific Capacity (Ah/g)", kind = "scatter")
        plt.title(f"{self.name}", fontsize = 8)
        plt.show()
        
        cycle_path = (
            Path(self.path)
            .parent
            .joinpath("cycle_auto")
            )

        if not cycle_path.exists():
            cycle_path.mkdir()
        target_file = cycle_path.joinpath(f'{self.name}_cycle.xlsx')
        
        df1.to_excel(target_file)
        
        return self.name
            
            
class LIB_sep(Dataloads):
    
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.raw = pd.read_parquet(self.file_path)
        # self.col_name = ["num", "step", "volt", "cap"]
        
    def get_steps(self):
        step_list = self.raw.step.unique()
        non_rest_steps = []
        
        for s in step_list:
            check_point = self.raw[self.raw.step == s].index[-1]
            cap_at_check_point = self.raw.cap.loc[check_point]
            
            if cap_at_check_point != 0:
                non_rest_steps.append(s)
                
        c_step, d_step = non_rest_steps
            
        return (c_step, d_step)
        
    def get_GCD(self):
        
        charge_step, discharge_step = self.get_steps()
        # steps = self.raw.step.unique()
        cols = ["cap", "volt"]
        self.df = pd.concat([self.raw[self.raw.step == charge_step][cols].reset_index(drop = True),  \
                             self.raw[self.raw.step == discharge_step][cols].reset_index(drop = True)], \
                            axis =1, ignore_index = True)
        self.df.columns = ["q_c", "v_c", "q_d", f"{self.name}"]
        
        
    def get_curve(self, color):
        qc, vc, qd, vd = self.df.columns
        plt.plot(self.df[qc], self.df[vc], color, label = self.name)
        plt.plot(self.df[qd], self.df[vd], color)
        
        
            
def get_export(path, exp_obj):
    output_path = os.path.join(path, "output")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    tot_pkl = f"{output_path}\\total.pkl"
    
    tot_df = pd.DataFrame()
    header_tot = []
    
    for i, exp in enumerate(exp_obj):
        header = [f"charge_{i}", f"volt_{i}", f"discharge_{i}", exp.name]
        tot_df = pd.concat([tot_df, exp.df], axis = 1, ignore_index = True)
        header_tot += header
    
    tot_df.columns = header_tot
    tot_df.to_pickle(tot_pkl)
    

def get_tot_plot(exp_obj, title, k = 1):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'purple', 'dimgrey', 'hotpink', 'steelblue', 'mediumseagreen', 'm']
    
    
    nc = len(color_list)
    n = len(exp_obj)
    numbering = range(k-1, n, k)
    plot2export = []
    for i, num in enumerate(numbering):
        try:
            exp_obj[num].get_GCD()
            exp_obj[num].get_curve(color_list[i%nc]) 
            plot2export.append(exp_obj[num])
        except:
            pass

    # for i, exp in enumerate(exp_obj):
    #     exp.get_GCD()
    #     exp.get_curve(color_list[i%len(color_list)])
    
    plt.xlabel("Specific Capacity (Ah/g)")
    plt.ylabel("Potential (V vs. Li/Li$^+$)")
    plt.title(title, fontsize = 8)
    
    return plot2export



def main(date_path = year_path, direct = False, k = 1):
    date_path = Path(date_path)
    
    if not direct:
        check = input("whcih file to anlyais? raw (r) or each cycle (c)? ")
    
    else:
        check = "r"
    
    if check.lower() == "r":
        if not direct:
            raw, path, _, _ = fileloads(date_path, "csv")
        
        else:
            raw = [_ for _ in os.listdir(date_path) if _.endswith("csv")]
            path = date_path
        profile = [_ for _ in raw if os.path.splitext(_)[0].endswith("DC")]
        cycle = [_ for _ in raw if os.path.splitext(_)[0].endswith("CYC")] 
               
        exp_obj = build_data(path, profile, LIB_tot)
        cyc_obj = build_data(path, cycle, LIB_cyc)
        exp_title = exp_obj[0].get_separation(cyc_obj[0].raw.mass.iloc[0])
        
        split_path = os.path.join(path, "split")
        
        test = Path(split_path)
        
        test_files = [_ for _ in test.iterdir() if _.name.endswith("pqt")]
        test_sorted = sorted(test_files, key = os.path.getmtime)
        sep_files = [_.name for _ in test_sorted]
        data_obj = build_data(split_path, sep_files, LIB_sep)
        
        if not direct:
            check = input("type split basis (default value is 1):  ")
            k = int(check) if check else 1
        to_export  = get_tot_plot(data_obj, exp_title, k)
        
        get_export(os.path.join(path,"split"), to_export)
        

        
    else:
        raw, path, _, _ = fileloads(date_path, "pqt")
        exp_obj = build_data(path, raw, LIB_sep)
        
        get_tot_plot(exp_obj, "gcd")
        get_export(path, exp_obj)
        
if __name__ == "__main__":
    
    main(year_path)
    
