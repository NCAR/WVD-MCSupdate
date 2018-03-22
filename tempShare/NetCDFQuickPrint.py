#NetCDF printer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:

import sys
from netCDF4 import Dataset

dataset = Dataset(sys.argv[1])
print (dataset.file_format)
print (dataset)
print (dataset.dimensions.keys())
print (dataset.dimensions['Timestamp'])
print (dataset.variables.keys())

#print (dataset.variables['Wavelength'][:])

#print (dataset.variables['LaserNum'].units)
print (dataset.variables['LaserNum'][:])
