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
import collections

# doc  = collections.defaultdict(str)

doc = {
    "Battery_cycle.py" : {
        "input": ".xlsx", 
        "help": "Capacity vs cycle, Wonatech"
        },
    
    "Battery_GCD_wonatech.py" : {
        "input":"xlsx", 
        "help": "legacy"},
    
    "BETplot_for_csv.py" :  {
        "input": ".csv", 
        "help": "legacy"},
    
    "BET_from_simple.py" : {
        "input": ".csv", 
        "help": "N2 physisorption (adsorption only data)" },
    
    "Capacity_from_mpr.py": {
        "input": ".mpr", 
        "help": "jyc_only"},
    
    "EC_DLCplot_from_CV_old.py": {
        "input": "txt", 
        "help": "legacy"},
    
    "EC_DLC_from_CV_mpt.py": {
        "input": ".mpt", 
        "help":"EDLC from CV, Biologic"},
    
    "EC_DLC_fit_report.py": {
        "input": "xlsx", 
        "help": "legacy"},
    
    "EIS_wonatech.py": {
        "input": ".xlsx", 
        "help": "get total EIS graph, Wonatech"},
    
    "Export_path.py": {
        "input": "None", 
        "help":"make path_ref.xlsx"},
    
    "mpt_separation.py": {
        "input" : ".mpt", 
        "help": "Capacity from total cycle, Biologic"},
    
    "Other_EMI.py": {
        "input": ".s2p", 
        "help" : "Electromagnetic shielding"},
    
    "Pkl2Excel.py": {
        "input" : ".pkl", 
        "help" : "simple conversion"},
    
    "Pqt2Excel.py": {
        "input": ".pqt", 
        "help" : "simple conversion"},
    
    "Set_path.py": {
        "input": "None", 
        "help" : "appyly for path_ref.xlsx"},
    
    "Strength_csv.py": {
        "input": ".csv", 
        "help" : "Stress vs strain"},
    
    "Supercap_GCD_mpt.py": {
        "input": ".mpt", 
        "help" : "Voltage vs Capacity for battery, Biologic"},
    
    "Supercap_GCD_mpt_legacy.py": {
        "input": ".mpt", 
        "help" : "CV and GCD for Supercap, Biologic"},
    
    "Supercap_GCD_Wonatech.py": {
        "input": ".xlsx", 
        "help" : "Supercap for Wonatech"},
    
    "Supercap_mpr.py": {
        "input": ".mpr", 
        "help" : "jyc_only"},
    
    "Unifiying wrd.py": {
        "input": ".wrd", 
        "help" : "merging wrd file location"},
    
    "Wonatech_CSV_reordering.py": {
        "input": ".csv", 
        "help": "one-click battery analysis, Wonatech"},
    
    "wonatech_for_csv.py": {
        "input": ".csv", 
        "help": "plot for selected cycle, Wonatech"}
        }





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
    to_ignore = ["__init__.py", "loadexp.py", "Player.py", "Battery_GCDplot_old.py", "__main__.py", \
                 "pilot.py", "separator_wonatech.py", "bat_ex.py", "EC_EIS.py", "mover.py"]
    codes = [_ for _ in code_list if _ not in to_ignore]    
    # code_dict = {i:code for i, code in enumerate(codes)}
    code_dict = dict(enumerate(codes))
    
    for key, value in code_dict.items():
        key = str(key)
        value = str(value)
        analysis = doc[value]
        d = analysis["input"]
        h = analysis["help"]
        print(f'[{key.rjust(2)}] :', end = " ")
        print(value.ljust(30, '_'), end = '')
        print(d.rjust(10, '_'), end = "")
        print(h.rjust(50, "_"), end = "-----")
        print(f'[{key.rjust(2)}]' )
        
        # print(f"{doc[value].ljust(6)}")

    selector = input("\nwhich file want to run: ")
    chosen = int(selector)
    
    
    year_path = get_data_folder(code_dict[chosen]) if code_dict[chosen] not in \
        ["Set_path.py", "Export_path.py", "Pkl2Excel.py", "Wonatech_CSV_reordering.py", \
         "EC_DLC_fit_report.py", "Unifiying wrd.py"] \
            else path
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


    

