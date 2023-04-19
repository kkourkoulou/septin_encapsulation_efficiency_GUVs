# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:21:05 2022

@author: kkourkoulou

Manual filtering of misplaced detections and vesicles with septin aggregates

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  
import csv

## Paths to folder with the data:
path_to_folder = "D:\\Personal\\TU Delft\\Thesis\\Encapsulation efficiency\\Analysis\\Output"

## specific output folders for each region:
DOPC_Region_8_folder = "\\DOPC-Region 8"
DOPC_Region_9_folder = "\\DOPC-Region 9"
DOPC_Region_10_folder = "\\DOPC-Region 10"
DOPC_Region_11_folder = "\\DOPC-Region 11"
DOPC_Region_12_folder = "\\DOPC-Region 12"
DOPC_Region_13_folder = "\\DOPC-Region 13"
DOPC_Region_14_folder = "\\DOPC-Region 14"


## Set current run:
current_choice = DOPC_Region_8_folder
current_images_folder = path_to_folder + "\\" + current_choice

#----------------------------------------------------------------

#------------------------ PREPARATION ---------------------------

data_file  = pd.read_csv(path_to_folder + current_choice + "-Output.csv")
data = pd.DataFrame(data_file).to_numpy()

## Create output file:

column_headers = ["Vesicle id", "Average signal", "Num. of pixels", "Comment"]

with open(current_images_folder + "\\" + "Deathmark.csv", "w", newline='') as output_file:
    df = csv.DictWriter(output_file, delimiter=',', fieldnames = column_headers)
    df.writeheader()

column_headers_final = ["Image", "Vesicle id", "xc", "yc", "Radius", "Average signal", "Num. of pixels"]

with open(current_images_folder + "\\" + current_choice + ".csv", "w", newline='') as output_file:
    df = csv.DictWriter(output_file, delimiter=',', fieldnames = column_headers_final)
    df.writeheader()
    
    
#----------------------------------------------------------------

#--------------------------- MAIN -------------------------------
    
num_vesicles = len(data[:,0])

## Initializing array to mark rejected detections:
death_mark = np.zeros(1, dtype=int)

for i in range(num_vesicles): 
    
    vesicle_image = plt.imread(current_images_folder + "\\Vesicle_" + str(int(i+1)) + "-ROI.png")
    
    plt.figure(dpi=150)   
    plt.axis('off')
    plt.imshow(vesicle_image)
    plt.show()
    
    mark = input("Ignore (i) or OK (o):")
    
    list_ves_id  = list([data[i,1]])
    list_signal  = list([data[i,5]])
    list_pixels  = list([data[i,5]])
    
    if mark == "o" :
        list_comment = ["o"]
    else:
        list_comment = ["i"]
    
    vesicle_row = list_ves_id + list_signal + list_pixels +list_comment
    
    with open(current_images_folder + "\\" + "Deathmark.csv", "a", newline='') as output_file:
                   
        writer = csv.writer(output_file)
        writer.writerow(vesicle_row)
        
    if mark == "o" :
        
        list_vesicle = list(data[i,:])
    
        with open(current_images_folder + "\\" + current_choice + ".csv", "a", newline='') as output_file:
        
            writer = csv.writer(output_file)
            writer.writerow(list_vesicle)
