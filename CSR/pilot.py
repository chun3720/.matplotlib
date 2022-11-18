# from loadexp import Dataloads, fileloads, build_data
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import openpyxl
from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass
from datetime import date


a = date.today()
b = date.isoformat(a)

c = b.replace("-", "")



file = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022\1027 newenw\1012_NCMLTO_PVDF_activation_077\split\cycle_2.pqt"


path = Path(file)


file2 = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1028 ecsa drying condition\60 VAC\1\output\60 VAC@1_summary.xlsx"


path2 = Path(file2)


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
            self.file_path = self.path_obj.joinpath(self.file)
            self.name, self.ext = os.path.splitext(self.file)
        
        
        
            
            
    
    
test_file = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1103 mpt sep test\1101 NCMLTO PVDF pouch GB fab LT10ET50 1103 wo 5kg.mpt"

test_obj = Path(test_file)


exp_obj = Dataloads(test_obj)


exp_obj2 = Dataloads(test_obj.parent, test_obj.name)


hdf_file = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1116 NCMLTO PVDF Epoxy w 60 vac 2h\output\Capacity_tot.hdf5"

df = pd.read_hdf(hdf_file, key = "tot_df")

# from galvani import BioLogic
# mpr = r"D:\Researcher\JYCheon\DATA\Electrochemistry\2022\Raw\1116 NCMLTO PVDF Epoxy w 60 vac 2h\1116 NCMLTO PVDF Epoxy w 60 vac 2h.mpr"
# mpr_file = BioLogic.MPRfile(mpr)

# df = pd.DataFrame(mpr_file.data)