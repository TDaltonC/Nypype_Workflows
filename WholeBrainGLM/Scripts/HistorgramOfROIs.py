# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:54:48 2014

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns

ROIs = []


# Add all of the ROIs you want to plot to the ROIs list
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_5/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lAG.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_5/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lIPS.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_5/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rIPS.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_5/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rLingual.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz'))

#ROIs = [
#        lAG,
#        lIPS,
#        rIPS,
#        rLingual
#        ]

for ROI in ROIs:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
        
    
    sns.kdeplot(nonZeros)