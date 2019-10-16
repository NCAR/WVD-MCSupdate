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

#%%################################# Etalon ################################### 
def processEtalons(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    print("Making Etalon Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','b','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'Etalonsample'
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
                        VariableDimension,VariableName   , VariableType      , VariableUnit)
    
#%%############################## Housekeeping ################################ 
def processHK(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    print("Making Housekeeping Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float)    
    # Defining file attributes
    FileType              = 'HKeepsample'
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
                        VariableDimension,VariableName   , VariableType      , VariableUnit)

#%%############################# Laser Locking ################################ 
def processLL(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    # Printing text to the console to tell the user what is happening
    print("Making LL Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a padded array as needed 
    DataType = ['str','f','f','b','f','f','f','f','f','f'] 
    VarData = DFF.ConvertAlphaNumericFile(DFF.ReadAndPadTextFile(FileName),DataType)
    # Defining file attributes
    FileType              = 'LLsample'
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
                        VariableDimension,VariableName   , VariableType      , VariableUnit)

#%%################################ MCS Data ##################################
def processMCSData(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    # Printing text to the console to tell the user what is happening
    print("Making MCS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','str','f','f','f','f','f','f','f','f','Pass'] 
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPhotonCountFile(FileName)),DataType,False)
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'MCSsample'
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
                            VariableDimension,VariableName   , VariableType      , VariableUnit)
    else:                # Some error is reported
        print('An error occured when reading the data file.')
        
#%%############################### MCS Power ##################################
def processMCSPower(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    # Printing text to the console to tell the user what is happening
    print("Making MCS Power Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True) 
    # Reading data file and returning a data array as needed 
    DataType = ['f','f','f','f','f','str','Pass']   
    VarData = DFF.ConvertAlphaNumericFile(list(NMF.ReadMCSPowerFile(FileName)),DataType,False)  
    # Checking to see if there were any file reading errors
    if not VarData[-1]:  # No error observed
        # Defining file attributes
        FileType              = 'Powsample'
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
                            VariableDimension,VariableName   , VariableType      , VariableUnit)
    else:                # Some error is reported
        print('An error occured when reading the data file.')
        
#%%################################## UPS #####################################
def processUPS(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    # Printing text to the console to tell the user what is happening
    print("Making UPS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True)   
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'UPSsample'
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
                        VariableDimension,VariableName   , VariableType      , VariableUnit)

#%%############################ Weather Station ###############################               
def processWS(FileName,NetCDFOutputPath,Header,NowDate,NowTime,LastTime):
    # Printing text to the console to tell the user what is happening
    print("Making WS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    (FileDate,FileTime) = DFF.FindFileDateAndTime(FileName,True)   
    # Reading data file and returning a padded array as needed  
    VarData = np.array(DFF.ReadAndPadTextFile(FileName)).astype(np.float) 
    # Defining file attributes
    FileType              = 'WSsample'
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
                        VariableDimension,VariableName   , VariableType      , VariableUnit)
    
##%%
def makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,Header):
    # Defining the files to be written
    PathTypes = ['UPS' ,'Housekeeping','WeatherStation','LaserLocking','LaserLocking','MCS'    ,'MCS'     ]    
    FileTypes = ['UPS' ,'Housekeeping','WeatherStation','LaserLocking','Etalon'      ,'MCSData','MCSPower']
    FileExts  = ['.txt','.txt'        ,'.txt'          ,'.txt'        ,'.txt'        ,'.bin'   ,'.bin'    ]
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
                    if   FileType == 'Etalon':         processEtalons(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'Housekeeping':   processHK(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'LaserLocking':   processLL(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'MCSData':        processMCSData(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'MCSPower':       processMCSPower(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'UPS':            processUPS(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                    elif FileType == 'WeatherStation': processWS(File,NetCDFPath,Header,NowDate,NowTime,LastTime)
                except:   # Logging the failure of any file to write
                    writeString = 'WARNING: Failure to process ' + FileType + ' data - ' + \
                                   FileType + ' file = ' + str(File) + ' - ' + str(NowTime) + \
                                   '\n' + str(sys.exc_info()[0]) + '\n\n'
                    print(writeString)