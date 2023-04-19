
Quantification of septin encapsulation efficiency in GUVs (eDICE)
-----------------------------------------------------------------------------------


This Python scripts quantify the encapsulated septin concentration in GUVs prepared 
with eDICE. 


Files
-----------------------------------------------------------------------------------

- calibration_curve.py    :   Calculation of the calibration curve for conversion from
			   intensity values to concentrations using points from septin
			   bulk solutions. Output proportionality constant A should be
			   used in histogram_encaps_eff.py  
		     
- average_encaps_signal.py:   Calculation of the avergage intensity (a.u.) of the septin
			   inside a circular ROI concentric to the detected GUVs. GUV
			   detection should be carried first in DisGUVery.  
		     	       
- manual_filtering.py     :   Script that allows manual filtering of detected vesicles 
             		   corresponding to misaligned detection or in case of the 
			   presence of septin aggregates. The output files of 
			   average_encaps_signal.py should be used as input.  

- histogram_encaps_eff.py :    Conversion of intensity values to encapsulated septin 
			   concentrations. Uses A calculated in calibration_curve.py
			   and output files of manual_filtering.py as input. 
			   
