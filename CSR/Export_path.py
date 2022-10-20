# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 17:47:58 2022

@author: user
"""

import os
from pathlib import Path
import pandas as pd

def main(year_path):


    path = Path(os.getcwd())
    
    path_ref = "path_ref.pkl"
    xl_ref = "path_ref.xlsx"
    
    pkl_path = path.parent.parent.joinpath(path_ref)
    xl_path = path.parent.parent.joinpath(xl_ref)
    
    df = pd.read_pickle(pkl_path)
    
    df.to_excel(xl_path)
    

if __name__ == "__main__":
    main(Path.cwd())