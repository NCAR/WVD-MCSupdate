#NetCDF printer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python NetCDFQuickPrint.py ..\WVDNewArchitectureUpdate\WVD_Architecture_Update\Data\NetCDFOutput\20180322\LLsample200000.nc

import sys
from netCDF4 import Dataset

dataset = Dataset(sys.argv[1])
print (dataset.file_format)
print (dataset)
print (dataset.dimensions.keys())
print (dataset.dimensions['Timestamp'])
print (dataset.variables.keys())

print (dataset.variables['LaserNum'][:])
#print (dataset.variables['LaserNum'].units)


            
