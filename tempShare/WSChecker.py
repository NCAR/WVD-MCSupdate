#Weather Station Data printer for NCAR WVD system
#Brad Schoenrock
#Jul. 2018
# useage:
# python WSChecker.py ..\WVDNewArchitectureUpdate\WVD_Architecture_Update\Data\NetCDFOutput\20180322\WSsample200000.nc



import sys
from netCDF4 import Dataset
import matplotlib.pyplot as plt


dataset = Dataset(sys.argv[1])
print (dataset.file_format)
print (dataset)
print (dataset.dimensions.keys())
print (dataset.dimensions['time'])
print (dataset.variables.keys())

print ("time = ", dataset.variables['time'][:50])
print ("time units = ", dataset.variables['time'].units)
print ("time = ", dataset.variables['time'][-50:])

