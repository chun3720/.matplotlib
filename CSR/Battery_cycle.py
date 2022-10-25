# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:06:16 2021
last update : Feb 15 2022
@author: jycheon
"""
from loadexp import Dataloads, fileloads, build_data
import pandas as pd
import os
from matplotlib import pyplot as plt

plt.style.use(['science', 'no-latex'])
year_path = r"D:\Researcher\JYCheon\DATA\Electrochemistry\Coin cell\2022"



class LIB_tot(Dataloads):
    # df_list = []
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.data = pd.read_excel(self.file_path, sheet_name = '데이터_1_1', names = ["cycle number", "Capacity"])
        self.unit = "(Ah/g)"
        self.x, self.y  = self.data.columns
        self.X = self.data[self.x]
        self.Y = self.data[self.y]

    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
   

def plot_setup(leg, title, xlabel, ylabel):
    
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
  

def export_with_plot(cols, exp_obj, writer, idx, basis = 1000, header = False):
    
    exp_obj.data[cols].assign(Capacity = exp_obj.data[cols][exp_obj.y] * basis).to_excel(writer, startcol =  2*idx, index= False, header = header)
    plt.plot(exp_obj.X, exp_obj.Y*basis, 'o', label = exp_obj.name)

    
def get_export(exp, path, check = 'n', convertor = 'n'):
    output_path = f'{path}output\\'
    cols = exp[0].data.columns

    if not os.path.exists(output_path):
        os.mkdir(output_path) 

    if check == 'y':
        
        with pd.ExcelWriter(f'{output_path}Cycle_tot.xlsx') as writer:
            for i, cy in enumerate(exp):
                
                export_with_plot(cols, cy, writer, i, header = ["mAh/g", cy.name])          
            
            leg = plt.legend(fontsize = 'xx-small')            
            plot_setup(leg, "","Cycle number", "Specific Capacity ($mAh/g$)" )
            
       
        if convertor != 'n':
            
            with pd.ExcelWriter(f'{output_path}Cycle_recalculation.xlsx') as writer:

                for i, cy in enumerate(exp):
                    
                    quest = input(f"type conversion factor(C) for '{cy.file}', ex) new_value = prev_value * C: ")
                    basis = float(quest)
                    
                    export_with_plot(cols, cy, writer, i, basis*1000, header = ["mAh/g(re)", cy.name])          
                    
                leg = plt.legend(fontsize = 'xx-small')
                plot_setup(leg, "recalculation", "Cycle number", "Specific Capacity ($mAh/g_{re}$)" )
                
    else:
        with pd.ExcelWriter(f'{output_path}Cycle_tot.xlsx') as writer:
    
            for i, cy in enumerate(exp):
                (
                 cy.data.rename(columns = {"cycle number": "Ah/g", "Capacity": cy.name})
                 .to_excel(writer, startcol = 2*i, index = False)   
                    )
                  
                
        if convertor != 'n':

            with pd.ExcelWriter(f'{output_path}Cycle_recalculation.xlsx') as writer:

                for i, cy in enumerate(exp):
                    quest = input(f"type conversion factor for '{cy.file}' (make sure it means denominator): ")
                    basis = float(quest)                    
                    export_with_plot(cols, cy, writer, i, basis, header = ["Ah/g(re)", cy.name])          

                leg = plt.legend(fontsize = 'xx-small')    
                plot_setup(leg, "recalculation", "Cycle number", "Specific Capacity ($Ah/g_{re}$)" )
                    

def cycle_plt(exp):
    
    for ex in exp:
        name = ex.name.replace("_", "-")
        plt.plot(ex.X, ex.Y, 'o', label = name)
        
    leg = plt.legend(fontsize = 'xx-small')
    plot_setup(leg, "","Cycle number", "Specific Capacity ($Ah/g$)" )
    

def main(py_path):
    
    raw, path, _, _ = fileloads(py_path, ".xlsx")
    exp_data = build_data(path, raw, LIB_tot)
    
    cycle_plt(exp_data)
    check = input("convert to mAh/g? yes (y) or no (n) :")
    convertor  = input("want to recalculate ? yes (y) or no (n) :")
    
    get_export(exp_data, path, check.lower(), convertor.lower())
    
if __name__ == "__main__":
    main(year_path)



