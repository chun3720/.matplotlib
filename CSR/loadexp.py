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
import PySimpleGUI as sg
import pandas as pd


def path_gen(path: str, file_ext: str = None) -> str:
    print('\nCurrent path: ')
    print('--------------------------------------------------------------------------------------')
    print(path)
    print('--------------------------------------------------------------------------------------')
    
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

def fileloads(year_path: str, file_ext: str) -> List[str]:  
    year_dict = path_gen(year_path)
    done = False
    n = len(year_dict)
    while not done:
        
        folder_select = input("Select folder to analyze, (move to parent path: type(.):  ")
        
        if folder_select.isnumeric() and int(folder_select) in range(n) or folder_select == ".":
            done = True
            break
        print("Invalid input! retry")
        
    # if not folder_select:
    #     raise SystemExit("Cancelling: no folder selected")
        
    if folder_select == ".":
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
        

def GUI_load():
    dir_path = sg.popup_get_folder("Select Folder")
    if not dir_path:
        sg.popup("Cancel", "No folder selected")
        raise SystemExit("Cancelling: no folder selected")
        
    else:
        sg.popup(f"The folder you chose was {dir_path}")
        
    return dir_path

# @dataclass
# class Dataloads:
#     path : str
#     file : str 
    
#     def __post_init__(self):
#         self.path_obj = Path(self.path)        
#         self.file_path = self.path_obj.joinpath(self.file)
#         self.name, self.ext = os.path.splitext(self.file_path.name)
        
@dataclass
class Dataloads:
    
    path : str
    file : str = None
    
    def __post_init__(self):
        
        if self.file is None:
            
            self.file_path = self.path
            self.path = self.file_path.parent
            self.name, self.ext = self.file_path.stem, self.file_path.suffix
            
        else:
            self.path_obj = Path(self.path)
            # self.file_path = self.path_obj.joinpath(self.file)
            self.file_path = self.path_obj.joinpath(self.file)
            self.name, self.ext = os.path.splitext(self.file)



        
def build_data(path: str, file: List[str], builder: object) -> List[object]:
    "Build class of each file and return list of builded classes"
    data = []
       
    for item in file:
        data.append(builder(path, item))
        # try:
        #     data.append(builder(path, item))
        # except:
        #     print(f'fail to load {item} file')
        #     pass
    return data

# from datetime import datetime

# print(datetime.now().isoformat(timespec = 'minutes'))

def get_data_folder(py_name):


    curr_path = Path(os.getcwd())
    
    mother_path = curr_path.parent.parent
    
    path_info = "path_ref.pkl"
    
    path_file = mother_path.joinpath(path_info)
    
    if path_file.exists():
        df = pd.read_pickle(path_file)
        
        # print("yes")
    else:
        
        year_path = Path(GUI_load())
        
        info = {"python_name": [f"{py_name}", "Capacity_norm_op", "Capacity_specific_op"
                                , "originpro"],
                "path_name" : [year_path, "", "", mother_path.joinpath("OriginPro")],
                "op" : ["", "", "", ""]}
        
        df = pd.DataFrame(info)
        df = df.set_index("python_name")
        
        df.to_pickle(path_file)
        
        return year_path
    
    try:
        year_path = df["path_name"].loc[py_name]
    except KeyError:
        print(f"\nError! path for {py_name} does not exist. Please check")
        year_path = Path(GUI_load())
        df.loc[py_name] = year_path, ""
        # df["path_name"].loc[py_name] = year_path
        df.to_pickle(path_file)
        
        return year_path
        
    
    if not year_path.exists():
        print("path does not exists. please select")
        year_path = Path(GUI_load())
        df.loc[py_name] = year_path, ""
        df.to_pickle(path_file)
        
    
    return year_path

