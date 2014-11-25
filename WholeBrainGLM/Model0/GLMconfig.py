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
cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['Scaling','T', ['Scaling'],[1]]
cont4 = ['Bundling','T', ['Bundling'],[1]]
cont5 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont6 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont7 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont8 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont9 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
contrasts = [cont0,cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8,cont9]

# ROI Masks
ROI_Masks = [os.path.abspath('../ROIs/HOMiddleFrontalGyrus.nii.gz'),
            os.path.abspath('../ROIs/lAG.nii.gz'),
            os.path.abspath('../ROIs/lIPS.nii.gz'),
            os.path.abspath('../ROIs/rIPS.nii.gz'),
            os.path.abspath('../ROIs/rLingual.nii.gz'),
            os.path.abspath('../ROIs/ACC.nii.gz'),
            os.path.abspath('../ROIs/lIFG.nii.gz'),
            os.path.abspath('../ROIs/lpITG.nii.gz'),
            os.path.abspath('../ROIs/lSFG1.nii.gz'),
            os.path.abspath('../ROIs/lSFG2.nii.gz'),
            os.path.abspath('../ROIs/mOFC.nii.gz'),
            os.path.abspath('../ROIs/Perc.nii.gz'),
            os.path.abspath('../ROIs/rIFG.nii.gz'),
            os.path.abspath('../ROIs/rPCG.nii.gz'),
            os.path.abspath('../ROIs/rpITG.nii.gz'),
            os.path.abspath('../ROIs/rSFG.nii.gz'),
            os.path.abspath('../ROIs/vmPFC.nii.gz')]


