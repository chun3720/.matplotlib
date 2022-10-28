# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:33:43 2022

@author: user
"""



import os
from pathlib import Path
from typing import List

def path_gen(path: Path, file_ext: str) -> dict:
    print('\nCurrent path: ')
    print('--------------------------------------------------------------------------------------')
    print(path)
    print('--------------------------------------------------------------------------------------')
        
    # path_folder = [_ for _ in path.iterdir() if _.name.endswith(file_ext)]    
    path_folder = list(path.iterdir())
    path_dict = dict(enumerate(path_folder))
    
    for key, val in path_dict.items():
        print(f'{key} : {val.name}')
        
    print('==========================================')       
    
    return path_dict
    
def raw_check(path: Path, file_ext: str) -> List[Path]:
    
    check = list(path.iterdir())
    print(check)
    
    if check:
        raw_list = [_ for _ in path.iterdir() if _.name.endswith(file_ext)]
        
        return sorted(raw_list, key = os.path.getmtime)
    
    return False

        
path =  r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1027 NCMLTO PVDF pouch air fab"

year_path = Path(path)


def fileloads(year_path: Path, file_ext: str) -> List[Path]:
    
    year_dict = path_gen(year_path, "*")
    folder_select = input("Select folder to analyze, (move to parent path: type(.):  ")
    
    if not folder_select:
        raise SystemExit("Cancelling: no folder selected")
        
    elif folder_select == ".":
        parent_path = Path(year_path).parent
        
        return fileloads(parent_path, file_ext)
    
    else:
        chosen_path = year_dict[int(folder_select)]
        
        check = raw_check(chosen_path, file_ext)
        
        if check:
            
            return check
        
        
        return fileloads(chosen_path, file_ext)
            

        
ans = fileloads(year_path, "mpt")
    
    





        
