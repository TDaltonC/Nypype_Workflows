# -*- coding: utf-8 -*-
"""
Custom MVPA script
Who needs pymvpa anyway?

Calvin Leather
"""

import os
import numpy as np
import nibabel as nib
from sklearn import neighbors, svm, naive_bayes
import gc
from math import factorial

datapath = '/home/brain/Desktop/analysismvpa/'
source_file = os.path.join(datapath, 'Scan5s008alowgaus.nii.gz')
evFile = 'Run5simplevcomplex.txt'
classifier = 'knn'
centroid_calc= True


def getchunks(datapath, filename):
    #open a 2 column, tab delimeted text file, 1st has targets, 2nd has chunks
    text_file = np.loadtxt(os.path.join(datapath, filename))
    text_file_targets = text_file[:, 0]
    text_file_targets.flatten()
    text_file_chunks = text_file[:,1]
    text_file_chunks.flatten()
    return text_file_targets, text_file_chunks

#use nibabel to import nifti
img = nib.load(source_file)
data = img.get_data()

#open attribute file and get chunks/targets
chunks, targets = getchunks(datapath, evFile)
if data.shape[3] != len(chunks):
    print "length not equal"

"""z score by estimating mean and SD for each voxel in block 
of resting state volumes before each chunk
might not need this if already done in nipype"""

#remove all volumes we aren't interested in (target = 0) & reshape into ordered pairs
data = data[:,:,:,(targets != 0)]
targets = targets[(targets != 0)]
data_dims = data.shape
flat_data = np.reshape(data, (data_dims[0]*data_dims[1]*data_dims[2], data_dims[3]))

#select ROI
flat_data = flat_data[300000:300010,:]

#determine equal distribution into testing and training sets
count = np.zeros(len(np.unique(targets)))
sort = np.zeros(len(targets))
for i in range(0, len(targets)-1):
    if count[targets[i]-1]==0:
        sort[i]=0
        count[targets[i]-1]=1
    else:
        sort[i]=1
        count[targets[i]-1]=0
        
#actually assign them
flat_data_train = flat_data[:,(sort==0)]
flat_data_test = flat_data[:,(sort==1)]
targets_train = targets[sort==0]
targets_test = targets[sort ==1]

#define, train and run the classifiers
if classifier=='knn':
    clf= neighbors.KNeighborsClassifier(n_neighbors=3)
    clf.fit(np.transpose(flat_data_train), targets_train)
    Z = clf.predict(np.transpose(flat_data_test))

elif classifier=='svm':
    clf = svm.SVC(kernel='rbf')
    
elif classifier=='gnb':
    clf = naive_bayes.GaussianNB()  
        
else:
    print 'classifier name invalid'

clf.fit(np.transpose(flat_data_train), targets_train)
Z = clf.predict(np.transpose(flat_data_test))

#print error rate
print np.sum(Z-targets_test)/len(Z)

if centroid_calc == True:
    centroid=np.zeros((len(np.unique(targets)),len(flat_data_test[:,1])))
    for i in range(0,len(np.unique(targets))):
        centroid[i] = np.mean(np.transpose(flat_data_test[:, targets_test==i+1]), axis=0)
    #averages, cat 1v2, 1v3,... 1vn, 2v3, 2v4, 2vn, ...n-1/n
    number_of_combinations=factorial(np.unique(targets).size)/(factorial((np.unique(targets).size-2))*2)
    centroid_pairs = np.zeros((number_of_combinations, flat_data_test[:,1].size))
    for i in range(0, np.unique(targets).size-1):
        for j in range(i+1, np.unique(targets).size):
            print (centroid[i,:]+centroid[j,:])/2
            

#take out the garbage
del data, img, flat_data
gc.collect()
