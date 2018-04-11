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




print ("WVOnline = ", dataset.variables['WVOnline'][:50])
print ("WVOnline units = ", dataset.variables['WVOnline'].units)

print ("WVOffline = ", dataset.variables['WVOffline'][:50])
print ("WVOffline units = ", dataset.variables['WVOffline'].units)

print ("HSRLCombined = ", dataset.variables['HSRLCombined'][:50])
print ("HSRLCombined units = ", dataset.variables['HSRLCombined'].units)

print ("HSRLMolecular = ", dataset.variables['HSRLMolecular'][:50])
print ("HSRLMolecular units = ", dataset.variables['HSRLMolecular'].units)

print ("ProfPerHist = ", dataset.variables['ProfPerHist'][:50])
print ("ProfPerHist units = ", dataset.variables['ProfPerHist'].units)

print ("CntsPerBin = ", dataset.variables['CntsPerBin'][:50])
print ("CntsPerBin units = ", dataset.variables['CntsPerBin'].units)

print ("NBins = ", dataset.variables['NBins'][:50])
print ("NBins units = ", dataset.variables['NBins'].units)

print ("WVOnlinePower = ", dataset.variables['WVOnlinePower'][:50])
print ("WVOnlinePower units = ", dataset.variables['WVOnlinePower'].units)

print ("WVOfflinePower = ", dataset.variables['WVOfflinePower'][:50])
print ("WVOfflinePower units = ", dataset.variables['WVOfflinePower'].units)

print ("HSRLPower = ", dataset.variables['HSRLPower'][:50])
print ("HSRLPower units = ", dataset.variables['HSRLPower'].units)

print ("WVOnlineLaserWavelength = ", dataset.variables['WVOnlineLaserWavelength'][:50])
print ("WVOnlineLaserWavelength units = ", dataset.variables['WVOnlineLaserWavelength'].units)

print ("WVOfflineLaserWavelength = ", dataset.variables['WVOfflineLaserWavelength'][:50])
print ("WVOfflineLaserWavelength units = ", dataset.variables['WVOfflineLaserWavelength'].units)

print ("HSRLLaserWavelength = ", dataset.variables['HSRLLaserWavelength'][:50])
print ("HSRLLaserWavelength units = ", dataset.variables['HSRLLaserWavelength'].units)

print ("WVOnlineLaserWaveDiff = ", dataset.variables['WVOnlineLaserWaveDiff'][:50])
print ("WVOnlineLaserWaveDiff units = ", dataset.variables['WVOnlineLaserWaveDiff'].units)

print ("WVOfflineLaserWaveDiff = ", dataset.variables['WVOfflineLaserWaveDiff'][:50])
print ("WVOfflineLaserWaveDiff units = ", dataset.variables['WVOfflineLaserWaveDiff'].units)

print ("HSRLLaserWaveDiff = ", dataset.variables['HSRLLaserWaveDiff'][:50])
print ("HSRLLaserWaveDiff units = ", dataset.variables['HSRLLaserWaveDiff'].units)

print ("WVOnlineLaserTempDesired = ", dataset.variables['WVOnlineLaserTempDesired'][:50])
print ("WVOnlineLaserTempDesired units = ", dataset.variables['WVOnlineLaserTempDesired'].units)

print ("WVOfflineLaserTempDesired = ", dataset.variables['WVOfflineLaserTempDesired'][:50])
print ("WVOfflineLaserTempDesired units = ", dataset.variables['WVOfflineLaserTempDesired'].units)

print ("HSRLLaserTempDesired = ", dataset.variables['HSRLLaserTempDesired'][:50])
print ("HSRLLaserTempDesired units = ", dataset.variables['HSRLLaserTempDesired'].units)

print ("WVOnlineLaserTempMeas = ", dataset.variables['WVOnlineLaserTempMeas'][:50])
print ("WVOnlineLaserTempMeas units = ", dataset.variables['WVOnlineLaserTempMeas'].units)

print ("WVOfflineLaserTempMeas = ", dataset.variables['WVOfflineLaserTempMeas'][:50])
print ("WVOfflineLaserTempMeas units = ", dataset.variables['WVOfflineLaserTempMeas'].units)

print ("HSRLLaserTempMeas = ", dataset.variables['HSRLLaserTempMeas'][:50])
print ("HSRLLaserTempMeas units = ", dataset.variables['HSRLLaserTempMeas'].units)

print ("WVOnlineLaserCurrent = ", dataset.variables['WVOnlineLaserCurrent'][:50])
print ("WVOnlineLaserCurrent units = ", dataset.variables['WVOnlineLaserCurrent'].units)

print ("WVOfflineLaserCurrent = ", dataset.variables['WVOfflineLaserCurrent'][:50])
print ("WVOfflineLaserCurrent units = ", dataset.variables['WVOfflineLaserCurrent'].units)

print ("HSRLLaserCurrent = ", dataset.variables['HSRLLaserCurrent'][:50])
print ("HSRLLaserCurrent units = ", dataset.variables['HSRLLaserCurrent'].units)

print ("WVEtalonTemperature = ", dataset.variables['WVEtalonTemperature'][:50])
print ("WVEtalonTemperature units = ", dataset.variables['WVEtalonTemperature'].units)

print ("WVEtalonTempDiff = ", dataset.variables['WVEtalonTempDiff'][:50])
print ("WVEtalonTempDiff units = ", dataset.variables['WVEtalonTempDiff'].units)

print ("HSRLEtalonTemperature = ", dataset.variables['HSRLEtalonTemperature'][:50])
print ("HSRLEtalonTemperature units = ", dataset.variables['HSRLEtalonTemperature'].units)

print ("HSRLEtalonTempDiff = ", dataset.variables['HSRLEtalonTempDiff'][:50])
print ("HSRLEtalonTempDiff units = ", dataset.variables['HSRLEtalonTempDiff'].units)

print ("WSTemperature = ", dataset.variables['WSTemperature'][:50])
print ("WSTemperature units = ", dataset.variables['WSTemperature'].units)

print ("WSRelHum = ", dataset.variables['WSRelHum'][:50])
print ("WSRelHum units = ", dataset.variables['WSRelHum'].units)

print ("WSPressure = ", dataset.variables['WSPressure'][:50])
print ("WSPressure units = ", dataset.variables['WSPressure'].units)

print ("WSAbsHum = ", dataset.variables['WSAbsHum'][:50])
print ("WSAbsHum units = ", dataset.variables['WSAbsHum'].units)

print ("WSAbsHum = ", dataset.variables['WSAbsHum'][:50])
print ("WSAbsHum units = ", dataset.variables['WSAbsHum'].units)

print ("range = ", dataset.variables['range'][:50])
print ("range units = ", dataset.variables['range'].units)

print ("volume_number = ", dataset.variables['volume_number'][:50])
#print ("volume_number units = ", dataset.variables['volume_number'].units)

print ("instrument_type = ", dataset.variables['instrument_type'][:50])
#print ("instrument_type units = ", dataset.variables['instrument_type'].units)

print ("time_coverage_start = ", dataset.variables['time_coverage_start'][:50])
#print ("time_coverage_start units = ", dataset.variables['time_coverage_start'].units)

print ("time_coverage_end = ", dataset.variables['time_coverage_end'][:50])
#print ("time_coverage_end units = ", dataset.variables['time_coverage_end'].units)

print ("latitude = ", dataset.variables['latitude'][:50])
print ("latitude units = ", dataset.variables['latitude'].units)

print ("longitude = ", dataset.variables['longitude'][:50])
print ("longitude units = ", dataset.variables['longitude'].units)

print ("altitude = ", dataset.variables['altitude'][:50])
print ("altitude units = ", dataset.variables['altitude'].units)

print ("sweep_number = ", dataset.variables['sweep_number'][:50])
#print ("sweep_number units = ", dataset.variables['sweep_number'].units)

print ("sweep_mode = ", dataset.variables['sweep_mode'][:50])
#print ("sweep_mode units = ", dataset.variables['sweep_mode'].units)

print ("fixed_angle = ", dataset.variables['fixed_angle'][:50])
print ("fixed_angle units = ", dataset.variables['fixed_angle'].units)

print ("sweep_start_ray_index = ", dataset.variables['sweep_start_ray_index'][:50])
#print ("sweep_start_ray_index units = ", dataset.variables['sweep_start_ray_index'].units)

print ("sweep_end_ray_index = ", dataset.variables['sweep_end_ray_index'][:50])
#print ("sweep_end_ray_index units = ", dataset.variables['sweep_end_ray_index'].units)

print ("azimuth = ", dataset.variables['azimuth'][:50])
print ("azimuth units = ", dataset.variables['azimuth'].units)

print ("elevation = ", dataset.variables['elevation'][:50])
print ("elevation units = ", dataset.variables['elevation'].units)

print ("heading = ", dataset.variables['heading'][:50])
print ("heading units = ", dataset.variables['heading'].units)

print ("roll = ", dataset.variables['roll'][:50])
print ("roll units = ", dataset.variables['roll'].units)

print ("pitch = ", dataset.variables['pitch'][:50])
print ("pitch units = ", dataset.variables['pitch'].units)

print ("drift = ", dataset.variables['drift'][:50])
print ("drift units = ", dataset.variables['drift'].units)

print ("rotation = ", dataset.variables['rotation'][:50])
print ("rotation units = ", dataset.variables['rotation'].units)

print ("tilt = ", dataset.variables['tilt'][:50])
print ("tilt units = ", dataset.variables['tilt'].units)




#print (" = ", dataset.variables[''][:50])
#print (" units = ", dataset.variables[''].units)




#odict_keys(['time', 'range', 'sweep', 'string_length'])
#<class 'netCDF4._netCDF4.Dimension'>: name = 'time', size = 1811

#odict_keys(['time', 'WVOnline', 'WVOffline', 'HSRLCombined', 'HSRLMolecular', 'ProfPerHist', 'CntsPerBin', 'NBins', 'WVOnlinePower', 'WVOfflinePower', 'HSRLPower', 'WVOnlineLaserWavelength', 'WVOfflineLaserWavelength', 'HSRLLaserWavelength', 'WVOnlineLaserWaveDiff', 'WVOfflineLaserWaveDiff', 'HSRLLaserWaveDiff', 'WVOnlineLaserTempDesired', 'WVOfflineLaserTempDesired', 'HSRLLaserTempDesired', 'WVOnlineLaserTempMeas', 'WVOfflineLaserTempMeas', 'HSRLLaserTempMeas', 'WVOnlineLaserCurrent', 'WVOfflineLaserCurrent', 'HSRLLaserCurrent', 'WVEtalonTemperature', 'WVEtalonTempDiff', 'HSRLEtalonTemperature', 'HSRLEtalonTempDiff', 'WSTemperature', 'WSRelHum', 'WSPressure', 'WSAbsHum', 'range', 'volume_number', 'instrument_type', 'time_coverage_start', 'time_coverage_end', 'latitude', 'longitude', 'altitude', 'sweep_number', 'sweep_mode', 'fixed_angle', 'sweep_start_ray_index', 'sweep_end_ray_index', 'azimuth', 'elevation', 'heading', 'roll', 'pitch', 'drift', 'rotation', 'tilt'])










