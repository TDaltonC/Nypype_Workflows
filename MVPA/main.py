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
import itertools
import matplotlib.pyplot as plt

datapath = '/home/brain/Desktop/analysismvpa/'
source_file = os.path.join(datapath, 'Scan5s008alowgaus.nii.gz')
evFile = 'Run5simplevcomplex.txt'
classifier = 'knn'
spotlight_size='r1'

centroid_calc= False
cross_validation = False #warning, this could take a long time, O(n!)
spotlight_calc = True


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

if spotlight_calc == True:
    spotlight_dataset = data[:,:,:,1]
    
    r0 = [(0,0,0)]
    r1 = [[0,0,0],[0,1,0],[1,0,0],[0,0,1]]
    r2 = [[0,0,0],[0,1,0],[1,0,0],[0,0,1],
         [1,1,0],[1,0,1],[0,1,1], [1,1,1],
         [0,2,0],[2,0,0],[0,0,2]]
  
    size_set = spotlight_dataset.size 
    
    for i in range(0,10):
        print 'element {} ****** of {}'.format(i,size_set)
        try:
            x, y, z = 45, 45+i, 45 
            neighborhood_adj=np.array(eval(spotlight_size))
            neighborhood = np.ndarray((neighborhood_adj.shape[1]*2+1,3))
            spotlight_cube = np.ndarray(neighborhood_adj.shape[1]*2+1)
            neighborhood[0,0:3]=[x,y,z]
            spotlight_cube[0] = spotlight_dataset[x,y,z]
            for i in np.arange(.5,neighborhood_adj.shape[0]*.5+1,1):
                neighborhood[i*2, 0:3]=[x+neighborhood_adj[i+.5][0], y+neighborhood_adj[i+.5][1], z+neighborhood_adj[i+.5][2]]
                spotlight_cube[i*2] = spotlight_dataset[x+neighborhood_adj[i+.5][0], y+neighborhood_adj[i+.5][1], z+neighborhood_adj[i+.5][2]]
                neighborhood[i*2+1, 0:3]=[x-neighborhood_adj[i+.5][0], y-neighborhood_adj[i+.5][1], z-neighborhood_adj[i+.5][2]]
                spotlight_cube[i*2+1] = spotlight_dataset[x-neighborhood_adj[i+.5][0], y-neighborhood_adj[i+.5][1], z-neighborhood_adj[i+.5][2]]
            print spotlight_cube
            
            
        except RuntimeError:
            print "oops"
    
            
#spotlight loop
"""

size is 91, 109, 91, number of volumes
first 91 is right left
109 is rostral/caudal
second 91 is dorsal/ventral

r0 = [(0,0,0)]4
r1 = [[0,0,0],[0,1,0],[1,0,0],[0,0,1]]
r2 = [[0,0,0],[0,1,0],[1,0,0],[0,0,1],
     [1,1,0],[1,0,1],[0,1,1], [1,1,1],
     [0,2,0],[2,0,0],[0,0,2]]
    
for i in range(0, flat_data_test[:,1].size): 
    try:
        element i + and - neighborhood array
     
take elements v to the right and left of i
shift vertically +/- n up to v, take elements v-n to right and left
shift +/-in depth

for i in range(0, flat_data_test[:,1].size):
    determine voxels in searchlight around element i
    width=
    depth=
    searchlight = [i, i-1, i+1, i+width, i+width-1, i+width+1, i-width-1, i-width+1, i-width]
    searchlight.append(searchlight-depth)
    searchligh.append(searchlight+depth)
    searchlight.append(i+2*depth)
    searchlight.append(i-2*depth)
    searchlight append(i+2)
    searchlight.append(i-2)
    
    searchlight = searchlight[searchlight>0 && searchlight[flat_data_test.size]
    
    clf.predict(searchlight_sphere)
r=0, 1 voxel r=1, 7 voxles  r=2, 15 voxles      
"""
            
if cross_validation == True:
    #warning, this takes a long time, O(n!)
    target_length=targets_train.size;
    permuted_targets_train = np.array(list(itertools.permutations(targets_train))); #generate all permutations of targets in train set
    cv_results=np.zeros(permuted_targets_train.shape[0])
    for i in range(0,permuted_targets_train.shape[0]): #iterate through permutations, train and test with each, 
        clf.fit(np.transpose(flat_data_train), permuted_targets_train[i,:]-1)
        Z = clf.predict(np.transpose(flat_data_test))
        cv_results[i]=np.sum(targets_test-Z)/len(Z) #cv_results is accuracy
        cv_results_10=cv_results*10
        
    bin_unique=np.zeros(np.unique(cv_results_10).size+100)  
    for i in np.unique(cv_results_10):
        bin_unique[i]=cv_results_10[cv_results_10==i].sum()
    x=np.arange(0,1.1, .1)
    plt.bar(x,bin_unique[0:11],.1,align='center')
    del permuted_targets_train, cv_results
        

#take out the garbage
#del data, img, flat_data, spotlight_dataset
gc.collect()
