# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:51:00 2022

@author: user
"""

import os
import importlib

from pathlib import Path


env = os.environ




data_path = r"D:\Researcher\JYCheon\DATA"
path = os.getcwd()
parent_path = Path(path).parent



new_path = str(parent_path) + env["PATH"]

env["PATH"] = new_path






code_list = [_ for _ in os.listdir(path) if _.endswith(".py")]
to_ignore = ["__init__.py", "loadexp.py", "Player.py"]
codes = [_ for _ in code_list if _ not in to_ignore]    
code_dict = {i:code for i, code in enumerate(codes)}
    

for key, value in code_dict.items():
    print(f'{key} : {value}')


selector = input("which file want to run: ")
chosen = int(selector)

to_import = code_dict[chosen][:-3]

import ForMatplotlib
package_to_load = f'ForMatplotlib.{to_import}'
module = importlib.import_module(package_to_load)
    

print("\n\n")
print(f"Current package: {package_to_load}\n")

module.main()