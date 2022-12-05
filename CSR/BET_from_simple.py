# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:36:29 2022

@author: user
"""
from loadexp import *
import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
import pygaps as pg
import pygaps.parsing as pgp
import pprint
import pygaps.characterisation as pgc
from pygaps.graphing.calc_graphs import psd_plot


plt.style.use(['science', 'no-latex'])
year_path = "D:\\Researcher\\JYCheon\\DATA\\BET"

class N2_sorption(Dataloads):
    isotherms = []
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        # self.iso = pgp.isotherm_from_commercial(self.file_path, "bel", "csv")
        self.df = pd.read_csv(self.file_path)
        pressure, loading  = self.df.columns
        
        self.iso = pg.PointIsotherm(
            pressure = self.df[pressure]
            , loading = self.df[loading]/647
            , pressure_mode = "relative"
            , m = "carbon"
            , t = 77
            , a = "nitrogen"
            , pressure_unit = None
            , loading_basis ="volume_liquid"
            , loading_unit = "cm3"
            , material_basis = "mass"
            , material_unit = "g"
            , temperature_unit = "K"


            )
        
        
        # self.iso = pgp.csv.isotherm_from_csv(self.file_path)
        # self.iso.convert_pressure(mode_to = 'relative')

        
    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def get_BET(self):
        print('-------------------------------------------------------------------------------------------')
        print("BET analysis result for: ", self.file)
        print('-------------------------------------------------------------------------------------------')
        lastidx = self.iso.data(branch = "ads").shape[0]- 1
        self.TPV = self.iso.data(branch = "ads")["loading"].loc[lastidx]
        print("Total pore volume is: {0} cm\u00b3/g".format(round(self.TPV, 2) ) )
        self.result = pgc.area_BET(self.iso, verbose=True)
        print('-------------------------------------------------------------------------------------------')
        plt.show()
        self.SSA= self.result["area"]
        # self.TPV = self.iso.data(branch = "ads")["loading"].loc[lastidx]/647       
        self.ads_X = self.iso.data(branch = "ads")["pressure"] 
        self.ads_Y = self.iso.data(branch = "ads")["loading"]
        self.des_X = self.iso.data(branch = "des")["pressure"] 
        self.des_Y = self.iso.data(branch = "des")["loading"]
           
        N2_sorption.isotherms.append([self.ads_X, self.ads_Y, self.des_X, self.des_Y])
        
        self.df_ads = self.iso.data(branch = "ads")[["pressure", "loading"]].reset_index(drop = True)
        self.df_des = self.iso.data(branch = "des")[["pressure", "loading"]].reset_index(drop = True)
        self.output_df =  pd.concat([self.df_ads, self.df_des], axis = 1, ignore_index = True)
        self.output_df.columns = ["ads", "Va/cm3(STP)g-1", "des", self.name]
     
#         # return (self.SSA, self.TPV)
    def get_name(self):
        return self.name
        
        
    def get_plot(self):
        
        marker = "s" # 's' mean squuare
        line = "-" # '-' mean solid line
        color = 'dimgray'
        markersize = 4
        
        plt.plot(self.ads_X, self.ads_Y, marker+line, color = color, markersize = markersize, label = "Total pore volume: " + str(round(self.TPV, 2)) + " cm$^3$/g")
        plt.plot(self.des_X, self.des_Y, marker+line, markerfacecolor = 'white', markeredgewidth = 0.5, markeredgecolor = color, markersize = markersize, color = color, label = "BET SSA: " + str(int(self.SSA)) + " m$^2$/g", zorder = 10)
        plt.title(self.name, fontsize = 9)
        plt.xlabel("$P/P_{0}$")
        plt.ylabel("$V_{a}$/cm$^3$$_{(STP)}$g$^{-1}$")
        plt.legend(fontsize = 8)
        self.output = self.path + 'export\\'
        try:
            os.mkdir(self.output)    
        except FileExistsError:
            pass        
        plt.savefig(self.output + self.name + ".png", dpi = 600)
        plt.show()
             
        
def plot(exp):

    for i in range(len(exp)):
        exp[i].get_BET()
        exp[i].get_plot() 
        

def get_export(exp, path):
    output = path + 'export\\'
    
    try:
        os.mkdir(output)    
    except FileExistsError:
        pass        
    for i in range(len(exp)):
        
        df3 = pd.DataFrame({"BET surface area" : [exp[i].SSA], "Total pore volume" : [exp[i].TPV]})        
        df = pd.concat([exp[i].output_df, df3], axis = 1, ignore_index= True)
        df.columns = ["p/p0", "Va/cm3(STP)g-1", "p/p0", "Va/cm3(STP)g-1", "BET SSA (m2/g)", "Total Pore Volume (cm3/g)"]
        try:
            with pd.ExcelWriter(output + exp[i].get_name() + '_corrected.xlsx') as writer:
                df.to_excel(writer, sheet_name = 'corrected')
        except PermissionError:
            pass
        

def get_multiplot(exp):
    isotherm_list = exp[-1].isotherms
    color_list = ['k', 'r', 'tab:orange', 'g', 'b', 'purple', 'c', 'm', 'k', 'r', 'tab:orange', 'g', 'b', 'purple']
    marker = "s" # 's' mean squuare
    line = "-" # '-' mean solid line
    # color = "dimgray"
    markersize = 4
 
    n = len(exp)
    # tot_df = pd.DataFrame()
    
    idx_list = []
    BET_list = []
    TPV_list = []
    
    for i in range(n):
        idx_list.append(exp[i].name)
        BET_list.append(exp[i].SSA)
        TPV_list.append(exp[i].TPV)
        
    d = {"BET SSA (m2/g)" : BET_list, "Total Pore Volume (cm3/g)" : TPV_list}
    df = pd.DataFrame(data = d, index = idx_list)    
    
    with pd.ExcelWriter(exp[-1].output + "Total.xlsx") as writer:
        for i in range(n):
            color = color_list[i%n]
            plt.plot(isotherm_list[i][0], isotherm_list[i][1], marker+line, color = color, markersize = markersize, label = exp[i].__str__())
            plt.plot(isotherm_list[i][2], isotherm_list[i][3], marker+line, markerfacecolor = 'white', markeredgewidth= 0.5, markeredgecolor = color, color = color, markersize = markersize, zorder = 10) 
        
            exp[i].output_df.to_excel(writer, startcol = 4*i, index = False)
            df.to_excel(writer, sheet_name = 'Summary')
            

    plt.xlabel("$P/P_{0}$")
    plt.ylabel("$V_{a}$/cm$^3$$_{(STP)}$g$^{-1}$")
    leg = plt.legend(fontsize = 8)
    for line, text in zip(leg.get_lines(), leg.get_texts()):
        text.set_color(line.get_color())
        
    plt.savefig(exp[-1].output +"Total.png", dpi = 600)
     


def main(date_path = year_path):

    raw_list, path, _, _ = fileloads(date_path, '.csv')
    exp = build_data(path, raw_list, N2_sorption)
    
    for ex in exp:
        ex.get_BET()
        
        
if __name__ == "__main__":
    main(year_path)
    
    # plot(exp)
    # get_export(exp, path)
    
    # output_path = path + "\\export"
    # output_list = [_ for _ in os.listdir(output_path) if _.endswith(".xlsx")]
    
    # print(output_list)
    # # isotherm_dfs = build_data(output_path, output_list, N2_Multi)
    # get_multiplot(exp)
    
# if __name__ == "__main__":
#     main()
    
    
# get_multiBET(isotherm_dfs, output_path)
# print(isotherm_dfs[0].df)



# test = build_data(path, raw_list, N2_Multi)

# result_dict_micro = pgc.psd_microporous(exp[0].iso, psd_model = 'HK', verbose = True)
# result_dict_meso = pgc.psd_mesoporous(exp[0].iso, pore_geometry = 'cylinder', verbose = True)
# result_dict_dft = pgc.psd_dft(exp[0].iso, 
#                               branch = 'ads', 
#             kernel ='DFT-N2-77K-carbon-slit',
#             verbose=True,
#             p_limits=None)

# result_dict_dft = pgc.psd_dft(
#     exp[0].iso,
#     bspline_order=5,
#     verbose=True,
# )



# ax = psd_plot(
#     result_dict_dft['pore_widths'],
#     result_dict_dft['pore_distribution'],
#     method='comparison',
#     labeldiff='DFT',
#     labelcum=None,
#     left=0.4,
#     right=8
# )
# ax.plot(
#     result_dict_micro['pore_widths'],
#     result_dict_micro['pore_distribution'],
#     label='microporous',
# )
# ax.plot(
#     result_dict_meso['pore_widths'],
#     result_dict_meso['pore_distribution'],
#     label='mesoporous',
# )
# ax.legend(loc='best')