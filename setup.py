# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:32:25 2022

@author: user
"""

from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup








setup(
      name = "CSR",
      version = "0.1.0",
      author = "jae yeong cheon",
      author_email= "chun3720@hotmail.com",
      packages = find_packages(where = "CSR"),
      package_dir={'': 'CSR'},
      py_modules=[splitext(basename(path))[0] for path in glob('CSR/*.py')],
      include_package_data= True,
      install_requires = [
          
          "pandas",
          "numpy",
          "matplotlib",
          "scienceplots",
          "openpyxl",
          "seaborn",
          "tqdm",
          "pygaps",
          "impedance",
          "pyxlsb",
          
          
          
          
          
          
          ]
      
      
      
      
      )