# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:51:00 2022

@author: user
"""

import os
import importlib
from pathlib import Path
from loadexp import get_data_folder
import sys



def runCSR(direct = False):

    path = os.getcwd()
    parent_path = Path(path).parent
    child_path = os.path.join(path, "CSR")
    
    
    if str(parent_path) not in sys.path:
        sys.path.append(str(parent_path))
        sys.path.append(path)
    
    # import ForMatplotlib
    if direct:
        code_list = [_ for _ in os.listdir(path) if _.endswith(".py")]
    else:
        code_list = [_ for _ in os.listdir(child_path) if _.endswith(".py")]
    to_ignore = ["__init__.py", "loadexp.py", "Player.py", "Battery_GCDplot_old.py", "__main__.py"]
    codes = [_ for _ in code_list if _ not in to_ignore]    
    # code_dict = {i:code for i, code in enumerate(codes)}
    code_dict = dict(enumerate(codes))
    
    for key, value in code_dict.items():
        print(f'{key} : {value}')
    
    selector = input("which file want to run: ")
    chosen = int(selector)
    year_path = get_data_folder(code_dict[chosen]) 
    to_import, ext = os.path.splitext(code_dict[chosen])
    
    # package_to_load = f'ForMatplotlib.{to_import}'
    package_to_load = f'CSR.{to_import}'
    module = importlib.import_module(package_to_load)
    
    print("\n\n")
    print(f"Current package: {package_to_load}\n")
    
    module.main(year_path)
    

    
if __name__ == "__main__":
    # year_path = get_data_folder()
    runCSR(True)

# GUI_load()


    

