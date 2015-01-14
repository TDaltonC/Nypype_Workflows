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
    valueTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    difficultyTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    controlTrials = trialbytrial[(trialbytrial.trialType  == 2)|(trialbytrial.trialType  == 3)]
    scalingTrials = trialbytrial[(trialbytrial.trialType  == 4)|(trialbytrial.trialType  == 5)|(trialbytrial.trialType  == 6)]
    bundlingTrials = trialbytrial[(trialbytrial.trialType  == 7)|(trialbytrial.trialType  == 8)|(trialbytrial.trialType  == 9)]
    sTwoItmTrials = scalingTrials[(scalingTrials.numItmOnScrn  == 2)]
    sThreeItmTrials = scalingTrials[(scalingTrials.numItmOnScrn  == 3)]
    sFourItmTrials = scalingTrials[(scalingTrials.numItmOnScrn  == 4)]
    bTwoItmTrials = bundlingTrials[(bundlingTrials.numItmOnScrn  == 2)]
    bThreeItmTrials = bundlingTrials[(bundlingTrials.numItmOnScrn  == 3)]
    bFourItmTrials = bundlingTrials[(bundlingTrials.numItmOnScrn  == 4)]
    print subjectID        
#   Make a plot of the distribution of value and value-diff across the three condictions and save them.         
    vpf.savePlotDisributionsByTT(trialbytrial,"linearValue",'EVfiles/'+subjectID)
    vpf.savePlotDisributionsByTT(trialbytrial,"linearDiff",'EVfiles/'+subjectID)
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        valueSingleRun = valueTrials[(valueTrials.run  == run)]
        difficultySingleRun = difficultyTrials[(difficultyTrials.run  == run)]
        controlSingleRun = controlTrials[(controlTrials.run  == run)] 
        sTwoItmSingeRun = sTwoItmTrials[(sTwoItmTrials.run  == run)]
        sThreeItmSingeRun = sThreeItmTrials[(sThreeItmTrials.run  == run)]
        sFourItmSingeRun = sFourItmTrials[(sFourItmTrials.run  == run)]
        bTwoItmSingeRun = bTwoItmTrials[(bTwoItmTrials.run  == run)]
        bThreeItmSingeRun = bThreeItmTrials[(bThreeItmTrials.run  == run)]
        bFourItmSingeRun = bFourItmTrials[(bFourItmTrials.run  == run)]
 #      Cut down to only 3 columns
        value3Col = valueSingleRun[['tResponse','linearValue']]
        difficulty3Col = difficultySingleRun[['tResponse','linearDiff']]
        control3Col = controlSingleRun[['tResponse','ones']]
        sTwoItm3Col = sTwoItmSingeRun[['tResponse','ones']]
        sThreeItm3Col = sThreeItmSingeRun[['tResponse','ones']]
        sFourItm3Col = sFourItmSingeRun[['tResponse','ones']]
        bTwoItm3Col = bTwoItmSingeRun[['tResponse','ones']]
        bThreeItm3Col = bThreeItmSingeRun[['tResponse','ones']]
        bFourItm3Col = bFourItmSingeRun[['tResponse','ones']]
#       Name and open the destinations for event files
        valueDir       = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Value.run00'+ str(run) +'.txt'))
        difficultyDir  = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Difficulty.run00'+ str(run) +'.txt'))
        controlDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        sTwoItmDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/sTwoItems.run00'+ str(run) +'.txt'))
        sThreeItmDir   = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/sThreeItems.run00'+ str(run) +'.txt'))
        sFourItmDir    = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/sFourItems.run00'+ str(run) +'.txt'))
        bTwoItmDir     = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/bTwoItems.run00'+ str(run) +'.txt'))
        bThreeItmDir   = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/bThreeItems.run00'+ str(run) +'.txt'))
        bFourItmDir    = vpf.safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/bFourItems.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        value3Col.to_csv(valueDir, sep ='\t', header = False)
        difficulty3Col.to_csv(difficultyDir, sep ='\t', header = False)
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        sTwoItm3Col.to_csv(sTwoItmDir, sep ='\t', header = False)
        sThreeItm3Col.to_csv(sThreeItmDir, sep ='\t', header = False)
        sFourItm3Col.to_csv(sFourItmDir, sep ='\t', header = False)
        bTwoItm3Col.to_csv(bTwoItmDir, sep ='\t', header = False)
        bThreeItm3Col.to_csv(bThreeItmDir, sep ='\t', header = False)
        bFourItm3Col.to_csv(bFourItmDir, sep ='\t', header = False)

#        Be Tidy! Close all of those open files! 
        valueDir.close()
        difficultyDir.close()
        controlDir.close()
        sTwoItmDir.close()
        sThreeItmDir.close()
        sFourItmDir.close()
        bTwoItmDir.close()
        bThreeItmDir.close()
        bFourItmDir.close()