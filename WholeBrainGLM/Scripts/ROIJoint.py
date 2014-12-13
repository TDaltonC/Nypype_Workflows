# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:54:48 2014

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns
import pandas as p
import scipy as sp

model = "Model_Complex6"
region= "HOMiddleFrontalGyrus"
cont1  = "con_2"
cont2  = "con_1"

ROI1 = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model +'/MFX_Results/ROIs/_'+ cont1 +'/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..'+ region +'.nii.gz/_ROIs0/zstat1_masked.nii.gz')
ROI2 = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model +'/MFX_Results/ROIs/_'+ cont2 +'/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..'+ region +'.nii.gz/_ROIs0/zstat1_masked.nii.gz')


ROIs = [
        ROI1,
        ROI2
        ]
        
names = [
        'Difficulty',
        'Value'
        ]

df = p.DataFrame(data = {'num':np.zeros(9696)})
i=0
for ROI in ROIs:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
    
    df[names[i]]=nonZeros
    i=i+1



sns.jointplot(df[names[0]],df[names[1]])

sp.stats.ttest_1samp(df['Scaling'],0)

# dlPFC Can I reduce the number of items?

# dlPFC do Value and Difference use difference sub-regions?

# How do we behavioraly measure value?

