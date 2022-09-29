# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:26:05 2022

@author: user
"""

from loadexp import *
import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
# from loadexp_0318 import *
from openpyxl import load_workbook
import csv
import tqdm
# import peakdetect


plt.style.use(['science', 'no-latex'])
year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\EIS"

class EIS_tot(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        print(f'Loading and splitting {self.file} file....................')
        self.wb = load_workbook(self.file_path)
        self.sheet_count = len(self.wb.sheetnames)
        self.raw_split = os.path.join(path, 'raw_split\\')
        
        if not os.path.exists(self.raw_split):
            os.mkdir(self.raw_split)
        
        for i in range(0, self.sheet_count, 2):
            name = self.wb[self.wb.sheetnames[i]]["A2"].value.split('\\')[-1].replace('.SEO', "")                                                                      
            ws = self.wb[self.wb.sheetnames[i+1]]
            
            with open(f'{self.raw_split}{name}.csv', 'w', newline = "", encoding = "cp949") as f:
                csv_writer = csv.writer(f)
                for r in ws.iter_rows():
                # for r in tqdm(ws.iter_rows()):
                    csv_writer.writerow([cell.value for cell in r])
            
            
        # print("done!")
        
class EIS_raw(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        self.raw = pd.read_csv(self.file_path, index_col = 0, encoding = "cp949")
        self.output_path = path + 'output\\'
        try:
            os.mkdir(self.output_path)    
        except FileExistsError:
            pass        
        
def raw_plot(path, obj_list):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'm', 'gray', 'brown','darkcyan', 
                  'skyblue', 'hotpink', 'dodgerblue']
    n = len(color_list)
    
    x, y = obj_list[0].raw.columns
    
    with pd.ExcelWriter(obj_list[-1].output_path + "EIS_total.xlsx") as writer:
        for i, exp in enumerate(obj_list):
            plt.plot(exp.raw[x], exp.raw[y], label = exp.name, color = color_list[i%n])
            (exp.raw[[x, y]]
             .to_excel(writer, startcol = 2*i, index = False, header = [f'{i}', exp.name] )
             
             )

    leg = plt.legend(fontsize = 8)
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlim(0, 300)
    plt.ylim(0, 300)
    plt.xlabel("$Z'[Ohms]$", fontsize = 12)
    plt.ylabel("$-Z''[Ohms]$", fontsize = 12)




        
        
        


def main(date_path = year_path):    
    done = False

    while not done:
        check = input("select method: splitting total data(x) or not (c): ")
        
        
        if check.lower() == "x":
            done = True
            
            raw, path, _, _ = fileloads(date_path, ".xlsx")
            if not os.path.exists(f'{path}raw_split\\'):
                
                exp_obj = build_data(path, raw, EIS_tot)
            
            raw_path = f'{path}raw_split\\'
            raw_list = [_ for _ in os.listdir(raw_path) if _.endswith(".csv")]

            sep_obj = build_data(raw_path, raw_list, EIS_raw)
            raw_plot(raw_path, sep_obj)
            
        elif check.lower() == "c":
            
            done = True
            
            raw, path, _, _ = fileloads(date_path, ".csv")
            sep_obj = build_data(path, raw, EIS_raw)
            raw_plot(path, sep_obj)
            
        else:
            print("Unvalid option!!\n")


if __name__ == "__main__":
    main()