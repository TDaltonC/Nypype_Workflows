# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 12:39:45 2014

@author: Dalton
"""

"""
=========
Imports
=========
"""
import os
import errno
import pandas
import numpy as np
#import seaborn as sb
import sys
sys.path.insert(0,  '/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Scripts')
import valuePilotFunctions as vpf

"""
=========
Functions
=========
"""

"""
==============
MEAT & POTATOS
==============
"""   
subjectList = ['SID702','SID703','SID705','SID706','SID707','SID708','SID709','SID710']

for subjectID in subjectList:
#   load the trial by trial data for this subject
    trialbytrial = pandas.DataFrame.from_csv(os.path.abspath('../../../RawData/'+ subjectID + '/MatLABOutput/trialByTrial.csv'))
    optionValue = pandas.DataFrame.from_csv(os.path.abspath('../../../RawData/'+ subjectID + '/dataFrames/DDMValue1.csv'))
#   Add a column of ones to the dataframe (this is usefull for creating the three column files)    
    trialbytrial['ones'] = 1

    trialbytrial['linearValue'] = optionValue['optionValue']
    trialbytrial['linearDiff'] = abs(trialbytrial['linearValue'])

    trialbytrial['numItmOnScrn'] = vpf.num_itm_on_screen_Vec(trialbytrial['trialType'])
#   Fliter down to multi-run event files  
    valueTrials = trialbytrial[(trialbytrial.valueOption  != 0)]
    difficultyTrials = trialbytrial[(trialbytrial.valueOption  != 0)]
    taskPosTrials = trialbytrial[(trialbytrial.valueOption  != 0)]
    itmCount = trialbytrial[(trialbytrial.numItmOnScrn  != 0)]
    print subjectID
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        valueSingleRun = valueTrials[(valueTrials.run  == run)]
        difficultySingleRun = difficultyTrials[(difficultyTrials.run  == run)]
        taskPosSingleRun = taskPosTrials[(taskPosTrials.run  == run)] 
        itmCountRun = itmCount[(itmCount.run  == run)]
 #      Cut down to only 3 columns
        value3Col = valueSingleRun[['tResponse','linearValue']]
        difficulty3Col = difficultySingleRun[['tResponse','linearDiff']]
        taskPos3Col = taskPosSingleRun[['tResponse','ones']]
        itmCount3Col = itmCountRun[['tResponse','numItmOnScrn']]
#       Name and open the destinations for event files
        valueDir       = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Value.run00'+ str(run) +'.txt'))
        difficultyDir  = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Difficulty.run00'+ str(run) +'.txt'))
        taskPosDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/TaskPos.run00'+ str(run) +'.txt'))
        itmCountDir    = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ItmCount.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        value3Col.to_csv(valueDir, sep ='\t', header = False)
        difficulty3Col.to_csv(difficultyDir, sep ='\t', header = False)
        taskPos3Col.to_csv(taskPosDir, sep ='\t', header = False)
        itmCount3Col.to_csv(itmCountDir, sep ='\t', header = False)     
#        Be Tidy! Close all of those open files! 
        valueDir.close()
        difficultyDir.close()
        taskPosDir.close()
        itmCountDir.close()

