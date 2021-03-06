# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:06:38 2014

@author: Dalton
"""

"""
=========
Imports
=========
"""
import os                                    # system functions

import nipype.interfaces.fsl as fsl          # fsl


# These two lines enable debug mode
#from nipype import config
#config.enable_debug_mode()

"""
==============
Configurations
==============
"""
#set output file format to compressed NIFTI.
fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

def configPaths(modelName):
    
    # Wthere the input data comes from
    data_dir =                os.path.abspath('../../../')
    ev_dir   =                os.path.abspath('../' + modelName + '/')
    # Where the outputs goes
    withinSubjectResults_dir =os.path.abspath('../' + modelName + '/FFX_Results')
    betweenSubjectResults_dir=os.path.abspath('../' + modelName + '/MFX_Results')
    # Working Directory
    workingdir =              os.path.abspath('../' + modelName + '/WorkingDir/')
    # Crash Records
    crashRecordsDir =         os.path.abspath('../' + modelName + '/WorkingDir/crashdumps')
    return data_dir, ev_dir, withinSubjectResults_dir, betweenSubjectResults_dir, workingdir,crashRecordsDir

# Templates
mfxTemplateBrain        = '/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz'
strippedmfxTemplateBrain= '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz'
mniConfig               = '/usr/local/fsl/etc/flirtsch/T1_2_MNI152_2mm.cnf'
mniMask                 = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'


# subject directories
subject_list = ['SID702','SID703','SID705','SID706','SID707','SID708','SID709','SID710'] 

#List of functional scans
func_scan= [1,2,3,4,5]

#ModelSettings
input_units = 'secs'
hpcutoff = 120
TR = 2.

# Contrasts
cont0 = ['TaskPos','T', ['TaskPos'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['ItmCount','T', ['ItmCount'],[1]]
contrasts = [cont0,cont1,cont2,cont3]

# ROI Masks
ROI_Masks = [os.path.abspath('../ROIs/HOMiddleFrontalGyrus.nii.gz'),
        os.path.abspath('../ROIs/lAG.nii.gz'),
        os.path.abspath('../ROIs/lIPS.nii.gz'),
        os.path.abspath('../ROIs/rIPS.nii.gz'),
        os.path.abspath('../ROIs/rLingual.nii.gz')]