# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:34:05 2022

@author: kkourkoulou

Calculation of histogram of encapsulated septin concentrations. 
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd           
import seaborn as sns

#------------------------- INPUT --------------------------------

## Determine proportionality constant from aclibration_curve.py output and the 
## nominal encapsulated concentration (nM):
    
A         = 0.00185182
c_nominal = 800

## Determine path to files from manual_filtering.py output:
    
path_data = "D:\\Personal\\TU Delft\\Thesis\\23_03_March\\Encapsulation efficiency\\Analysis\\Output\\"

## Specify number of regions collected and the corresponding file names:
num_regions = 7

DOPC_Region_8_csv   = path_data + "DOPC-Region 8-Output.csv"    
DOPC_Region_9_csv   = path_data + "DOPC-Region 9-Output.csv" 
DOPC_Region_10_csv  = path_data + "DOPC-Region 10-Output.csv" 
DOPC_Region_11_csv  = path_data + "DOPC-Region 11-Output.csv"    
DOPC_Region_12_csv  = path_data + "DOPC-Region 12-Output.csv" 
DOPC_Region_13_csv  = path_data + "DOPC-Region 13-Output.csv" 
DOPC_Region_14_csv  = path_data + "DOPC-Region 14-Output.csv"     
 
## Reading of files:
    
detected_vesicles_1  = pd.read_csv(DOPC_Region_8_csv)
data_1 = pd.DataFrame(detected_vesicles_1).to_numpy()

detected_vesicles_2  = pd.read_csv(DOPC_Region_9_csv)
data_2 = pd.DataFrame(detected_vesicles_2).to_numpy()

detected_vesicles_3  = pd.read_csv(DOPC_Region_10_csv)
data_3 = pd.DataFrame(detected_vesicles_3).to_numpy()

detected_vesicles_4  = pd.read_csv(DOPC_Region_11_csv)
data_4 = pd.DataFrame(detected_vesicles_3).to_numpy()

detected_vesicles_5  = pd.read_csv(DOPC_Region_12_csv)
data_5 = pd.DataFrame(detected_vesicles_3).to_numpy()

detected_vesicles_6  = pd.read_csv(DOPC_Region_13_csv)
data_6 = pd.DataFrame(detected_vesicles_3).to_numpy()

detected_vesicles_7  = pd.read_csv(DOPC_Region_14_csv)
data_7 = pd.DataFrame(detected_vesicles_3).to_numpy()

#----------------------------------------------------------------

#--------------------------- MAIN -------------------------------

## Rearrangment of data:
    
data = data_1[:,5]
data = np.append(data, data_2[:,5])
data = np.append(data, data_3[:,5])
data = np.append(data, data_4[:,5])
data = np.append(data, data_5[:,5])
data = np.append(data, data_6[:,5])
data = np.append(data, data_7[:,5])

## Conversion to concentrations and normalization by the nominal encapsulated 
## concentration :

data = data / (A * c_nominal)


## Plotting of resulting histogram:
    
plt.figure(figsize =(8, 6), dpi= 150)
plt.title("Histogram of Encapsulation Efficiency")
sns.set(font_scale=1.5)
sns.set_style(style='white') 
sns.histplot(data , color="darkmagenta", bins=20, edgecolor="white" ,kde=True, line_kws={'label': "KDE fit"})#, **kwargs)
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
plt.xlabel("$c_{enc}/c_{nominal}$", fontsize=18)
plt.axvline(x = 1, color = 'black', linestyle="dashed",label="$c_{enc}$=$c_{nominal}$")
plt.legend()
ax = sns.histplot(data, bins=20, kde=True, alpha= 0.1, color='darkmagenta')
kdeline = ax.lines[0]
xs = kdeline.get_xdata()
ys = kdeline.get_ydata()
mode_idx = np.argmax(ys)






