# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 08:44:21 2021

@author: user
"""
from loadexp import *
import pandas as pd
import os
import numpy as np
# from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
# from sklearn.linear_model import HuberRegressor
plt.style.use(['science', 'no-latex'])
year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2021\\Raw"
    
def dlc_func(x, a, b):   
    return a*x + b

class DLC_builder(Dataloads):   
    dlc_current = []
    dlc_rate = []
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.df = pd.read_csv(self.file_path, sep = "\t", engine='python', encoding = "utf-8")
        self.df.drop(columns = 'Unnamed: 2', inplace = True)
        self.appl_input = ''
        
    def get_filename(self):
        return self.file
    
    def shift_to_OCP(self):
        self.ocp = self.df.loc[0, 'Ewe/V']
        self.df['Ewe/V'] = self.df['Ewe/V'].apply(lambda x: x-self.ocp)
        
        
    def get_mpl(self, condition):
        self.condition = condition
        self.condition_path = os.path.join(self.path, self.condition)
    
    def get_condition(self, skips = 35):
        self.condition_df = pd.read_csv(self.condition_path, skiprows = skips, encoding = "utf-8") 
        self.target = self.condition_df.columns[0] 
        if self.target[:5] == 'dE/dt':
            # self.appl_input = ''
            for i in self.target:
                if i.isnumeric():
                    self.appl_input += str(i)
                if i == '.':
                    break        
        else:
            # DLC_builder.get_condition(self, skips + 1)
            return self.get_condition(skips + 1)

    def set_rate(self):
        # self.get_condition()
        DLC_builder.dlc_rate.append(int(self.appl_input))
        
    def CV_plot(self):      
        plt.plot(self.df['Ewe/V'], self.df['<I>/mA']) 
        plt.xlabel('Potential (V vs. OCP)', fontsize=13)
        plt.xlim(-0.06, 0.06)
        plt.xticks(fontsize=11)
        plt.ylabel('Current (mA)', fontsize=13)
        # plt.ylim(-0.02, 0.02)
        plt.yticks(fontsize=11)
        plt.tight_layout()
    
    def get_dlc(self):
        self.get_condition()
        self.dlc = self.df.copy()
        self.filt = self.dlc[self.dlc['Ewe/V']    < 0].index
        self.dlc = self.dlc.drop(self.filt)
        self.min = self.dlc.loc[2:, 'Ewe/V'].idxmin()
        self.point = (self.dlc.loc[0, '<I>/mA'] - self.dlc.loc[self.min, '<I>/mA'])/2
        DLC_builder.dlc_current.append(self.point)

    def dlc_fit(self):       
        # self.X = np.array( [5, 10, 20, 30, 40, 50])
        self.X = np.array(DLC_builder.dlc_rate)
        self.Y = np.array(DLC_builder.dlc_current)
        # self.popt, self.pcov = curve_fit(dlc_func, self.X, self.Y)
        # self.fit = dlc_func(self.X, *self.popt)
        ## via np.linalg method
        n = len(self.X)
        A = np.vstack((self.X, np.ones(n))).T
        XX, resid, _, _ = np.linalg.lstsq(A, self.Y, rcond = None)
        self.m, self.k = XX
        

              
    def dlc_result(self):       
        dlc_rs = pd.DataFrame({'Scan rate (mV/s)' : self.X, 'DLC current (mA)' : self.Y, 'Fitted (mA)' : self.m*self.X})
        dlc_rs.set_index('Scan rate (mV/s)', inplace = True)
        dlc_rs.loc[5, 'Total Capacitance (uF)'] = self.m*1000000
        dlc_rs.loc[5, 'Length Capacitance (uF/cm)'] = self.m*1000000/3
        return dlc_rs
    
    def dlc_plot(self):        
        plt.scatter(self.X, self.Y)
        # plt.plot(self.X, self.fit, 'r-', label = "LS: " + str(int((self.popt[0]*1000000)/3)) +  r' $\mu$F/cm')
        plt.plot(self.X, self.m*self.X + self.k, 'r-', label = str(int(self.m*1000000/3))+ r' $\mu$F/cm')
        plt.xlabel('Scan Rate (mV/s)', fontsize=13)
        plt.xlim(0, 60)
        plt.xticks(fontsize=11)
        plt.ylabel('DLC Current (mA)', fontsize=13)
        # plt.ylim(0, 0.01)
        plt.yticks(fontsize=11)
        plt.tight_layout()
        plt.legend(fontsize=14)
                  
def get_CVplot(path, exp, exp_path, exp_title, exp_dict):
    for i in range(len(exp)):
        exp[i].shift_to_OCP()
        exp[i].get_mpl( exp_dict[exp[i].get_filename()]             )
        exp[i].get_dlc()
        # exp[i].get_condition()  
        exp[i].set_rate()
        exp[i].CV_plot()        
    plt.title(exp_title, fontsize = 10)
    plt.savefig(path + exp_path + '_CV.png', dpi=600)
    plt.show()
    
def get_DLCplot(path, exp, exp_path, exp_title):
    exp[-1].dlc_fit()
    dlc_df = exp[-1].dlc_result()
    exp[-1].dlc_plot()
    plt.title(exp_title, fontsize = 10)
    plt.savefig(path + exp_path + '_DLC.png', dpi=600)
    
    """for Huber Regression"""
    # X = exp[-1].X
    # _X = X.reshape(-1, 1)
    # Y = exp[-1].Y
    # huber = HuberRegressor(alpha=0.0, epsilon=1.35)
    # huber.fit(_X, Y)
    # coef_ = huber.coef_ * X + huber.intercept_
    # Huber_result = huber.coef_[0]*1000000/3
    
    # plt.plot(X, coef_, 'tab:pink', linewidth = 0.5, label="Huber: {0}".format(int(Huber_result)) + r' $\mu$F/cm')    
    # plt.legend() 
    
    return dlc_df

# old version
# def get_specific(name, num = -1):
#     if name[:num].endswith('_'):
#         condition = name[:num-1] + '.mpl'
#         return condition    
#     else:
#         return get_specific(name, num-1)

def get_specific(name, num = -1):
    temp = os.path.splitext(name)
    if temp[0][:num].endswith('_'):
        condition = temp[0][:num-1] + '.mpl'
        return condition
    else:
        return get_test(name, num-1)
    

def get_export(path, exp, dlc_df, exp_path):
    with pd.ExcelWriter(path + exp_path +'_DLC.xlsx') as writer:
        for i in range(len(exp_data)):
            exp[i].df.to_excel(writer, sheet_name = 'CV', startcol = 2*i, index=False )
        dlc_df.to_excel(writer, sheet_name = 'DLC')

def main(date_path = year_path):
    file_list, path_dir, exp_path, exp_title = fileloads(date_path, '.txt')
    # condition_list = specific(get_specific, file_list)
    condition_list = [get_specific(_) for _ in file_list]
    # condition_test = [get_test(_) for _ in file_list]
    
    exp_dict = {}
    for index, i in enumerate(file_list):
        exp_dict[i]  = condition_list[index]    
    CVs = []
    GCDs= []
    for i in exp_dict:
        try:
            test_file = os.path.join(path_dir, exp_dict[i])
            with open(test_file, 'r') as f:
                # f = open(test_file, 'r')
                lines = f.readlines()
                method = lines[2]
                if method == 'Cyclic Voltammetry\n':
                    CVs.append(i)
                elif method == 'Constant Current\n':
                    GCDs.append(i)
                # f.close()
        except FileNotFoundError:
            pass
    exp_data = build_data(path_dir, CVs, DLC_builder)
    get_CVplot(path_dir, exp_data, exp_path, exp_title, exp_dict)
    dlc_df = get_DLCplot(path_dir, exp_data, exp_path, exp_title)
    
    
    print('\nDone!')
    get_export(path_dir, exp_data, dlc_df, exp_path)

if __name__ == "__main__":
    main()