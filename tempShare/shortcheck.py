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
print (dataset.dimensions['time'])
print (dataset.variables.keys())


print ("time = ", dataset.variables['time'][:50])
print ("time units = ", dataset.variables['time'].units)




print ("Power = ", dataset.variables['Power'][:50])
print ("Power units = ", dataset.variables['Power'].units)

print ("ChannelAssignment = ", dataset.variables['ChannelAssignment'][:50])
print ("ChannelAssignment units = ", dataset.variables['ChannelAssignment'].units)





"""

print ("LaserName = ", dataset.variables['LaserName'][:50])
print ("LaserName units = ", dataset.variables['LaserName'].units)

print ("Wavelength = ", dataset.variables['Wavelength'][:50])
print ("Wavelength units = ", dataset.variables['Wavelength'].units)

print ("WaveDiff = ", dataset.variables['WaveDiff'][:50])
print ("WaveDiff units = ", dataset.variables['WaveDiff'].units)

print ("IsLocked = ", dataset.variables['IsLocked'][:50])
print ("IsLocked units = ", dataset.variables['IsLocked'].units)

print ("TempDesired = ", dataset.variables['TempDesired'][:50])
print ("TempDesired units = ", dataset.variables['TempDesired'].units)

print ("TempMeas = ", dataset.variables['TempMeas'][:50])
print ("TempMeas units = ", dataset.variables['TempMeas'].units)

print ("Current = ", dataset.variables['Current'][:50])
print ("Current units = ", dataset.variables['Current'].units)

"""



