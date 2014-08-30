# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 12:39:45 2014

@author: Dalton
"""
import os
import pandas


trialbytrial = pandas.DataFrame.from_csv(os.path.abspath('../../RawData/SID702/MatLABOutput/trialByTrial.csv'))

print trialbytrial.head