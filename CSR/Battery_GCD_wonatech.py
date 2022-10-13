# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:06:16 2021
last update : Feb 15 2022
@author: jycheon
"""
from loadexp import *
import pandas as pd
import os
import string
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
import csv
from pathlib import Path
from tqdm import tqdm

# plt.style.use('science')
plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"

class LIB_tot(Dataloads):  
    # df_list = []
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        # self.raw = pd.read_csv(self.file_path, index_col = 0, encoding = "cp949") 
        self.raw = pd.read_pickle(self.file_path)
        self.raw.index = self.raw.index.astype('int64')
        # self.df.set_index('인덱스', inplace = True)
        self.X, self.Y = self.raw.columns[0], self.raw.columns[1]
        
    def get_check(self):
        plt.plot(self.raw.index, self.raw[self.Y], label = "potential profile")
        plt.xlabel("Index")
        plt.ylabel("Potential (V vs. Li/Li$^+$)")
        plt.show()
        
    def separation(self, electrode, cut_off):
        if electrode == 'a':
            if self.raw.iloc[0, 1] > cut_off:
                null = self.raw[self.raw[self.Y] < cut_off].index 
                self.data = (
                    self.raw.iloc[null[0]:]
                    .reset_index(drop = True)
                    .drop(index = 0)
                    )

            else:
                self.data = self.raw
            self.idx_list_values = self.raw[self.raw[self.Y] > cut_off].index
            
        
        elif electrode =='c':
            if self.raw.iloc[0, 1] < cut_off:
                null = self.raw[self.raw[self.Y] > cut_off].index
                self.data = (
                    self.raw.iloc[null[0]:]
                    .reset_index(drop = True)
                    .drop(index = 0)
                    )
                  
            else:
                self.data = self.raw
            self.idx_list_values = self.data[self.data[self.Y] < cut_off].index
            
  
        self.idxx = [0] + list(self.idx_list_values)
        
        # print(self.idx_list_values)
        df_list = []
        
        output_path = os.path.join(self.path, 'split\\')
        
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        n = len(self.idxx)-1
        
        idx_list = []
        capacity_list = []
        progress_bar(0, n)
        
        for i in range(n):
            

            df = self.data.iloc[self.idxx[i]:self.idxx[i+1]]
            df.to_csv(f'{output_path}cycle{i+1}.csv', encoding = "cp949")
            # df.to_csv(output_path + "cycle" + str(i+1) + ".csv", encoding = "cp949")        
            k = df.shape[0]
            cap, vol = df.iloc[k-1]
            capacity_list.append(cap)
            idx_list.append(i+1)
            progress_bar(i+1, n)     
            

        
        d = {"Cycle": idx_list, "Capacity (Ah/g)" : capacity_list}
        df1 = pd.DataFrame(data = d, index = idx_list)      
        
        cycle_path = (
            Path(self.path)
            .parent
            .joinpath("cycle_auto")
            )

        if not cycle_path.exists():
            cycle_path.mkdir()
        
        target_file = cycle_path.joinpath(f'{self.name}_cycle.xlsx')
        with pd.ExcelWriter(target_file) as writer:
            df1.to_excel(writer, sheet_name = '데이터_1_1', index = False)     
        
        return output_path
    

    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
  
        
        
class LIB_csv(Dataloads):  
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.df = pd.read_csv(self.file_path, index_col = 0, encoding = "cp949") 
        self.X, self.Y  = self.df.columns[0], self.df.columns[1]
        self.null = self.df[self.df[self.X] == 0].index
        self.df = self.df.drop(self.null)
        self.min = self.df[self.Y].idxmin()
        self.max = self.df[self.Y].idxmax()
        self.positive = None
        self.negative = None
    
    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def df_indexing(self):
        if self.df.iloc[0, 1] > self.df.iloc[3, 1]:
            self.negative = self.df.loc[:self.min]
            self.positive = self.df.loc[self.min+1 :]  
        else:
            self.positive = self.df.loc[:self.max]
            self.negative = self.df.loc[self.max +1 :]
            
    def get_name(self):
        return self.name
    
    # def get_check(self):
    #     return self.df.loc[self.min, "Voltage(V)"]
              
    def get_discharge(self):
        return self.df.loc[self.max]
        
    def get_charge(self):
        return self.df.loc[self.min]
    
    def GCD_plot(self, color):
        plt.plot(self.negative[self.X], self.negative[self.Y], color, label = LIB_csv.__str__(self))
        plt.plot(self.positive[self.X], self.positive[self.Y], color )


def get_plot(path, exp, k=None):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'purple', 'dimgrey', 'hotpink', 'steelblue', 'mediumseagreen', 'm']
    n = len(exp)
    nc = len(color_list)
    numbering = range(k-1, n, k)
    
    for ix, num in enumerate(numbering):
        exp[num].df_indexing()
        exp[num].GCD_plot(color_list[ix%nc])
    
    leg = plt.legend(fontsize = 6)
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlabel('Specific Capacity (Ah/g)')
    plt.ylabel(r'Potential (V vs. Li/Li$^+$)')  
    plt.savefig(path + '_GCD.png', dpi=300)

def get_result(path, exp, k=None):
    n = len(exp)
    numbering = range(k-1, n, k)
    for i in numbering:
        print(exp[i].get_name().rjust(42))
        print(exp[i].get_charge())
        print('------------------------------------------')
        print(exp[i].get_discharge(), end='\n')
        print('==========================================')       
    print('\nDone!\n')   

def get_export(path, exp_obj, k=None):
    output_path = os.path.join(path, 'output\\')
    # output_path = self.path + 'output\\'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    GCDs = []
    n = len(exp_obj)
    numbering = range(k-1, n, k)
    for num, b in zip(numbering, exp_obj):
        with pd.ExcelWriter(f'{output_path}{exp_obj[num].name}_corrected.xlsx') as writer:
        # with pd.ExcelWriter(output_path + exp[a].get_name() + '_corrected.xlsx') as writer:
            (
                pd.concat([exp_obj[num].negative.reset_index(drop = True)
                           ,exp_obj[num].positive.reset_index(drop = True)]
                           ,axis = 1, ignore_index = True)
                           .to_excel(writer, index = False
                                     ,header = ["negative (Ah/g)","V1", "positive (Ah/g)", "V2"])
                    
                )       
        GCDs.append(exp_obj[num])
        
    with pd.ExcelWriter(f'{output_path}total.xlsx') as writer:
        num = len(GCDs)
        progress_bar(0, num)
        for ix, gcd in enumerate(GCDs):
            
            (
                pd.concat([gcd.negative.reset_index(drop = True)
                           , gcd.positive.reset_index(drop = True)], axis = 1)
                .to_excel(writer, startcol = 4*ix, index = False
                          , header = [f"negative_{ix}", f"V_{ix}", f"positive_{ix}", gcd.name])
                                      
                )
            progress_bar(ix+1, num)
            
            
def csv_from_excel(path, file):
    
    print("loading............................\n")
    wb = openpyxl.load_workbook(path + file, read_only = True, data_only = True)
    sheet_names = wb.worksheets
    target_sheet = sheet_names[1].title
    # ws = wb.get_sheet_by_name(target_sheet)
    ws = wb[target_sheet]
    name, ext = os.path.splitext(file)
    
    # with open(path + name + '.csv', 'w', newline = "") as f:
    #     csv_writer = csv.writer(f)
    #     for r in tqdm(ws.iter_rows()):            
    #         csv_writer.writerow([cell.value for cell in r])
    temp = []
    for r in tqdm(ws.iter_rows()):
        temp.append([cell.value for cell in r])
    
    df = pd.DataFrame(np.array(temp[1:]), columns = temp[0])
    df.set_index("인덱스").to_pickle(f'{path}{name}.pkl')
# runs the csv_from_excel function:

    
def main(date_path = year_path):
    done0 =  False    
    
    while not done0:
        get_input = input("select data file extension, xlsx (x) or csv(c): ")    
        if get_input in ["X", "x", "C", "c"]:
            done0 = True
        else:
            print("typing error!")
    
    if get_input.lower() == "x":
        ext = 'xlsx'
    elif get_input.lower() == "c":
        ext = "csv"
    
    raw, path, _, _ = fileloads(date_path, ext)
    
    if get_input == "x" and len(raw) > 1:
        import Battery_GCDplot_old as xl
        exp_obj = build_data(path, raw, xl.LIB_builder)
        xl.get_plot(path, exp_obj)
        xl.get_result(path, exp_obj)
        xl.get_export(path, exp_obj)
        
    elif get_input == "c" and len(raw) > 1:
        exp_obj= build_data(path, raw, LIB_csv)
        get_plot(path, exp_obj, k=1)
        get_result(path, exp_obj, k=1)
        get_export(path, exp_obj, k=1)
      
    
    else:
    
        if (os.path.splitext(raw[0])[0] + ".pkl") not in os.listdir(path):
            csv_from_excel(path, raw[0])
            csv_list = [_ for _ in os.listdir(path) if _.endswith(".pkl")]
        else:
            csv_list = [_ for _ in os.listdir(path) if _.endswith(".pkl")]
            
        
        exp_data = build_data(path, csv_list, LIB_tot)
        exp_data[0].get_check()
        done1 = False
        while not done1:
            electrode = input("which electrode? a, anode or c, cathode (or full cell): ")
            
            if electrode in ['A', 'a', 'c', "C"]:
                done1 = True
            else:
                print("typing error!")         
            
        electrode = electrode.lower()
        done2 =  False
        while not done2:
            cutoff = input("type cutoff voltage for each cycle (anode-> top, cathode -> bottom): ")
            if cutoff[0].isnumeric():
                done2 = True
            else:
                print("typing error!")
                
        
        output_path = exp_data[0].separation(electrode, float(cutoff))
        
        raw_list = os.listdir(output_path)
        raw_list = [_ for _ in raw_list if _.endswith(".csv")]
        sorted_list = sorted(raw_list, key = len)
        exp_obj = build_data(output_path, sorted_list , LIB_csv)
        
        done3 = False
        while not done3:
            
            k = input("\ntype separation unit: ")
            
            if k[0].isnumeric():
                done3 = True
            else:
                print("typing error!")
        k = int(k)
        def final_plot(output_path, exp_obj, k):
            get_plot(output_path, exp_obj, k)
            get_result(output_path, exp_obj, k)
            get_export(output_path, exp_obj, k)
                   

        final_plot(output_path, exp_obj, k)
        
        

if __name__ == "__main__":
    main()