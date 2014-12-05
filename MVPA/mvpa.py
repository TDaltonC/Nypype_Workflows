# -*- coding: utf-8 -*-
"""
Basic MVPA Script
Calvin
"""

from mvpa2.suite import *
import numpy as np

"""
if __debug__:
    from mvpa2.base import debug
    debug.active += ["SVS", "SLC"]
"""

"""========Functions==========="""

def removeNan(dataset):
    dataset= np.array(dataset.samples)
    return np.nan_to_num(dataset)


"""========Preprocessing==========="""

#Specify datapath for preprocessed scans, attribute (EV) file, and masks
datapath = '/home/brain/Desktop/mvpa/'

#Load files from above path
attr = SampleAttributes(os.path.join(datapath, 'Run5.txt'))
fds = fmri_dataset(samples=os.path.join(datapath, 'scan5s008.nii.gz'),
                   targets=attr.targets, chunks=attr.chunks)
                   #mask=os.path.join(datapath,'maskname')              
   
#Detrender (equivalent to highpass, may be redundant)                
detrender=PolyDetrendMapper(polyord=1, chunks_attr='chunks')
detrended_fds = fds.get_mapped(detrender)

print np.unique(fds.sa.targets)

#Normalize with a z-score & discard resting state scans
#don't need z-score for SVM
#zscorer=ZScoreMapper(param_est=('targets', [0]))
#zscore(detrended_fds, param_est=('targets', [0]))
fds=detrended_fds
fds=fds[fds.sa.targets != '0']

#remove any NaNs and output preprocessed file
fds.samples=removeNan(fds)
nimg = map2nifti(fds)
nimg.to_filename('mytest.nii.gz')


#label scans as odd or even for classifier 
rnames = {0:'even', 1:'odd'}
fds.sa['runtype'] = [rnames[float(c)%2] for c in fds.sa.chunks]

averager = mean_group_sample(['targets', 'runtype'])
type(averager)
fds = fds.get_mapped(averager)

fds=fds[:, np.all(np.isfinite(fds.samples),axis=0)]

"""========Classifier==========="""

#k-nearest neighbors
#clf = kNN(k=1, dfx=one_minus_correlation, voting='majority')
#clf.set_postproc(None)

#linear support vector
clf = LinearCSVMC()
hpart = HalfPartitioner(attr='runtype')
cv=CrossValidation(clf,hpart)
cv_results = cv(fds)

print cv_results.samples
print np.mean(cv_results)
