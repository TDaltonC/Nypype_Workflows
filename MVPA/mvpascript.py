# -*- coding: utf-8 -*-
"""
Basic MVPA Script
Calvin
"""

from mvpa2.suite import *

"""
if __debug__:
    from mvpa2.base import debug
    debug.active += ["SVS", "SLC"]
"""

"""========Preprocessing==========="""

#Specify datapath for preprocessed scans, attribute (EV) file, and masks
datapath = '/media/datadrive/subj1'

#Load files from above path, note that attr.targets and .chunks is predefined, doesn't need a header
attr = SampleAttributes(os.path.join(datapath, 'labels.txt'))
fds = fmri_dataset(samples=os.path.join(datapath, 'bold.nii.gz'),
                   targets=attr.targets, chunks=attr.chunks,
                   #mask=os.path.join(datapath,)
                   )
   
#Detrender (equivalent to highpass, may be redundant)                
detrender=PolyDetrendMapper(polyord=1, chunks_attr='chunks')
detrended_fds = fds.get_mapped(detrender)

#Normalize with a z-score & discard resting state scans
zscorer=ZScoreMapper(param_est=('targets', ['rest']))
zscore(detrended_fds, param_est=('targets', ['rest']))
fds=detrended_fds
fds_w_rest = fds
fds=fds[fds.sa.targets != 'rest']

#label scans as odd or even for classifier 
rnames = {0:'even', 1:'odd'}
fds.sa['runtype'] = [rnames[c%2] for c in fds.sa.chunks]

averager = mean_group_sample(['targets', 'runtype'])
type(averager)
fds = fds.get_mapped(averager)
print(fds.sa.targets)


"""========Classifier==========="""

#
clf = kNN(k=1, dfx=one_minus_correlation, voting='majority')
clf.set_postproc(None)
hpart = HalfPartitioner(attr='runtype')
cv=CrossValidation(clf,hpart)
cv_results = cv(fds)

print cv_results.samples
print np.mean(cv_results)

print 'done'
