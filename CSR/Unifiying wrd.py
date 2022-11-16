# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:43:03 2022

@author: user
"""

from loadexp import GUI_load
from pathlib import Path


year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022"


def main(date_path = year_path):
    path = GUI_load()
    
    mother_path = Path(path)
    
    
    files = []
    
    for item in mother_path.glob("**/*.wrd"):
        
        files.append(item)
        
         
    for file in files:
        file.rename(mother_path/file.name)
    
if __name__ == "__main__":
    main(year_path)
# for folder in mother_path.iterdir():
#     if folder.is_dir():
#         folder.rmdir()