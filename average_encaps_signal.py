# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:08:05 2022

@author: kkourkoulou

Calculation of average intensity within defined ROI.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap    
import pandas as pd           
import cv2
import csv
from skimage.draw import disk

## Defining commonly used color map:
colors          = ["black","magenta", "magenta"]
nodes           = [0.0, 0.05, 1.0]
cmap_magenta_enhanced = LinearSegmentedColormap.from_list("cmap_magenta_enhanced", list(zip(nodes, colors)))

## Determine path to images and DisGUVery files and path for the output:
path_to_folder = "D:\\Personal\\TU Delft\\Thesis\\23_03_March\\Encapsulation efficiency\\Analysis\\"
path_to_output = path_to_folder + "\\Output"

#------------------------- INPUT --------------------------------

## Define circular ROI radius in vesicle radius units:
    
roi_radius  = 0.9

## Determine file names:
    
## csv
DOPC_Region_8_csv   = "20230306-DOPC-Region 8_Merged_RAW_ch00_detected_vesicles.csv"    
DOPC_Region_9_csv   = "20230306-DOPC-Region 9_Merged_RAW_ch00_detected_vesicles.csv" 
DOPC_Region_10_csv  = "20230306-DOPC-Region 10_Merged_RAW_ch00_detected_vesicles.csv" 
DOPC_Region_11_csv  = "20230306-DOPC-Region 11_Merged_RAW_ch00_detected_vesicles.csv"    
DOPC_Region_12_csv  = "20230306-DOPC-Region 12_Merged_RAW_ch00_detected_vesicles.csv" 
DOPC_Region_13_csv  = "20230306-DOPC-Region 13_Merged_RAW_ch00_detected_vesicles.csv" 
DOPC_Region_14_csv  = "20230306-DOPC-Region 14_Merged_RAW_ch00_detected_vesicles.csv"     

## tiff
DOPC_Region_8_tif   = "20230306-DOPC-Region 8_Merged_RAW_ch00.tif"    
DOPC_Region_9_tif   = "20230306-DOPC-Region 9_Merged_RAW_ch00.tif"
DOPC_Region_10_tif  = "20230306-DOPC-Region 10_Merged_RAW_ch00.tif"
DOPC_Region_11_tif  = "20230306-DOPC-Region 11_Merged_RAW_ch00.tif"
DOPC_Region_12_tif  = "20230306-DOPC-Region 12_Merged_RAW_ch00.tif"
DOPC_Region_13_tif  = "20230306-DOPC-Region 13_Merged_RAW_ch00.tif"
DOPC_Region_14_tif  = "20230306-DOPC-Region 14_Merged_RAW_ch00.tif"

## specific output folder:
DOPC_Region_8_folder = "\\DOPC-Region 8"
DOPC_Region_9_folder = "\\DOPC-Region 9"
DOPC_Region_10_folder = "\\DOPC-Region 10"
DOPC_Region_11_folder = "\\DOPC-Region 11"
DOPC_Region_12_folder = "\\DOPC-Region 12"
DOPC_Region_13_folder = "\\DOPC-Region 13"
DOPC_Region_14_folder = "\\DOPC-Region 14"

## Set current run:

Current_Region_csv    = path_to_folder + DOPC_Region_8_csv
Current_Region_tif    = path_to_folder + DOPC_Region_8_tif
Current_Region_folder = DOPC_Region_8_folder

## Paths to specific output folders:
    
path_to_image_output = path_to_folder + "\\Output" + Current_Region_folder

## Reading files:

detected_vesicles  = pd.read_csv(Current_Region_csv)
coordinates = pd.DataFrame(detected_vesicles).to_numpy()

septin_signal = plt.imread(Current_Region_tif)
#----------------------------------------------------------------

#------------------------ PREPARATION ---------------------------

## Useful parameters:
    
num_vesicles   = len(coordinates[:,0])
image_dim_x    = len(septin_signal[0,:])
image_dim_y    = len(septin_signal[:,0])
image_dim      = [image_dim_x,image_dim_y]


## Creating output file:
column_headers = ["Image", "Vesicle id", "xc", "yc", "Radius", "Average signal", "Num. of pixels"]

with open(path_to_image_output + "\\" + "Output.csv", "w", newline='') as output_file:
    df = csv.DictWriter(output_file, delimiter=',', fieldnames = column_headers)
    df.writeheader()

#----------------------------------------------------------------

#--------------------------- MAIN -------------------------------

## Plotting image to be analyzed:
    
plt.figure(dpi=150)
plt.title('Total number of detected vesicles: ' + str(num_vesicles))    
plt.axis('off')
plt.imshow(septin_signal, cmap=cmap_magenta_enhanced )
 
plt.savefig(path_to_image_output + "\\" + "Overview.png")


for i in range(num_vesicles):
    
    ## Vesicle parameters:
        
    vesicle_id = coordinates[i,0]
    xc         = int(coordinates[i,1])
    yc         = int(coordinates[i,2])
    radius     = int(coordinates[i,3])
    
    ## Create zoom-in image:  
    vesicle_box_side = int(radius)
    
    move_right = 0
    move_left  = 0
    move_up    = 0
    move_down  = 0
    
    ## Recentering of box if vesicle exceeds image borders:
    if xc - vesicle_box_side < 0: 
        move_right = vesicle_box_side - xc
                  
    if xc + vesicle_box_side > image_dim[0]: 
        move_left  = vesicle_box_side - (image_dim[0]-xc)   
        
    if yc - vesicle_box_side < 0: 
        move_down  = vesicle_box_side - yc           
                      
    if yc + vesicle_box_side > image_dim[1]: 
        move_up    = vesicle_box_side - (image_dim[1]-yc)   
         
    vesicle_box = septin_signal[int(yc - vesicle_box_side + move_down - move_up):int(yc + vesicle_box_side + move_down - move_up), int(xc - vesicle_box_side + move_right - move_left):int(xc + vesicle_box_side - move_left + move_right)]
    
    
    ## Create circular mask corresponding to the ROI of interest:
        
    mask = np.zeros((2*vesicle_box_side, 2*vesicle_box_side), dtype=np.uint8)
    
    rr, cc = disk((vesicle_box_side, vesicle_box_side), roi_radius*radius)
    mask[rr, cc] = 1
    
    ## Calculate average signal within the ROI:
    
    num_pixels     = np.count_nonzero(np.logical_not(mask))
    average_signal = np.average(np.ma.array(vesicle_box, mask=np.logical_not(mask)))  
    
    ## Display ROI:
        
    roi = vesicle_box    
    roi = cv2.circle(roi, (vesicle_box_side,vesicle_box_side), int(roi_radius*radius), color=(255,0,255), thickness = 1)
    
    plt.figure(dpi=150)
    plt.title('Vesicle ' + str(int(vesicle_id)) + " - Selected ROI: # of pixels = " + str(num_pixels))  
    plt.axis('off')
    plt.imshow(roi, cmap=cmap_magenta_enhanced )
    
    plt.savefig(path_to_image_output+"\\" + "Vesicle_" + str(int(vesicle_id)) + "-ROI.png")
    
    ## Save vesicle info in output file:
    
    list_name            = list([Current_Region_tif])
    list_ves_coordinates = list(coordinates[i,:])
    list_signal          = list([average_signal])
    list_pixels          = list([num_pixels])
    
    vesicle_row = list_name +  list_ves_coordinates + list_signal + list_pixels
    
    with open(path_to_image_output+"\\" + "Output.csv", "a", newline='') as output_file:
               
        writer = csv.writer(output_file)
        writer.writerow(vesicle_row)