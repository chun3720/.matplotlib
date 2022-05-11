# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:06:16 2021
last update : Feb 15 2022
@author: jycheon
"""
from loadexp import *
import pandas as pd
import os
import string
from matplotlib import pyplot as plt
import seaborn as sns
# plt.style.use('science')
plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"

class LIB_builder(Dataloads):  
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        # (self.name, self.ext) = self.file.split('.')
        self.df = pd.read_excel(self.file_path, sheet_name = 1 , index_col = 0) 
        # self.df.set_index('인덱스', inplace = True)
        self.null = self.df[self.df['|용량_s|(Ah/g)'] == 0].index
        self.df = self.df.drop(self.null)
        self.min = self.df['전압(V)'].idxmin()
        self.max = self.df['전압(V)'].idxmax()
    
    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def df_indexing(self):
        if self.df.iloc[0, 1] > self.df.iloc[5, 1]:
            self.negative = self.df.loc[:self.min]
            self.positive = self.df.loc[self.min+1 :]  
        else:
            self.positive = self.df.loc[:self.max]
            self.negative = self.df.loc[self.max +1 :]
            
    def get_name(self):
        return self.name
    
    def get_check(self):
        return self.df.loc[self.min, '전압(V)']
              
    def get_discharge(self):
        return self.df.loc[self.max]
        
    def get_charge(self):
        return self.df.loc[self.min]
    
    def GCD_plot(self, color_list):    
        
        plt.plot(self.negative['|용량_s|(Ah/g)'], self.negative['전압(V)'], '-', color_list, label = LIB_builder.__str__(self))
        plt.plot(self.positive['|용량_s|(Ah/g)'], self.positive['전압(V)'], '-', color_list)

def get_plot(path, exp):
    n = len(exp)
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'purple', 'dimgrey', 'hotpink', 'steelblue', 'mediumseagreen', 'm']
    k = len(color_list)
    progress_bar(0, n)
    for i, gcd in enumerate(exp):
    # for i in range(len(exp)):
        X, Y =  gcd.df.columns[0], gcd.df.columns[1]
        gcd.df_indexing()
        plt.plot(gcd.negative[X], gcd.negative[Y], color_list[i%k], label = gcd.name)
        plt.plot(gcd.positive[X], gcd.positive[Y], color_list[i%k])
        # gcd.GCD_plot(color_list[i%k])   
        progress_bar(i+1, n)
    plt.xlabel('Capacity (Ah/g)')
    plt.ylabel(r'Potential (V vs. Li/Li$^+$)') 
    # plt.xlim()
    # try:
    #     test = exp[1].get_check()
    #     if test <0.5 or 3.1 > test > 2.8:   
    #         plt.ylabel(r'Potential (V vs. Li/Li$^+$)')  
    #     else:
    #         plt.ylabel('Voltage (V)')
    # except:
    #     plt.ylabel(r'Potential (V vs. Li/Li$^+$)') 
    
    leg = plt.legend(fontsize = 'xx-small')
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
    plt.savefig(path + '_GCD.png', dpi=300)

def get_result(path, exp_obj):
    for exp in exp_obj:
    # for i in range(len(exp)):
        print(exp.name.rjust(42))
        print(exp.get_charge())
        print('------------------------------------------')
        print(exp.get_discharge(), end='\n')
        print('==========================================')       
    print('\nDone!\n')   
    # try:    
    #     test = exp[1].get_check()
    #     if test < 0.5:
    #         print(">>> anode <<<")
    #     elif 3.1 > test >2.8:
    #         print(">>> cathode <<<")
    #     else:
    #         print(">>> full cell <<<")
    # except:
    #     pass

def get_export(path, exp):
    output_path = os.path.join(path, 'output\\')
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)    
    
    for i, ex in enumerate(exp):
        # writer = pd.ExcelWriter()
        # writer.close()
        with pd.ExcelWriter(output_path + ex.name + '_corrected.xlsx') as writer:
            ex.negative.to_excel(writer, sheet_name = 'negative')
            ex.positive.to_excel(writer, sheet_name = 'postiive')
            
    with pd.ExcelWriter(output_path + 'total.xlsx') as writer:
        n = len(exp)
        progress_bar(0, n)
        for ix, gcd in enumerate(exp):
            df = pd.concat([gcd.negative.reset_index(drop = True),
                            gcd.positive.reset_index(drop = True)], axis = 1)
                
            # df1 = gcd.negative.copy()
            # df2 = gcd.positive.copy()
            # df1.reset_index(drop = True, inplace = True)
            # df2.reset_index(drop = True, inplace = True)
            # df = pd.concat([df1, df2], axis = 1)
            df.columns = [f"Charge_{i}", f"V_{i}", f"Discharge_{i}", gcd.name]                
            df.to_excel(writer, startcol = 4*ix, index = False)
            progress_bar(i+1, n)

def main() -> None:
    raw_list, path, _ , _ = fileloads(year_path, '.xlsx')
    exp_data = build_data(path, raw_list, LIB_builder)
    get_plot(path, exp_data)
    get_result(path, exp_data)
    get_export(path, exp_data)

    


if __name__=="__main__":
    main()


