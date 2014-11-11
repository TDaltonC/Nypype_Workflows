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
#   Add a column of ones to the dataframe (this is usefull for creating the three column files)    
    trialbytrial['ones'] = 1
#   Solve for the number of items on screen
    trialbytrial['numItmOnScrn'] = VEC_num_itm_on_screen(trialbytrial['trialType'])
#   Fliter down to multi-run event files  
    controlTrials = trialbytrial[(trialbytrial.numItmOnScrn  == 1)]
    twoItmTrials = trialbytrial[(trialbytrial.numItmOnScrn  == 2)]
    threeItmTrials = trialbytrial[(trialbytrial.numItmOnScrn  == 3)]
    fourItmTrials = trialbytrial[(trialbytrial.numItmOnScrn  == 4)]
    print subjectID
    runs =set(trialbytrial['run'])
    for run in runs:
#       chop each of the event fiels acording to run
        controlSingleRun = controlTrials[(controlTrials.run  == run)] 
        twoItmSingeRun = twoItmTrials[(twoItmTrials.run  == run)]
        threeItmSingeRun = threeItmTrials[(threeItmTrials.run  == run)]
        fourItmSingeRun = fourItmTrials[(fourItmTrials.run  == run)]
 #      Cut down to only 3 columns
        control3Col = controlSingleRun[['tResponse','ones']]
        twoItm3Col = twoItmSingeRun[['tResponse','ones']]
        threeItm3Col = threeItmSingeRun[['tResponse','ones']]
        fourItm3Col = fourItmSingeRun[['tResponse','ones']]
#       Name and open the destinations for event files
        controlDir  = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/Control.run00'+ str(run) +'.txt'))
        twoItmDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/TwoItems.run00'+ str(run) +'.txt'))
        threeItmDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/ThreeItems.run00'+ str(run) +'.txt'))
        fourItmDir = safe_open_w(os.path.abspath('EVfiles/'+subjectID + '/Run' + str(run) + '/FourItems.run00'+ str(run) +'.txt'))
#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        twoItm3Col.to_csv(twoItmDir, sep ='\t', header = False)
        threeItm3Col.to_csv(threeItmDir, sep ='\t', header = False)
        fourItm3Col.to_csv(fourItmDir, sep ='\t', header = False)        
#       Be Tidy! Close all of those open files! 
        controlDir.close()
        twoItmDir.close()
        threeItmDir.close()
        fourItmDir.close()

