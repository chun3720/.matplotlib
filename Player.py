# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:51:00 2022

@author: user
"""

import os
import importlib
from pathlib import Path
import sys

"""
modify the below 'data_path' for your data folder path
"""
data_path = r"D:\Researcher\JYCheon\DATA"

path = os.getcwd()
parent_path = Path(path).parent

if str(parent_path) not in sys.path:
    sys.path.append(str(parent_path))

import ForMatplotlib

code_list = [_ for _ in os.listdir(path) if _.endswith(".py")]
to_ignore = ["__init__.py", "loadexp.py", "Player.py"]
codes = [_ for _ in code_list if _ not in to_ignore]    
# code_dict = {i:code for i, code in enumerate(codes)}
code_dict = dict(enumerate(codes))

for key, value in code_dict.items():
    print(f'{key} : {value}')

selector = input("which file want to run: ")
chosen = int(selector)
to_import = code_dict[chosen][:-3]

package_to_load = f'ForMatplotlib.{to_import}'
module = importlib.import_module(package_to_load)

print("\n\n")
print(f"Current package: {package_to_load}\n")

module.main()
# module.main(data_path)