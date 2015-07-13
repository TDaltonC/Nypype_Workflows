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
#import errno
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
    
    trialbytrial['linearValue']= trialbytrial['valueOption']
    trialbytrial['linearDiff'] = trialbytrial['valueDiff']
    
    trialbytrial['numItmOnScrn'] = vpf.num_itm_on_screen_Vec(trialbytrial['trialType'])
    trialbytrial['AverageValue'] = trialbytrial['linearValue']/trialbytrial['numItmOnScrn']
    trialbytrial['AverageDiff'] = trialbytrial['linearDiff']/trialbytrial['numItmOnScrn']

#   Fliter down to multi-run event files  
    valueTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    difficultyTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    controlTrials = trialbytrial[(trialbytrial.trialType  == 2)|(trialbytrial.trialType  == 3)]
    scalingTrials = trialbytrial[(trialbytrial.trialType  == 4)|(trialbytrial.trialType  == 5)|(trialbytrial.trialType  == 6)]
    bundlingTrials = trialbytrial[(trialbytrial.trialType  == 7)|(trialbytrial.trialType  == 8)|(trialbytrial.trialType  == 9)]
    print subjectID        
#   Make a plot of the distribution of value and value-diff across the three condictions and save them.         
#    vpf.savePlotDisributionsByTT(trialbytrial,"linearValue",'EVfiles/'+subjectID)
#    vpf.savePlotDisributionsByTT(trialbytrial,"linearDiff",'EVfiles/'+subjectID)
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        # valueSingleRun = valueTrials[(valueTrials.run  == run)]
        # difficultySingleRun = difficultyTrials[(difficultyTrials.run  == run)]
        controlSingleRun = controlTrials[(controlTrials.run  == run)]
        scalingSingleRun = scalingTrials[(scalingTrials.run  == run)]
        bundlingSingleRun = bundlingTrials[(bundlingTrials.run  == run)] 
 #      Cut down to only 3 columns
        control3Col     = controlSingleRun[['tResponse','ones']]
        scaling3Col     = scalingSingleRun[['tResponse','ones']]
        bundling3Col    = bundlingSingleRun[['tResponse','ones']]
        valueC3Col      = controlSingleRun[['tResponse','AverageValue']]
        difficultyC3Col = controlSingleRun[['tResponse','AverageDiff']]
        valueS3Col      = scalingSingleRun[['tResponse','AverageValue']]
        difficultyS3Col = scalingSingleRun[['tResponse','AverageDiff']]
        valueB3Col      = bundlingSingleRun[['tResponse','AverageValue']]
        difficultyB3Col = bundlingSingleRun[['tResponse','AverageDiff']]
#       Name and open the destinations for event files
        controlDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        scalingDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Scaling.run00'+ str(run) +'.txt'))
        bundlingDir    = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Bundling.run00'+ str(run) +'.txt'))
        valueCDir       = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ValueC.run00'+ str(run) +'.txt'))
        difficultyCDir  = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/DifficultyC.run00'+ str(run) +'.txt'))
        valueSDir       = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ValueS.run00'+ str(run) +'.txt'))
        difficultySDir  = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/DifficultyS.run00'+ str(run) +'.txt'))
        valueBDir       = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ValueB.run00'+ str(run) +'.txt'))
        difficultyBDir  = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/DifficultyB.run00'+ str(run) +'.txt'))

#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        bundling3Col.to_csv(bundlingDir, sep ='\t', header = False)
        valueC3Col.to_csv(valueCDir, sep ='\t', header = False)
        difficultyC3Col.to_csv(difficultyCDir, sep ='\t', header = False)
        valueS3Col.to_csv(valueSDir, sep ='\t', header = False)
        difficultyC3Col.to_csv(difficultySDir, sep ='\t', header = False)
        valueB3Col.to_csv(valueBDir, sep ='\t', header = False)
        difficultyB3Col.to_csv(difficultyBDir, sep ='\t', header = False)
#        Be Tidy! Close all of those open files! 
        controlDir.close()
        scalingDir.close()
        bundlingDir.close()
        valueCDir.close()
        difficultyCDir.close()
        valueSDir.close()
        difficultySDir.close()
        valueBDir.close()
        difficultyBDir.close()