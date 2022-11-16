# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 17:13:01 2022

@author: user
"""

import os
from pathlib import Path, PureWindowsPath
import pandas as pd


def convertor(item):
    
    try:
        return Path(item)
        # return PureWindowsPath(item)
    
    except:
        pass



def main(year_path):
    path = Path(os.getcwd())
    
    path_ref = "path_ref.pkl"
    xl_ref = "path_ref.xlsx"
    
    pkl_path = path.parent.parent.joinpath(path_ref)
    xl_path = path.parent.parent.joinpath(xl_ref)
    
    
    df = pd.read_excel(xl_path, index_col = 0)
    
    df.path_name = df.path_name.apply(lambda x: convertor(x))
    
    df.fillna(0).to_pickle(pkl_path)
    # df.to_pickle(pkl_path)
    

if __name__ == "__main__":
    main(Path.cwd())