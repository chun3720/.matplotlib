# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 09:16:41 2022

@author: user
"""

import os
from pathlib import Path
from loadexp import GUI_load
import importlib
import sys

year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022"

# path = GUI_load()


def built_in(path_list):
    curr_path = Path(os.getcwd())
    sys.path.append(curr_path.name)
    
    module = importlib.import_module("wonatech_for_csv")
    
    for path in path_list:
        try:
            module.main(path, True)
        except:
            pass
        
    




def main(date_path = year_path):
    date_path = GUI_load()

    mother_path = Path(date_path)
    dc_files = [_ for _ in mother_path.iterdir() if "DC" in _.name]
    cyc_files = [_ for _ in mother_path.iterdir() if "CYC" in _.name]
    
    sub_paths = []
    for dc, cyc in zip(dc_files, cyc_files):
        
        folder_name = dc.name[:-7]
        
        child_path = mother_path.joinpath(folder_name)
        sub_paths.append(child_path)
        if not child_path.exists():
            child_path.mkdir()
        
        dc.rename(child_path/dc.name)
        cyc.rename(child_path/cyc.name)
    
    built_in(sub_paths)
    
    
    
    
    



if __name__ == "__main__":
    main(year_path)
    

    
    
    
    
    
    
 
    




