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

# Wthere the input data comes from
data_dir =                os.path.abspath('../../../RawData')
# Where the outputs goes
withinSubjectResults_dir =os.path.abspath('../FFX_Results')
betweenSubjectResults_dir=os.path.abspath('../MFX_Results')
# Working Directory
workingdir =              os.path.abspath('../WorkingDir/')
# Crash Records
crashRecordsDir =         os.path.abspath('../WorkingDir/crashdumps')

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
cont1 = ['Control','T', ['Control'],[1]]
cont2 = ['Value','T', ['Value'],[1]]
cont3 = ['Difficulty','T', ['Difficulty'],[1]]
cont4 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont5 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont6 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont7 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont8 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[1,1,-1]]
contrasts = [cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8]

