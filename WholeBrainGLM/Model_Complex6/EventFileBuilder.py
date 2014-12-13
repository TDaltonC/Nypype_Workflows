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

"""
=========
Functions
=========
"""
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')
 
def num_itm_on_screen(trialType):
    if   trialType == 1:
        return 0
    elif trialType in (2, 3):
        return 1
    elif trialType in (4, 7):
        return 2
    elif trialType in (5, 8):
        return 3
    elif trialType in (6, 9):
        return 4

VEC_num_itm_on_screen = np.vectorize(num_itm_on_screen)

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

    trialbytrial['numItmOnScrn'] = VEC_num_itm_on_screen(trialbytrial['trialType'])

#   Fliter down to multi-run event files  
    valueTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    difficultyTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    controlTrials = trialbytrial[(trialbytrial.trialType  == 2)|(trialbytrial.trialType  == 3)]
    scalingTrials = trialbytrial[(trialbytrial.trialType  == 4)|(trialbytrial.trialType  == 5)|(trialbytrial.trialType  == 6)]
    bundlingTrials = trialbytrial[(trialbytrial.trialType  == 7)|(trialbytrial.trialType  == 8)|(trialbytrial.trialType  == 9)]
    itmCount = trialbytrial[(trialbytrial.numItmOnScrn  != 0)]
    ScalingItmCount = itmCount[(itmCount.trialType  == 4)|(itmCount.trialType  == 5)|(itmCount.trialType  == 6)]
    bundlingItmCount = itmCount[(itmCount.trialType  == 7)|(itmCount.trialType  == 8)|(itmCount.trialType  == 9)]
    print subjectID
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        valueSingleRun = valueTrials[(valueTrials.run  == run)]
        difficultySingleRun = difficultyTrials[(difficultyTrials.run  == run)]
        controlSingleRun = controlTrials[(controlTrials.run  == run)] 
        scalingSingleRun = scalingTrials[(scalingTrials.run  == run)]
        bundlingSingleRun = bundlingTrials[(bundlingTrials.run  == run)]
        ScalingItmCountRun = ScalingItmCount[(ScalingItmCount.run  == run)]
        bundlingItmCountRun = bundlingItmCount[(bundlingItmCount.run  == run)]
 #      Cut down to only 3 columns
        value3Col = valueSingleRun[['tResponse','valueOption']]
        difficulty3Col = difficultySingleRun[['tResponse','valueDiff']]
        control3Col = controlSingleRun[['tResponse','ones']]
        scaling3Col = scalingSingleRun[['tResponse','ones']]
        bundling3Col = bundlingSingleRun[['tResponse','ones']]
        ScalingItmCount3Col = ScalingItmCountRun[['tResponse','numItmOnScrn']]
        bundlingItmCount3Col = bundlingItmCountRun[['tResponse','numItmOnScrn']]
#       Name and open the destinations for event files
        valueDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Value.run00'+ str(run) +'.txt'))
        difficultyDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Difficulty.run00'+ str(run) +'.txt'))
        controlDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        scalingDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Scaling.run00'+ str(run) +'.txt'))
        BundlingDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Bundling.run00'+ str(run) +'.txt'))
        ScalingItmCountDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ScalingItmCount.run00'+ str(run) +'.txt'))
        bundlingItmCountDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/BundlingItmCount.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        value3Col.to_csv(valueDir, sep ='\t', header = False)
        difficulty3Col.to_csv(difficultyDir, sep ='\t', header = False)
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        bundling3Col.to_csv(BundlingDir, sep ='\t', header = False)
        ScalingItmCount3Col.to_csv(  ScalingItmCountDir, sep ='\t', header = False) 
        bundlingItmCount3Col.to_csv(bundlingItmCountDir, sep ='\t', header = False)    
#        Be Tidy! Close all of those open files! 
        valueDir.close()
        difficultyDir.close()
        controlDir.close()
        scalingDir.close()
        BundlingDir.close()
        ScalingItmCountDir.close()
        bundlingItmCountDir.close()

