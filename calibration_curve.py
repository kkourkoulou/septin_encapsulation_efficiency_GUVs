# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:58:05 2022

@author: kkourkoulou

Calculation of calibration curve for conversion of intensity values to 
septin concentration. 
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd           
import seaborn as sns


#------------------------- INPUT --------------------------------

### Septin bulk solutions:
    
## Concentrations of septin bulk solutions prepared:
concentrations = np.array((0, 200, 400, 600, 800, 1000))

## Average of intesity (a.u.) of all regions calculated in Fiji (5 regions for each concentration):
bulk_0    = np.array((0.011, 0.011, 0.011, 0.01, 0.011))
bulk_200  = np.array((0.106, 0.101, 0.113, 0.099, 0.127))
bulk_400  = np.array((0.584, 0.624, 0.6, 0.667, 0.629))
bulk_600  = np.array((1.002, 0.983, 1.063, 0.995, 0.977))
bulk_800  = np.array((1.886, 1.74, 1.83, 1.647, 1.811))
bulk_1000 = np.array((1.706, 1.859, 1.791, 1.727, 1.793))

#----------------------------------------------------------------

#--------------------------- MAIN -------------------------------

## Rearrangment of data:
bulk      = np.array((bulk_0, bulk_200, bulk_400, bulk_600, bulk_800, bulk_1000))

## Calculation of calibration curve points:
bulk_average = np.average(bulk, axis = 1)
bulk_stddev  = np.std(bulk, axis = 1)

## Least squares fit:
x = concentrations[:,np.newaxis]
y = bulk_average
A = np.linalg.lstsq(x, y, rcond=None)[0]

## Calibration curve: 
plt.figure(figsize =(8, 6),dpi=125)
plt.title('Calibration curve')
plt.xlabel("\n $c_{nominal}$ in bulk solutions (nM)")
plt.ylabel("mean intensity (a.u.)\n")
plt.errorbar(x, y, bulk_stddev, linestyle='None', marker='o', color='darkmagenta', markersize=10)
plt.plot(x, A*x, 'black',linestyle='dashed')#, label='I$_{sept}$=A$\cdot$ c$_{sept}$, A= ' + str(round(A[0],8)))
# plt.legend(fontsize=15)
plt.show()


