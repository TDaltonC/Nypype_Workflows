# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 13:33:04 2014

@author: Dalton
"""

import os                                    # Operating system Functions
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.io as nio           # Data i/o

from nipype import config
config.enable_debug_mode()


TemplateBrain = '/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz'
ROIDir        = os.path.abspath('../' + 'ROIs')
workingdir =    os.path.abspath('../' + 'ROIs' + '/WorkingDir/')

ROIs = ['-add 1 -roi 45 1 74 1 51 1 0 1 ROI1',
        '-add 1 -roi 45 1 23 1 51 1 0 1 ROIBETA']


'''
#########
##Nodes##
#########
'''
sphericalROI = pe.Workflow(name = 'sphericalROI',
                           base_dir = workingdir)

#Zero the standard brain
zeroing = pe.Node(interface=fsl.BinaryMaths(in_file = TemplateBrain,
                                            operation = 'mul',
                                            operand_value = 0),
                       name='zeroing')
                       
                       
# Node for creating a point at the center of the ROI
addPoint = pe.Node(interface=fsl.maths.MathsCommand(# Find a way to RegEx this
#                                                    args = '-add 1 -roi 45 1 74 1 51 1 0 1'
                                                    ),
                       iterables = ('args',ROIs),
                       name='addPoint')

# node for expanding the point
dilatePoint = pe.Node(interface=fsl.DilateImage(operation = 'mean',
                                                kernel_shape = 'sphere',
                                                kernel_size = 5),
                       name='dilatePoint')
                       
#DataSink  --- stores important outputs
dataSink = pe.Node(interface=nio.DataSink(base_directory= ROIDir,
                                          parameterization = True # This line keeps the DataSink from adding an aditional level to the directory, I have no Idea why this works.
                                          
                                          ),
                   name="dataSink")
                       
                       
'''
###############
##Connections##
###############
'''


sphericalROI.connect([(zeroing, addPoint,[('out_file','in_file')]),
                      (addPoint, dilatePoint,[('out_file','in_file')]),
                      (dilatePoint,dataSink,[('out_file','ROI')]),
                      ])

sphericalROI.run()