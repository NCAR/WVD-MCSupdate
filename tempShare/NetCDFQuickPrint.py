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



#print ("WVOnlineWavelength = ", dataset.variables['WVOnlineWavelength'][:15])
#print ("WVOnlineWavelength units = ", dataset.variables['WVOnlineWavelength'].units)
#print ("WVOfflineWavelength = ", dataset.variables['WVOfflineWavelength'][:15])
#print ("WVOfflineWavelength units = ", dataset.variables['WVOfflineWavelength'].units)

#print ("WVOnlineWaveDiff = ", dataset.variables['WVOnlineWaveDiff'][:15])
#print ("WVOnlineWaveDiff units = ", dataset.variables['WVOnlineWaveDiff'].units)
#print ("WVOfflineWaveDiff = ", dataset.variables['WVOfflineWaveDiff'][:15])
#print ("WVOfflineWaveDiff units = ", dataset.variables['WVOfflineWaveDiff'].units)

#print ("OnlineH2OPower = ", dataset.variables['OnlineH2OPower'][:15])
#print ("OnlineH2OPower units = ", dataset.variables['OnlineH2OPower'].units)
#print ("OnlineH2OPower = ", dataset.variables['OnlineH2OPower'][:15])
#print ("OnlineH2OPower units = ", dataset.variables['OnlineH2OPower'].units)

#print (dataset.variables['LaserNum'].units)


            
