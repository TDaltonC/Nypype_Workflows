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
    
def extValueLookup(trialType):
    if trialType == 0:
        value = 0
    elif trialType == 1:
        value = 0
    elif trialType == 2:
        value = 1
    elif trialType == 3:
        value = 1
    elif trialType == 4:
        value = 0
    elif trialType == 5:
        value = 0
    elif trialType == 6:
        value = 0
    elif trialType == 7:
        value = 2
    elif trialType == 8:
        value = 2
    elif trialType == 9:
        value = 2
    return value

def VolumeTypeLookUp(VolNum,liveTrials):
    try:
        TrialType = int(liveTrials[liveTrials.volumeNum == VolNum].TargetType)
        return TrialType
    except:
        return 0

extValueLookupVec = np.vectorize(extValueLookup)
VolumeTypeLookUp_Vec = np.vectorize(VolumeTypeLookUp,excluded = ['liveTrials'])
"""
==============
MEAT & POTATOS
==============
"""   
subjectList = ['SID702','SID703','SID705','SID706','SID707','SID708','SID709','SID710']

for subjectID in subjectList:
#   load the trial by trial data for this subject
    trialbytrial = pandas.DataFrame.from_csv(os.path.abspath('../../RawData/'+ subjectID + '/dataFrames/trialByTrial.csv'))

    trialbytrial['TargetType'] = extValueLookupVec(trialbytrial.trialType)

#   Fliter down to multi-run event files  
    liveTrials = trialbytrial[(trialbytrial.TargetType  != 0)]
    
    liveTrials.reset_index(level=0, inplace=True)
    liveTrials["volumeNum"] = np.rint(liveTrials.tOnset+5/2)
    
    
    
    print subjectID
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the evelt fiels acording to run
        liveTrialsSingleRun = liveTrials[(liveTrials.run  == run)]
#        THIS only adds lines up to the last desired volume, there maybe some undesierable volumes beyond that.
        filledOut = pandas.DataFrame(data = {"trialType":np.zeros(int(max(liveTrialsSingleRun.volumeNum)+1))})        
        filledOut["trialType"] = VolumeTypeLookUp_Vec(filledOut.index,liveTrials = liveTrialsSingleRun)
#       Name and open the destinations for event files
        writeDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        filledOut.to_csv(writeDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        writeDir.close()