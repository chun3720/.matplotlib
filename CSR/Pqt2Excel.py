# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:36:13 2022

@author: user
"""

import pandas as pd
from loadexp import Dataloads, build_data, GUI_load
import os
from tqdm import tqdm
# import xlsxwriter

year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw"



class Pqt2Xl(Dataloads):
    
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        
        self.df =  pd.read_parquet(self.file_path)
        self.xl_name = f"{self.name}.xlsx"
        self.target_file = os.path.join(self.path, self.xl_name)
        
    
    def get_xl(self):
        
        self.df.to_excel(self.target_file, engine = 'xlsxwriter', index  =  False)
        
        # with pd.ExcelWriter(self.target_file, engine = "xlsxwriter") as f:
        #     self.df.to_excel(f, index  =  False)
            
        
        
        
        

def get_conversion(objs):
    
    for obj in tqdm(objs):
        # df = tqdm(obj.df)
        obj.get_xl()
        
        

def main(date_path = year_path):

    date_path = GUI_load()
    # raw_list, path_dir, exp_name, exp_title = fileloads(date_path, '.pkl')
    
    raw_list = [_ for _ in os.listdir(date_path) if _.endswith("pqt")]
    exp_obj = build_data(date_path, raw_list, Pqt2Xl)   
    get_conversion(exp_obj)
    

if __name__ == "__main__":
    main(year_path)

