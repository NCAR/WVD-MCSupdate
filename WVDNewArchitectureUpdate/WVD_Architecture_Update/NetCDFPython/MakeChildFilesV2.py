# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# These functions are used to convert raw data from the MicroPulse DIAL systems
# to netcdf data. The information should be identical except for the following 
# cases:
#       1) Files where the data are jagged arrays instead of full are filled 
#          with a bad data marker (-1000000000) to make all rows the same size

import datetime
import os
import sys
import DataFileFunctions     as DFF
import NCARMCSFunctions      as NMF
import numpy                 as np
import SharedPythonFunctions as SPF

def ThermocoupleMap(Types):    
    Strings = []
    for Type in Types:
        if   Type == 0: String = "Unknown"
        elif Type == 1: String = "Empty"
        elif Type == 2: String = "OpticalBench"
        elif Type == 3: String = "HVACSource"
        elif Type == 4: String = "HVACReturn"
        elif Type == 5: String = "Window"
        elif Type == 6: String = "WindowHeaterFan"
        elif Type == 7: String = "WVEtalonHeatSink"
        elif Type == 8: String = "HSRLEtalonHeatSink"
        elif Type == 9: String = "HSRLOven"
        else:         	  String = "Unassigned"
        Strings.append(String)
    return Strings

#%%################################# General ##################################
#def processGeneral()
    

def processClock(FileName,NetCDFOutputPath,Header):
    print("Making Clock Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    FileData = [' '.join(Line).split() for Line in DFF.ReadAndPadTextFile(FileName)]
    VarData = np.array(FileData).astype(np.float) 
    # Defining file attributes
    FileType              = 'Clock'
    FileDescription       = 'Master clock  data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[:,1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','PulseDelay','GateDelay','DutyCycle','SwitchRate','PulseDuration','PRF','RiseTime',\
                           'TSOA','Online','Offline','Gate']
    VariableColumn      = [0,9,10,11,12,13,14,15,4,5,6,7] # column in the data file to find these variables
    Transpose           = [False]*len(VariableColumn)
    VariableDimension   = [('time')]*len(VariableColumn)
    VariableType        = ['float'] + ['float32']*(len(VariableColumn)-1)
    VariableUnit        = ['Fractional Hours','MicroSeconds','MicroSeconds','Unitless','Hz','MicroSeconds','Hz','MicroSeconds',\
                           'Unitless','Unitless','Unitless','Unitless']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Time from the clock trigger to the laser pulse trigger',
                           'Time from the clock trigger to the gate pulse trigger',
                           'Duty cyle of the offline pulse (0 = always off, 1 = always on)',
                           'Rate of switching from online to offline',
                           'The duration of the laser pulse',
                           'Pulse repetition frequency',
                           'Rise time of the opto-electric switches',
                           'Operating mode of the TSOA (0 = Operations, 1 = Off)',
                           'Operating mode of the Online 1x1 switch (0 = Operations, 1 = Open, 2 = Closed, 3 = Receiver Scan)',
                           'Operating mode of the Offline 1x1 switch (0 = Operations, 1 = Open, 2 = Closed, 3 = Receiver Scan)',
                           'Operating mode of the detector gate (0 = Operations, 1 = Off)']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
#%%############################### Container ################################## 
def processContainer(FileName,NetCDFOutputPath,Header):
    print("Making Container Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','f','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'Container'
    FileDescription       = 'Container data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','FunctionType','LastCheckin','CQueueEl','RQueueEl','Status']
    VariableColumn      = [1,0,2,3,4,5] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float64','U','float32','float32','float64','float32']
    VariableUnit        = ['float','U','float','float32','float32','b']
    VariableUnit        = ['Fractional Hours','Unitless','Fractional Hours','Unitless','Unitless','Unitless']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Type of function reporting status',
                           'Last time a particular function reported a status',
                           'Number of elements currently reported in the child command queue',
                           'Number of elements currently reported in the child response queue',
                           'Status of the child. Bit tested with the order: Child exiting, Child COmmanded Stop, Child Responding']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)

#%%################################# Etalon ################################### 
def processEtalons(FileName,NetCDFOutputPath,Header):
    print("Making Etalon Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','b','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'Etalon'
    FileDescription       = 'Etalon data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','EtalonNum','Temperature','TempDiff','IsLocked']
    VariableColumn      = [4,0,1,2,3] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','U','float32','float32','b']
    VariableUnit        = ['Fractional Hours','Unitless','Celcius','Celcius','Unitless']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Name of the etalon that was being checked (Choices are: WVEtalon, HSRLEtalon, O2Etalon, or unknown)',
                           'Measured temperature of the etalon from the Thor 8000 thermo-electric cooler',
                           'Temperature difference of etalon measured - desired setpoint',
                           'Boolean value defining if the operational software considered the temperature difference low enough to be locked']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
                        
#%%############################### Etalon Scan ################################# 
def processEtalonScan(FileName,NetCDFOutputPath,Header):
    print("Making Etalon Scan Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','b','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'ReceiverScanEtalon'
    FileDescription       = 'Etalon scan data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','EtalonNum','Temperature','TempDiff','IsLocked']
    VariableColumn      = [4,0,1,2,3] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','U','float32','float32','b']
    VariableUnit        = ['Fractional Hours','Unitless','Celcius','Celcius','Unitless']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Name of the etalon that was being checked (Choices are: WVEtalon, HSRLEtalon, O2Etalon, or unknown)',
                           'Measured temperature of the etalon from the Thor 8000 thermo-electric cooler',
                           'Temperature difference of etalon measured - desired setpoint',
                           'Boolean value defining if the operational software considered the temperature difference low enough to be locked']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)                        
    
#%%############################## Housekeeping ################################ 
def processHK(FileName,NetCDFOutputPath,Header):
    print("Making Housekeeping Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float)    
    # Defining file attributes
    FileType              = 'HKeep'
    FileDescription       = 'Housekeeping data file: Thermocouples monitoring internal temperature of container'
    FileDimensionNames    = ['time', 'nSensors']
    FileDimensionSize     = [len(VarData[:,1]), len(VarData[1,:])-1]
    # Defining variable descriptions to be written
    VariableName        = ['time','Temperature']
    VariableColumn      = [0,list(np.asarray(range(len(VarData[1,:])-1))+1)] # column in the data file to find these variables
    Transpose           = [False,True]
    VariableDimension   = [('time'),('nSensors','time')]
    VariableType        = ['float','float32']
    VariableUnit        = ['Fractional Hours','Celcius']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Temperature at various points within the container']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         , Transpose         ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    
def processHKV2(FileName,NetCDFOutputPath,Header):
    BitsPerLocation  = 4
    print("Making HousekeepingV2 Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float)  
    # Determining the location of the thermocouples
    MaxThermocouples = len(VarData[1,:])-1
    LocString = '{:'+str(MaxThermocouples*BitsPerLocation)+'b}'
    LocString = LocString.format(int(FileName.split('_')[-4])).replace(' ','0')
    Locations = ThermocoupleMap([int(LocString[I*BitsPerLocation:I*BitsPerLocation+BitsPerLocation],2) for I in list(range(MaxThermocouples))])
    Locations.reverse()
    Locations = np.array(Locations).astype(np.str)   
    # Defining file attributes
    FileType              = 'HKeep'
    FileDescription       = 'Housekeeping data file: Thermocouples monitoring internal temperature of container'
    FileDimensionNames    = ['time', 'nSensors','nSensorLabels']
    FileDimensionSize     = [len(VarData[:,1]), MaxThermocouples, len(Locations)]
    # Pushing Thermocouple locations into data file structure
    A = list(np.asarray(range(len(VarData[1,:])-1))+1)
    VarData = [VarData[:,0],np.transpose(VarData[:,A]),Locations]
    # Defining variable descriptions to be written
    VariableName        = ['time','Temperature','ThermocoupleLocations']
    VariableColumn      = [0,1,2] # column in the data file to find these variables
    Transpose           = [False,False,False]
    VariableDimension   = [('time'),('nSensors','time'),('nSensorLabels')]
    VariableType        = ['float','float32','U']
    VariableUnit        = ['Fractional Hours','Celcius','Unitless']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Temperature at various points within the container',
                           'Location of the thermocouples']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         , Transpose         ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)


    
#%%################################# Etalon ################################### 
def processHumidity(FileName,NetCDFOutputPath,Header):
    print("Making Humidity Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'Humidity'
    FileDescription       = 'Humidity sensor data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[:,1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','InternalTemperature','ExternalTemperature','DewPoint','RelativeHumidity']
    VariableColumn      = [4,0,1,3,2] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','float32','float32','float32','float32']
    VariableUnit        = ['Fractional Hours','Celcius','Celcius','Celcius','%']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Temperature measured by the humidity sensor base station',
                           'Temperature measured by the humidity sensor head',
                           'Dew point temperature measured by the humidity sensor head',
                           'The relative humidity measured by the humidity sensor head']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)

#%%############################# Laser Locking ################################ 
def processLL(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making LL Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','b','f','f','f','f','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'LL'
    FileDescription       = 'Laser Locking data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','LaserName','Wavelength','WaveDiff','IsLocked','TempDesired','TempMeas','Current','SeedPower']
    VariableColumn      = [7,0,1,2,3,4,5,6,9] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','U','float32','float32','b','float32','float32','float32','float32']
    VariableUnit        = ['Fractional Hours','Unitless','nm','nm','Unitless','Celcius','Celcius','Amp','dBm']    
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Name of the laser that was being locked (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or unknown)',
                           'Wavelength of the seed laser measured by the wavemeter (reference to vacuum)',
                           'Wavelength of the seed laser measured by the wavemeter (reference to vacuum) - Desired wavelenth',
                           'Boolean value defining if the operational software considered the wavelength difference low enough to be locked',
                           'Laser temperature setpoint',
                           'Measured laser temperature from the Thor 8000 diode thermo-electric cooler',
                           'Measured laser current from the Thor 8000 diode laser controller',
                           'Power of the seed laser measured by the wavemeter']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)

#%%############################# Laser Locking ################################ 
def processLaserScan(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making Laser Scan Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a padded array as needed 
    DataType = ['str','str','str','str','f','f','f','f','f','str'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'ReceiverScanLaser'
    FileDescription       = 'Laser Scanning data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','LaserName','TempDesired','TempMeas','Current']
    VariableColumn      = [7,0,4,5,6] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','U','float32','float32','float32']
    VariableUnit        = ['Fractional Hours','Unitless','Celcius','Celcius','Amp']    
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Name of the laser that was being locked (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or unknown)',
                           'Laser temperature setpoint',
                           'Measured laser temperature from the Thor 8000 diode thermo-electric cooler',
                           'Measured laser current from the Thor 8000 diode laser controller']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)

#%%################################ MCS Data ##################################
def processMCSData(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making MCS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','str','f','f','f','f','f','f','f','f','Pass'] 
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPhotonCountFile(FileName)),DataType,False)
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'MCS'
        FileDescription       = 'Multi-channel scalar (MCS) photon count histogram data file'
        FileDimensionNames    = ['time','nBins','nChannels']
        FileDimensionSize     = [len(VarData[9]),len(VarData[3][0]),len(VarData[1])]
        # Defining variable descriptions to be written
        VariableName        = ['time','ProfilesPerHist','Channel','nsPerBin','NBins','Data','ChannelAssignment','RTime','FrameCount','SyncSource']
        VariableColumn      = [9,6,0,2,5,3,1,7,4,8] # column in the data file to find these variables
        Transpose           = [False,False,False,False,False,True,False,False,False,False]
        VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('nBins','time'),('nChannels'),('time'),('time'),('time')]
        VariableType        = ['float','float32','float32','float32','float32','float32','U','float32','float32','float32']
        VariableUnit        = ['Fractional Hours','Number of shots','Unitless','ns','Unitless','photons','unitless','ms','Unitless','Unitless']
        VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                               'Number of laser shots summed to create a single verticle histogram',
                               'MCS hardware channel number for each measurement. There are 8 real valued inputs and 4 extra channels resulting from demuxing',
                               'The width of each altitude bin',
                               'Number of sequential altitude bins measured for each histogram profile',
                               'A profile containing the number of photons returned in each of the sequential altitude bin',
                               'String value defining what hardware was connected to the MCS digital detection channels (Choices are: WVOnline, WVOffline, HSRLCombined, HSRLMolecular, O2Online, O2Offline, or Unassigned)',
                               'Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)',
                               'Number of the data frame sent by the MCS. This should be sequential and incrimenting by 1 each new measurement',
                               'The number of the input sync source used on the MCS. There are 3 availible numbered 0-2.']
        # Writing the netcdf file 
        DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         , Transpose         ,
                            FileDate         ,FileDescription,FileDimensionNames ,
                            FileDimensionSize,FileTime       ,FileType           , 
                            VarData          ,VariableColumn ,VariableDescription,
                            VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    else:                # Some error is reported
        print('An error occured when reading the data file.')

#%%################################ MCS Data ##################################
def processMCSDataV2(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making MCS V2 Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','str','f','f','f','f','f','f','f','f','Pass'] 
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPhotonCountFileV2(FileName)),DataType,False)
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'MCS'
        FileDescription       = 'Multi-channel scalar (MCS) photon count histogram data file'
        FileDimensionNames    = ['time','nBins','nChannels']
        FileDimensionSize     = [len(VarData[9]),len(VarData[3][0]),len(VarData[1])]
        # Defining variable descriptions to be written
        VariableName        = ['time','ProfilesPerHist','Channel','nsPerBin','NBins','Data','ChannelAssignment','RTime','FrameCount','SyncSource']
        VariableColumn      = [9,6,0,2,5,3,1,7,4,8] # column in the data file to find these variables
        Transpose           = [False,False,False,False,False,True,False,False,False,False]
        VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('nBins','time'),('nChannels'),('time'),('time'),('time')]
        VariableType        = ['float','float32','float32','float32','float32','float32','U','float32','float32','float32']
        VariableUnit        = ['Fractional Hours','Number of shots','Unitless','ns','Unitless','photons','unitless','ms','Unitless','Unitless']
        VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                               'Number of laser shots summed to create a single verticle histogram',
                               'MCS hardware channel number for each measurement. There are 8 real valued inputs and 4 extra channels resulting from demuxing',
                               'The width of each altitude bin',
                               'Number of sequential altitude bins measured for each histogram profile',
                               'A profile containing the number of photons returned in each of the sequential altitude bin',
                               'String value defining what hardware was connected to the MCS digital detection channels (Choices are: WVOnline, WVOffline, HSRLCombined, HSRLMolecular, O2Online, O2Offline, or Unassigned)',
                               'Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)',
                               'Number of the data frame sent by the MCS. This should be sequential and incrimenting by 1 each new measurement',
                               'The number of the input sync source used on the MCS. There are 3 availible numbered 0-2.']
        # Writing the netcdf file 
        DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         , Transpose         ,
                            FileDate         ,FileDescription,FileDimensionNames ,
                            FileDimensionSize,FileTime       ,FileType           , 
                            VarData          ,VariableColumn ,VariableDescription,
                            VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    else:                # Some error is reported
        print('An error occured when reading the data file.')
        
#%%################################ MCS Data ##################################
def processMCSScanDataV2(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making MCS V2 Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','str','f','f','f','f','f','f','f','f','Pass'] 
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPhotonCountFileV2(FileName)),DataType,False)
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'ReceiverScanMCS'
        FileDescription       = 'Multi-channel scalar (MCS) photon count histogram data file'
        FileDimensionNames    = ['time','nBins','nChannels']
        FileDimensionSize     = [len(VarData[9]),len(VarData[3][0]),len(VarData[1])]
        # Defining variable descriptions to be written
        VariableName        = ['time','ProfilesPerHist','Channel','nsPerBin','NBins','Data','ChannelAssignment','RTime','FrameCount','SyncSource']
        VariableColumn      = [9,6,0,2,5,3,1,7,4,8] # column in the data file to find these variables
        Transpose           = [False,False,False,False,False,True,False,False,False,False]
        VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('nBins','time'),('nChannels'),('time'),('time'),('time')]
        VariableType        = ['float','float32','float32','float32','float32','float32','U','float32','float32','float32']
        VariableUnit        = ['Fractional Hours','Number of shots','Unitless','ns','Unitless','photons','unitless','ms','Unitless','Unitless']
        VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                               'Number of laser shots summed to create a single verticle histogram',
                               'MCS hardware channel number for each measurement. There are 8 real valued inputs and 4 extra channels resulting from demuxing',
                               'The width of each altitude bin',
                               'Number of sequential altitude bins measured for each histogram profile',
                               'A profile containing the number of photons returned in each of the sequential altitude bin',
                               'String value defining what hardware was connected to the MCS digital detection channels (Choices are: WVOnline, WVOffline, HSRLCombined, HSRLMolecular, O2Online, O2Offline, or Unassigned)',
                               'Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)',
                               'Number of the data frame sent by the MCS. This should be sequential and incrimenting by 1 each new measurement',
                               'The number of the input sync source used on the MCS. There are 3 availible numbered 0-2.']
        # Writing the netcdf file 
        DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         , Transpose         ,
                            FileDate         ,FileDescription,FileDimensionNames ,
                            FileDimensionSize,FileTime       ,FileType           , 
                            VarData          ,VariableColumn ,VariableDescription,
                            VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    else:                # Some error is reported
        print('An error occured when reading the data file.')
        
#%%############################### MCS Power ##################################
def processMCSPower(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making MCS Power Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','f','f','f','f','str','Pass']   
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPowerFile(FileName)),DataType,False)  
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'Power'
        FileDescription       = 'Multi-channel scalar (MCS) power monitor data file'
        FileDimensionNames    = ['time','nChannels']
        FileDimensionSize     = [len(VarData[4]),len(VarData[2])]
        # Defining variable descriptions to be written
        VariableName        = ['time','RTime','Power','ChannelAssignment','AccumEx','Demux']
        VariableColumn      = [4,3,2,5,0,1] # column in the data file to find these variables
        Transpose           = [False,False,False,False,False,False]
        VariableDimension   = [('time'),('time'),('nChannels','time'),('nChannels'),('nChannels','time'),('nChannels','time')]
        VariableType        = ['float','float32','float32','U','float32','float32']
        VariableUnit        = ['Fractional Hours','Unitless','Pin count','Unitless','Unitless','Unitless']
        VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                               'Raw pin count from the MCS analog detectors (must be converted to power by _______)',
                               'String value defining what hardware was connected to each of the 12 MCS analog detection channels (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or Unknown)',
                               'Relative time counter, 20 bit time value relative to the most recent system reset (or time reset)',
                               'Number of shots to accumulate to average out the power (2^#)',
                               'The source of the demuxing signal used to split power measurements']
        # Writing the netcdf file 
        DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                            FileDate         ,FileDescription,FileDimensionNames ,
                            FileDimensionSize,FileTime       ,FileType           , 
                            VarData          ,VariableColumn ,VariableDescription,
                            VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    else:                # Some error is reported
        print('An error occured when reading the data file.')
        
#%%############################### MCS Power ##################################
def processMCSPowerV2(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making MCS V2 Power Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','f','f','f','f','str','Pass']   
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPowerFileV2(FileName)),DataType,False)  
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'Power'
        FileDescription       = 'Multi-channel scalar (MCS) power monitor data file'
        FileDimensionNames    = ['time','nChannels']
        FileDimensionSize     = [len(VarData[4]),len(VarData[2])]
        # Defining variable descriptions to be written
        VariableName        = ['time','RTime','Power','ChannelAssignment','AccumEx','Demux']
        VariableColumn      = [4,3,2,5,0,1] # column in the data file to find these variables
        Transpose           = [False,False,False,False,False,False]
        VariableDimension   = [('time'),('time'),('nChannels','time'),('nChannels'),('nChannels','time'),('nChannels','time')]
        VariableType        = ['float','float32','float32','U','float32','float32']
        VariableUnit        = ['Fractional Hours','Unitless','Pin count','Unitless','Unitless','Unitless']
        VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                               'Raw pin count from the MCS analog detectors (must be converted to power by _______)',
                               'String value defining what hardware was connected to each of the 12 MCS analog detection channels (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or Unknown)',
                               'Relative time counter, 20 bit time value relative to the most recent system reset (or time reset)',
                               'Number of shots to accumulate to average out the power (2^#)',
                               'The source of the demuxing signal used to split power measurements']
        # Writing the netcdf file 
        DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                            FileDate         ,FileDescription,FileDimensionNames ,
                            FileDimensionSize,FileTime       ,FileType           , 
                            VarData          ,VariableColumn ,VariableDescription,
                            VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    else:                # Some error is reported
        print('An error occured when reading the data file.')

#%%################################## UPS #####################################
def processUPS(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making UPS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)   
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'UPS'
    FileDescription       = 'UPS data file'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[:,1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','BatteryNominal','BatteryReplace','BatteryInUse','BatteryLow','BatteryCapacity','BatteryTimeLeft','UPSTemperature','HoursOnBattery']
    VariableColumn      = [0,1,2,3,4,5,6,7,8] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','b','b','b','b','float32','float32','float32','float32']
    VariableUnit        = ['Fractional Hours','unitless','unitless','unitless','unitless','percent','hours','Celcius','hours']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Boolean for Battery Nominal (1 = nominal, 0 = abnormal)',
                           'Boolean for Battery Replace (1 = replace, 0 = okay for now)',
                           'Boolean for if UPS is on Battery (1 = wall power, 0 = on battery)',
                           'Boolean for if battery is low (1 = okay, 0 = low)',
                           'Battery capacity remaining',
                           'Hours of runtime remaining on batteries',
                           'UPS temperature',
                           'Hours on battery since last on wall power']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)

#%%############################### Wavemeter ##################################               
def processWavemeter(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making Wavemeter Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)   
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'ReceiverScanWavemeter'
    FileDescription       = 'Wavemeter raw data'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[:,1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','Wavelength','SeedPower']
    VariableColumn      = [0,3,4] # column in the data file to find these variables
    Transpose           = [False,False,False]
    VariableDimension   = [('time'),('time'),('time')]
    VariableType        = ['float','float32','float32']
    VariableUnit        = ['Fractional Hours','nm','dBm']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Wavelength of the seed laser measured by the wavemeter (reference to vacuum)',
                           'Power of the seed laser measured by the wavemeter']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
                           
#%%############################ Weather Station ###############################               
def processWS(FileName,NetCDFOutputPath,Header):
    # Printing text to the console to tell the user what is happening
    print("Making WS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)   
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'WS'
    FileDescription       = 'Weather Station data file: taken at surface level'
    FileDimensionNames    = ['time']
    FileDimensionSize     = [len(VarData[:,1])]
    # Defining variable descriptions to be written
    VariableName        = ['time','Temperature','RelHum','Pressure','AbsHum']
    VariableColumn      = [4,0,1,2,3] # column in the data file to find these variables
    Transpose           = [False,False,False,False,False]
    VariableDimension   = [('time'),('time'),('time'),('time'),('time')]
    VariableType        = ['float','float32','float32','float32','float32']
    VariableUnit        = ['Fractional Hours','Celcius','%','Millibar','g/m^3']
    VariableDescription = ['The time of collected data in UTC hours from the start of the day',
                           'Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)',
                           'Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)',
                           'Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)',
                           'Atmospheric water vapor mixing ratio measured by the weather station at ground level (actual height is 2 meters at the top of the container)']
    # Writing the netcdf file 
    DFF.WriteNetCDFFile(NetCDFOutputPath ,Header         ,Transpose          ,
                        FileDate         ,FileDescription,FileDimensionNames ,
                        FileDimensionSize,FileTime       ,FileType           , 
                        VarData          ,VariableColumn ,VariableDescription,
                        VariableDimension,VariableName   , VariableType      , VariableUnit,MPDNum)
    
#%%
def makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,Header):
    # Defining the files to be written
    PathTypes = ['UPS' ,'Housekeeping'  ,'WeatherStation','LaserLocking','LaserLocking','MCS'        ,'MCS'         ,'MCS'      ,'MCS'       ,'HumiditySensor','ReceiverScan','ReceiverScan','ReceiverScan' ,'ReceiverScan'  ,'QuantumComposer'   ,'Container']    
    FileTypes = ['UPS' ,'HousekeepingV2','WeatherStation','LaserLocking','Etalon'      ,'TestingData','TestingPower','MCSDataV2','MCSPowerV2','Humidity'      ,'MCSDataV2'   ,'Wavemeter'   ,'LaserScanData','EtalonScanData','QuantumComposerOps','ContainerLogging']
    FileExts  = ['.txt','.txt'          ,'.txt'          ,'.txt'        ,'.txt'        ,'.bin'       ,'.bin'        ,'.bin'     ,'.bin'      ,'.txt'          ,'.bin'        ,'.txt'        ,'.txt'         ,'.txt'          ,'.txt'              ,'.txt']
#    PathTypes = ['Housekeeping'   ]    
#    FileTypes = ['HousekeepingV2']
#    FileExts  = ['.txt']
    # Looping over all the file types of interest
    for PathType,FileType,FileExt in zip(PathTypes, FileTypes,FileExts): 
        # Where2FindData = os.path.join(sys.argv[1],PathType,FileType)
        Where2FindData = os.path.join(sys.argv[1],'Data',PathType)
        if os.path.isdir(Where2FindData):
            # Making a list of possible files
            FileList = SPF.getFiles(Where2FindData , FileType, FileExt, ThenDate, ThenTime)
            FileList.sort()
            # Looping over all the files found
            for File in FileList: # read in file, process into NetCDF, and write out file
                try:    # trying to process each file by type
                    if   FileType == 'ContainerLogging':   processContainer(File,NetCDFPath,Header)
                    elif FileType == 'Etalon':             processEtalons(File,NetCDFPath,Header)
                    elif FileType == 'EtalonScanData':     processEtalonScan(File,NetCDFPath,Header)
                    elif FileType == 'Housekeeping':       processHK(File,NetCDFPath,Header)
                    elif FileType == 'HousekeepingV2':     processHKV2(File,NetCDFPath,Header)
                    elif FileType == 'Humidity':           processHumidity(File,NetCDFPath,Header)
                    elif FileType == 'LaserLocking':       processLL(File,NetCDFPath,Header)
                    elif FileType == 'LaserScanData':      processLaserScan(File,NetCDFPath,Header)
                    elif FileType == 'MCSData':            processMCSData(File,NetCDFPath,Header)
                    elif FileType == 'MCSPower':           processMCSPower(File,NetCDFPath,Header)
                    elif FileType == 'QuantumComposerOps': processClock(File,NetCDFPath,Header)
                    elif FileType == 'UPS':                processUPS(File,NetCDFPath,Header)
                    elif FileType == 'TestingData' or FileType == 'MCSDataV2':    
                    	if    PathType == 'MCS':              processMCSDataV2(File,NetCDFPath,Header)
                    	elif  PathType == 'ReceiverScan':     processMCSScanDataV2(File,NetCDFPath,Header)
                    elif FileType == 'TestingPower' or FileType == 'MCSPowerV2':   
                    	processMCSPowerV2(File,NetCDFPath,Header)
                    elif FileType == 'Wavemeter':          processWavemeter(File,NetCDFPath,Header)
                    elif FileType == 'WeatherStation':     processWS(File,NetCDFPath,Header)
                    elif FileType == '':                   12
                except:   # Logging the failure of any file to write
                    writeString = 'WARNING: Failure to process ' + FileType + ' data - ' + \
                                   FileType + ' file = ' + str(File) + ' - ' + str(NowTime) + \
                                   '\n' + str(sys.exc_info()[0]) + '\n\n'
                    print(writeString)