#NetCDF printer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python NetCDFQuickPrint.py ..\WVDNewArchitectureUpdate\WVD_Architecture_Update\Data\NetCDFOutput\20180322\LLsample200000.nc

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
print ("type(time)=",type(dataset.variables['time'][:50]))
print ("time units = ", dataset.variables['time'].units)


print ("WVOnline = ", dataset.variables['WVOnline'][:50])
print ("type(WVOnline)=",type(dataset.variables['WVOnline'][:50]))
print ("WVOnline units = ", dataset.variables['WVOnline'].units)


print ("WVOnlinePower = ", dataset.variables['WVOnlinePower'][:50])
print ("WVOnlinePower units = ", dataset.variables['WVOnlinePower'].units)


print ("WSRelHum = ", dataset.variables['WSRelHum'][:50])
print ("WSRelHum units = ", dataset.variables['WSRelHum'].units)


print ("UPSHoursOnBattery = ", dataset.variables['UPSHoursOnBattery'][:50])
print ("UPSHoursOnBattery units = ", dataset.variables['UPSHoursOnBattery'].units)


print ("time = ", dataset.variables['time'][:50])
print ("ProfPerHist = ", dataset.variables['ProfPerHist'][:50])
print ("nsPerBin = ", dataset.variables['nsPerBin'][:50])
print ("WVOnline = ", dataset.variables['WVOnline'][:50])
print ("WVOffline = ", dataset.variables['WVOffline'][:50])
print ("WVOnlinePower = ", dataset.variables['WVOnlinePower'][:50])
print ("WVOfflinePower = ", dataset.variables['WVOfflinePower'][:50])
print ("HSRLPower = ", dataset.variables['HSRLPower'][:50])
print ("WVOnlineLaserWavelength = ", dataset.variables['WVOnlineLaserWavelength'][:50])
print ("WVOfflineLaserWavelength = ", dataset.variables['WVOfflineLaserWavelength'][:50])
print ("HSRLLaserWavelength = ", dataset.variables['HSRLLaserWavelength'][:50])
print ("WVOnlineLaserWaveDiff = ", dataset.variables['WVOnlineLaserWaveDiff'][:50])
print ("WVOfflineLaserWaveDiff = ", dataset.variables['WVOfflineLaserWaveDiff'][:50])
print ("HSRLLaserWaveDiff = ", dataset.variables['HSRLLaserWaveDiff'][:50])
print ("WVOnlineLaserTempDesired = ", dataset.variables['WVOnlineLaserTempDesired'][:50])
print ("WVOfflineLaserTempDesired = ", dataset.variables['WVOfflineLaserTempDesired'][:50])
print ("HSRLLaserTempDesired = ", dataset.variables['HSRLLaserTempDesired'][:50])
print ("WVOnlineLaserTempMeas = ", dataset.variables['WVOnlineLaserTempMeas'][:50])
print ("WVOfflineLaserTempMeas = ", dataset.variables['WVOfflineLaserTempMeas'][:50])
print ("HSRLLaserTempMeas = ", dataset.variables['HSRLLaserTempMeas'][:50])
print ("WVOnlineLaserCurrent = ", dataset.variables['WVOnlineLaserCurrent'][:50])
print ("WVOfflineLaserCurrent = ", dataset.variables['WVOfflineLaserCurrent'][:50])
print ("HSRLLaserCurrent = ", dataset.variables['HSRLLaserCurrent'][:50])
print ("WVEtalonTemperature = ", dataset.variables['WVEtalonTemperature'][:50])
print ("WVEtalonTempDiff = ", dataset.variables['WVEtalonTempDiff'][:50])
print ("HSRLEtalonTemperature = ", dataset.variables['HSRLEtalonTemperature'][:50])
print ("HSRLEtalonTempDiff = ", dataset.variables['HSRLEtalonTempDiff'][:50])
print ("WSTemperature = ", dataset.variables['WSTemperature'][:50])
print ("WSRelHum = ", dataset.variables['WSRelHum'][:50])
print ("WSPressure = ", dataset.variables['WSPressure'][:50])
print ("WSAbsHum = ", dataset.variables['WSAbsHum'][:50])
print ("ContainerTemperature = ", dataset.variables['ContainerTemperature'][:50])
print ("UPSTemperature = ", dataset.variables['UPSTemperature'][:50])
print ("UPSHoursOnBattery = ", dataset.variables['UPSHoursOnBattery'][:50])
print ("range = ", dataset.variables['range'][:50])
print ("volume_number = ", dataset.variables['volume_number'][:50])
print ("instrument_type = ", dataset.variables['instrument_type'][:50])
print ("time_coverage_start = ", dataset.variables['time_coverage_start'][:50])
print ("time_coverage_end = ", dataset.variables['time_coverage_end'][:50])
print ("latitude = ", dataset.variables['latitude'][:50])
print ("longitude = ", dataset.variables['longitude'][:50])
print ("altitude = ", dataset.variables['altitude'][:50])
print ("sweep_number = ", dataset.variables['sweep_number'][:50])
print ("sweep_mode = ", dataset.variables['sweep_mode'][:50])
print ("len(sweep_mode)=",len(dataset.variables['sweep_mode']))
print ("len(sweep_mode[0])=",len(dataset.variables['sweep_mode'][0]))
print ("fixed_angle = ", dataset.variables['fixed_angle'][:50])
print ("sweep_start_ray_index = ", dataset.variables['sweep_start_ray_index'][:50])
print ("sweep_end_ray_index = ", dataset.variables['sweep_end_ray_index'][:50])
print ("azimuth = ", dataset.variables['azimuth'][:50])
print ("elevation = ", dataset.variables['elevation'][:50])




plt.plot(dataset.variables['time'],dataset.variables['WSTemperature'] )
plt.show()





"""

print (" = ", dataset.variables[''][:50])
print (" units = ", dataset.variables[''].units)

print ("Power = ", dataset.variables['Power'][:50])
print ("Power units = ", dataset.variables['Power'].units)

print ("ChannelAssignment = ", dataset.variables['ChannelAssignment'][:50])
print ("ChannelAssignment units = ", dataset.variables['ChannelAssignment'].units)

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



