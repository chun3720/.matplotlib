# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:15:23 2021
last update : Feb 15 2022
@author: jycheon
"""

import os
from dataclasses import dataclass
from typing import List
from pathlib import Path

def path_gen(path: str, file_ext: str = None) -> str:
    print('\nCurrent path: ')
    print('--------------------------------------------------------------------------------------')
    print(path)
    print('--------------------------------------------------------------------------------------')
    
    
    # path_folder = os.listdir(path)
    
    if file_ext is not None:

        path_folder = [_ for _ in os.listdir(path) if _.endswith(file_ext)]
        
    else:
        path_folder = os.listdir(path)
        
    path_dict = dict(enumerate(path_folder))
    
    for key, val in path_dict.items():
        print(f'{key} : {val}')
        
    print('==========================================')       
    
    return path_dict
    


def get_sort(listitem: List, KeyFunction: object) -> List[str]:
    sorted_list = sorted(listitem, key = KeyFunction)
    return sorted_list

def raw_check(path: str, file_ext: str) -> List:
        # check_list = os.listdir(path)
        check_true = [_ for _ in os.listdir(path) if _.endswith(file_ext)]
        if len(check_true) != 0:
            with_path = [os.path.join(path,_) for _ in check_true]    
            sorted_list = get_sort(with_path, os.path.getmtime)  
            file_only_list = [os.path.basename(_) for _ in sorted_list]
            return file_only_list
        # else:
        return check_true

def fileloads(year_path: str, file_ext: str) -> List:  
    year_dict = path_gen(year_path)
    folder_select = input("Select folder to analyze, (move to parent path: type(.):  ")
    
    if not folder_select:
        raise SystemExit("Cancelling: no folder selected")
        
    elif folder_select == ".":
        parent_path = Path(year_path).parent
        
        return fileloads(parent_path, file_ext)
    
    else:
        
        # date_path = year_path + '\\' + year_dict[int(folder_select)] + '\\'
        date_path = os.path.join(year_path, year_dict[int(folder_select)]) + '\\'
        list_check = raw_check(date_path, file_ext) 
        if len(list_check) !=0:
            list_true = list_check
            path_true = date_path
            path_gen(path_true, file_ext)
            EXP_title = year_dict[int(folder_select)].replace("_", "-")
            return (list_true, path_true, year_dict[int(folder_select)], EXP_title)  
        # else:
        return fileloads(date_path, file_ext)
        
    

def progress_bar(progress: int, total: int) -> None:
    percent = 100 * (progress / float(total))
    bar = '■' * int(percent) + '-' * (100 - int(percent))
    print(f"\r{bar}| {percent:.2f}%", end = "\r")

# class Dataloads(object):
#     def __init__(self, path, file):
#         self.path = path
#         self.file = file
#         self.file_path = os.path.join(self.path, self.file)
#         # self.test = os.path.splitext(self.file_path)
#         # self.name, self.ext = self.file.split('.')
#         self.name, self.ext = os.path.splitext(self.file)
        
@dataclass
class Dataloads:
    path : str
    file : str 
    
    def __post_init__(self):
        self.file_path = os.path.join(self.path, self.file)
        self.name, self.ext = os.path.splitext(self.file)
        
def build_data(path: str, file: List[str], builder: object) -> List[object]:
    "Build class of each file and return list of builded classes"
    data = []
       
    for item in file:
        # data.append(builder(path, item))
        try:
            data.append(builder(path, item))
        except:
            print(f'fail to load {item} file')
            pass
    return data

# from datetime import datetime

# print(datetime.now().isoformat(timespec = 'minutes'))
