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
 
def valueLookup(itemRank,itemValueDF):
    if itemRank == 0 :
        value = 0.
    else:
        value = itemValueDF[itemValueDF.index == str(itemRank)].CSValue
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
    itemvalue = pandas.DataFrame.from_csv(os.path.abspath('../../../RawData/'+ subjectID + '/dataFrames/itemValue.csv'))
#   Add a column of ones to the dataframe (this is usefull for creating the three column files)    
    trialbytrial['ones'] = 1

#   Create a new column that is the linear value of each option (SORRY THIS IS SO WET! WE WERE IN A HURRY!!!)
#       value of item in position 1
    trialbytrial['item1value'] = valueLookupVec(trialbytrial.item1,itemValueDF = itemvalue)
#       value of item in position 2
    trialbytrial['item2value'] = valueLookupVec(trialbytrial.item2,itemValueDF = itemvalue)
#       value of item in position 3
    trialbytrial['item3value'] = valueLookupVec(trialbytrial.item3,itemValueDF = itemvalue)
#       value of item in position 4
    trialbytrial['item4value'] = valueLookupVec(trialbytrial.item4,itemValueDF = itemvalue)
#        the linear value is the sum of the measure for each of the items in a bundle
    trialbytrial['linearValue'] = trialbytrial['item1value'] + trialbytrial['item2value'] + trialbytrial['item3value'] + trialbytrial['item4value']
    fixedOptionValue = valueLookup(11,itemvalue)
    trialbytrial['linearDiff'] = abs(trialbytrial['linearValue'] - fixedOptionValue['11'])

#   Fliter down to multi-run event files  
    valueTrials = trialbytrial[(trialbytrial.linearValue  != 0)]
    controlTrials = trialbytrial[(trialbytrial.trialType  == 2)|(trialbytrial.trialType  == 3)]
    scalingTrials = trialbytrial[(trialbytrial.trialType  == 4)|(trialbytrial.trialType  == 5)|(trialbytrial.trialType  == 6)]
    bundlingTrials = trialbytrial[(trialbytrial.trialType  == 7)|(trialbytrial.trialType  == 8)|(trialbytrial.trialType  == 9)]
    print subjectID
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        valueSingleRun = valueTrials[(valueTrials.run  == run)]
        controlSingleRun = controlTrials[(controlTrials.run  == run)] 
        scalingSingleRun = scalingTrials[(scalingTrials.run  == run)]
        bundlingSingleRun = bundlingTrials[(bundlingTrials.run  == run)]
 #      Cut down to only 3 columns
        value3Col = valueSingleRun[['tResponse','linearValue']]
        control3Col = controlSingleRun[['tResponse','ones']]
        scaling3Col = scalingSingleRun[['tResponse','ones']]
        bundling3Col = bundlingSingleRun[['tResponse','ones']]
#       Name and open the destinations for event files
        valueDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Value.run00'+ str(run) +'.txt'))
        controlDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        scalingDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Scaling.run00'+ str(run) +'.txt'))
        BundlingDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Bundling.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        value3Col.to_csv(valueDir, sep ='\t', header = False)
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        bundling3Col.to_csv(BundlingDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        valueDir.close()
        controlDir.close()
        scalingDir.close()
        BundlingDir.close()