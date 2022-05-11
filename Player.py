# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:51:00 2022

@author: user
"""

import os
import importlib
import ForMatplotlib


path = os.getcwd()
code_list = [_ for _ in os.listdir(path) if _.endswith(".py")]

code_dict = {}

for i, code in enumerate(code_list):
    code_dict[i] = code
    

for key, value in code_dict.items():
    print(f'{key} : {value}')










selector = input("which file want to run: ")
chosen = int(selector)


to_import = code_dict[chosen][:-3]

# from ForMatplotlib import to_import
# main()

package_to_load = f'ForMatplotlib.{to_import}'
module = importlib.import_module(package_to_load)
    
# importlib.resources.files(to_import)
print("\n\n")
print(f"Current package: {package_to_load}\n")
module.main()