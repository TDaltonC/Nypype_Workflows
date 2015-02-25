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

import sys
sys.path.insert(0,  '/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Scripts')
import valuePilotFunctions as vpf

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
 
def valueLookup(itemRank,itemValueDF):
    if itemRank == 0 :
        value = 0. 
    else:
        value = itemValueDF[itemValueDF.index == str(itemRank)].eToTheCSValue
    return value
    
valueLookupVec = np.vectorize(valueLookup,excluded = ['itemValueDF'])

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

#   Fliter down to multi-run event files  
    valueTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    difficultyTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    controlTrials = trialbytrial[(trialbytrial.trialType  == 2)|(trialbytrial.trialType  == 3)]
    scalingTrials = trialbytrial[(trialbytrial.trialType  == 4)|(trialbytrial.trialType  == 5)|(trialbytrial.trialType  == 6)]
    bundlingTrials = trialbytrial[(trialbytrial.trialType  == 7)|(trialbytrial.trialType  == 8)|(trialbytrial.trialType  == 9)]
    print subjectID      
#   Make a plot of the distribution of value and value-diff across the three condictions and save them.         
    vpf.savePlotDisributionsByTT(trialbytrial,"linearValue",'EVfiles/'+subjectID)
    vpf.savePlotDisributionsByTT(trialbytrial,"linearDiff",'EVfiles/'+subjectID)
    vpf.savePlotDisributionsByItemCount(trialbytrial,"linearValue",'EVfiles/'+subjectID)
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        valueSingleRun = valueTrials[(valueTrials.run  == run)]
        difficultySingleRun = difficultyTrials[(difficultyTrials.run  == run)]
        controlSingleRun = controlTrials[(controlTrials.run  == run)] 
        scalingSingleRun = scalingTrials[(scalingTrials.run  == run)]
        bundlingSingleRun = bundlingTrials[(bundlingTrials.run  == run)]
 #      Cut down to only 3 columns
        value3Col = valueSingleRun[['tResponse','linearValue']]
        difficulty3Col = difficultySingleRun[['tResponse','linearDiff']]
        control3Col = controlSingleRun[['tResponse','ones']]
        scaling3Col = scalingSingleRun[['tResponse','ones']]
        bundling3Col = bundlingSingleRun[['tResponse','ones']]
#       Name and open the destinations for event files
        valueDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Value.run00'+ str(run) +'.txt'))
        difficultyDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Difficulty.run00'+ str(run) +'.txt'))
        controlDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        scalingDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Scaling.run00'+ str(run) +'.txt'))
        BundlingDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Bundling.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        value3Col.to_csv(valueDir, sep ='\t', header = False)
        difficulty3Col.to_csv(difficultyDir, sep ='\t', header = False)
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        bundling3Col.to_csv(BundlingDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        valueDir.close()
        difficultyDir.close()
        controlDir.close()
        scalingDir.close()
        BundlingDir.close()