# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 16:08:50 2014

@author: Dalton
"""

## From MNI to 2mm voxel space

MNIx = 32
MNIy = -51
MNIz =  59

# X coordinate
Vx = (MNIx-90)/(-2)

# Y coordinate
Vy = (MNIy + 126)/2

# Z coordinate
Vz = (MNIz+72)/2

print Vx
print Vy
print Vz

