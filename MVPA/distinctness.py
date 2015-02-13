"""
usage of mahalanobis distance to determine 'distance' between two datasets
a la allefeld 2014
input arrays to determine distance between target A and B each consist of an array
of all volumes for the target.

This could be used in conjunction with the searchlight in order to determine which regions
have strong commonality between single-item and homogeneous bundle.
""""

import scipy.spatial.distance.mahalanobis

def distinctness(array1, array2):

raw_dist = mahalanobis(array1, array2)

#perform some operations

return raw_dist

return 
