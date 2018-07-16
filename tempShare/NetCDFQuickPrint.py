#NetCDF printer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python NetCDFQuickPrint.py ../WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/NetCDFOutput/20180426/MergedFiles080000.nc WVOffline

import sys
from netCDF4 import Dataset

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import pylab
from matplotlib.colors import LogNorm

dataset = Dataset(sys.argv[1])
print (dataset.file_format)
print (dataset)
print (dataset.dimensions.keys())
print (dataset.dimensions['time'])
print (dataset.variables.keys())

print ("time = ", dataset.variables['time'][:50])
print ("time units = ", dataset.variables['time'].units)
print ("time = ", dataset.variables['time'][-50:])

print ("range = ", dataset.variables['range'][:50])
print ("range units = ", dataset.variables['range'].units)

print (sys.argv[2]," = ", dataset.variables[sys.argv[2]][:50])
print (sys.argv[2]," units = ", dataset.variables[sys.argv[2]].units)

data = dataset.variables[sys.argv[2]]
time = dataset.variables['time']
rangei= dataset.variables['range']

#pylab.pcolor(time, rangei, data)
 
datamin=100000000
datamax=0
for i in range(0,len(data)):
    if not np.isnan(data[i][0]):
        minval = min(data[i])
        maxval = max(data[i])
        if datamin > minval:
            datamin = minval
        if datamax < maxval:
            datamax = maxval

data = np.array(data).T.tolist()

print ("min = ",datamin)
print ("max = ",datamax)

if datamin < 1:
    datamin=1

pylab.pcolor(time, rangei, data, norm=LogNorm(vmin=datamin, vmax=datamax), cmap='PuBu_r')
pylab.colorbar()
pylab.show()
