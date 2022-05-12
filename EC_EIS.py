# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 13:28:31 2022

@author: user
"""

from loadexp import *
import pandas as pd
from impedance import preprocessing
from impedance.models.circuits import CustomCircuit
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist
from openpyxl import load_workbook
import numpy as np
# plt.style.use("science")

year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\EIS\\2022"

class EIS_builder(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        # self.df = pd.read_excel(self.file_path, sheet_name = 1, index_col = 0, engine="pyxlsb")
        # self.df = pd.read_excel(self.file_path, sheet_name = 1)
        self.df = pd.read_excel(self.file_path, sheet_name = 1, usecols = [8, 11, 12])
        # self.df.drop(columns = self.df.columns[:8], inplace = True)
        # self.df.drop(columns = self.df.columns[1:3], inplace = True)
        # self.df.drop(columns = self.df.columns[3:], inplace = True)
        self.outdf = self.df.copy()
        self.outdf.columns = ["Frequency", "Zreal_Ohm", "minusZim_Ohm"]
        # columns = ["Frequency_Hz", "Zreal_Ohm", "Zimg_Ohm"]
        self.outdf["minusZim_Ohm"] =  -self.outdf["minusZim_Ohm"]
        self.output_path = path + 'output\\'
        try:
            os.mkdir(self.output_path)    
        except FileExistsError:
            pass        
        # self.output_file = self.output_path +  self.name + '_Fit.xlsx'
        # self.temp_file = self.output_path +  self.name + '_corrected.csv' 
        # self.df.to_csv(self.temp_file, header = False, index = False)        
        # with pd.ExcelWriter(self.output_file) as writer:
        #     self.outdf.to_excel(writer, sheet_name = "Raw")

    def __str__(self):
        self.label = self.name.replace("_", "-").replace("#", "")
        return self.label
    
    
    def circuit_fit(self):
        frequencies, Z = preprocessing.readCSV(self.temp_file )   
        frequencies, Z  = preprocessing.ignoreBelowX(frequencies, Z)
        # self.circuit = 'R_0-p(R_1,CPE_1)-p(R_2-Wo_1,CPE_2)'
        # initial_guess = [10, 10, 10, 10, 10, 10, 10, 10 , 10]
        # self.circuit = CustomCircuit(self.circuit, initial_guess=initial_guess)
        # initial_guess = [
            # 1e-8,  #L0
            # .01,  #R0
            # .005,  #R1
            # .1,  #CPE1-1
            # .9, # CPE1-2
            # 1,  ###R2###
            # .1, #W12
            # 200, #W2
            # .1, #CPE2-1
            # # .9] #CPE2-2
        # test_guess = [2.64493471e-07, 1.60420253e+00, 1.86655122e+03, 1.02179188e-02,
        #  5.50566090e-01, 1.22411664e+02, 4.26450456e+01, 3.50146815e-01,
        #  1.82602116e-05, 8.28235768e-01]
        test_guess = [2.64493471e-07, 1.60420253e+00, 1, 1.02179188e-02,
          5.50566090e-01, 1.22411664e+02, 4.26450456e+01, 3.50146815e-01,
          1.82602116e-05, 8.28235768e-01]
        # circuit = CustomCircuit('L_0-R_0-p(R_1,CPE_1)-p(R_2-Wo_1,CPE_2)', initial_guess=initial_guess)
        self.circuit = CustomCircuit('L_0-R_0-p(R_1,CPE_1)-p(R_2-Wo_1,CPE_2)', initial_guess=test_guess)      
        self.circuit.fit(frequencies, Z)
        Z_fit = self.circuit.predict(frequencies)
        fig, ax = plt.subplots()
        plot_nyquist(ax, Z, fmt='o')
        plot_nyquist(ax, Z_fit, fmt='-')
        Rct = int(self.circuit.parameters_[5])
        # print(circuit.parameters_)
        plt.legend(['Data', 'Fit: '+ str(Rct)+ ' Ohm'])
        plt.title(EIS_builder.__str__(self))
        plt.xlim(0, 60)
        plt.ylim(0, 60)
        plt.show()
        self.fit = pd.DataFrame({"Real": Z_fit.real, "Img": -Z_fit.imag})
        
def raw_plot(path, exp):
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'm', 'gray', 'brown','darkcyan', 
                  'skyblue', 'hotpink', 'dodgerblue']
    n = len(color_list)
    
    
    with pd.ExcelWriter(exp[-1].output_path + "total.xlsx") as writer:
        for i in range(len(exp)):
            plt.plot(exp[i].outdf["Zreal_Ohm"], exp[i].outdf["minusZim_Ohm"], label = exp[i].__str__(), color = color_list[i%n])
            df = exp[i].outdf[exp[i].outdf.columns[1:]].copy()
            df.columns = ["X", exp[i].name]
            df.to_excel(writer, startcol = 2*i, index = False)
        
    
    leg = plt.legend(fontsize = 8)
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.xlim(0, 150)
    plt.ylim(0, 150)
    plt.xlabel("$Z'[Ohms]$", fontsize = 12)
    plt.ylabel("$-Z''[Ohms]$", fontsize = 12)
        
    
        
def fit_and_plot(path, exp):
    # res = []
    for i in range(len(exp)):
        exp[i].circuit_fit()
        book = load_workbook(exp[i].output_file)
        with pd.ExcelWriter(exp[i].output_file, engine = 'openpyxl') as writer:
            writer.book = book   
            exp[i].fit.to_excel(writer, sheet_name = "Fit")
        os.remove(exp[i].temp_file)
        
    
def main(default_path = year_path):
    raw_list, path, _, _ = fileloads(default_path, '.xlsb')
    exp_data = build_data(path, raw_list, EIS_builder)
    
    #fit_and_plot(path, exp_data)
    
    raw_plot(path, exp_data)
    
    
if __name__ == "__main__":
    main()












        