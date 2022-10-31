# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:29:01 2022

@author: user
"""
from loadexp import GUI_load
from pathlib import Path
import pandas as pd
from datetime import date
year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw"


def main(py_path = year_path):
    a = date.today()
    b = date.isoformat(a)
    c = b.replace("-", "")
    
    
    tot_path = GUI_load()
    
    curr_path = Path(tot_path)
    
    # sample_file = "D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1028 ecsa drying condition\Tot\60 VAC_summary.xlsx"
    xls = [_ for _ in curr_path.iterdir() if _.name.endswith("xlsx")]
    
    tot_df = pd.DataFrame()
    header_tot = []
    
    for xl in xls:
        df = pd.read_excel(xl, index_col = 0)
        header = list(df.columns)
        tot_df = pd.concat([tot_df, df], axis = 1, ignore_index = True)
        header_tot += header
        
    
    sub_path = curr_path.joinpath("report")
    
    if not sub_path.exists():
        sub_path.mkdir()
        
    final_file = sub_path.joinpath(f"{c}_report.xlsx")
    
    tot_df.to_excel(final_file, header = header_tot)
    
    
if __name__ == "__main__":
    main(year_path)