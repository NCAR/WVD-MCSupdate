# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research

import numpy as np
import copy
from   collections import defaultdict

#%% Defining the column structure of alpha-numeric data files
def DefineFileStructure(Type):
    # Defining the raw data file format for alpha-numeric files 
    FileType = {'Container':      ['str','f','f','f','f','f'], 
                'Etalon':         ['str','f','f','b','f','f'],
                'LL':             ['str','f','f','b','f','f','f','f','f','f'],
                'LaserScan':      ['str','str','str','str','f','f','f','f','f','str'],
                'MCS':            ['f','str','f','f','f','f','f','f','f','f','Pass'],
                'Power':          ['f','f','f','f','f','str','Pass']}
    # Defining variables that have the same file type as others
    FileType['EtalonScan'] = copy.deepcopy(FileType['Etalon'])
    FileType['MCSV2']      = copy.deepcopy(FileType['MCS'])
    FileType['MCSScanV2']  = copy.deepcopy(FileType['MCS'])
    FileType['PowerV2']    = copy.deepcopy(FileType['Power'])
    return(FileType[Type])
#%% Defining the data type map
def DefineDataTypeMap():
    return({'str': np.str,'b': np.bool,'Pass':'Pass', 
            'float': np.float,'float32':np.float,'f':np.float})
#%% Defining maps for placement of measurement elements (defined in labview)
def DefineCurrentMap():  
    # Defining known locations
    return({0:"Unknown",1:"Empty",2: "SystemInput",3: "HVAC",
            4:"WallHeaters",5:"WindowHeaterFan",6:"WallPowerStrip"})
def DefineThermocoupleMap():  
    # Defining known locations
    return({0:"Unknown"   ,1:"Empty" ,2:"OpticalBench"   ,3:"HVACSource", 
            4:"HVACReturn",5:"Window",6:"WindowHeaterFan",7:"WVEtalonHeatSink",
            8:"HSRLEtalonHeatSink",9:"HSRLOven"})
#%% Defining maps for laser and detector channels (defined in labview)
def MCSPowerMapV2(Type):
    MCSPowerMap = {1:'Unknown',2:'WVOnline',3:'WVOffline',4:'O2Online',5:'O2Offline',6:'HSRL'}
    MCSPowerMap = defaultdict(lambda:'Unassigned',MCSPowerMap)
    return MCSPowerMap[Type]

def MCSPhotonCountMapV2(Type):
    MCSMap = {1:'Unknown',
              2:'WVOnline',3:'WVOnlineLow',4:'WVOffline',5:'WVOfflineLow',                      # WV DIAL
              6:'O2Online',7:'O2OnlineLow',8:'O2Offline',9:'O2OfflineLow',                      # O2 DIAL
              10:'O2OnlineMol',11:'O2OnlineMolLow',12:'O2OnlineComb',13:'O2OnlineCombLow',      # O2 Online HSRL/DIAL
              14:'O2OfflineMol',15:'O2OfflineMolLow',16:'O2OfflineComb',17:'O2OfflineCombLow',  # O2 Offline HSRL/DIAL
              18:'HSRLMol',19:'HSRLMolLow',20:'HSRLCombined',21:'HSRLCombinedLow'}              # Standalone HSRL
    MCSMap = defaultdict(lambda:'Unassigned',MCSMap)
    return MCSMap[Type]
#%% Defining all of the information to be written into netcdf files
def DefineNetCDFFileAttributes(ArrayData=None,List1d=None,List2d=None):
    # Checking for input data and padding with junk as needed
    ArrayData = np.empty((2,3))             if ArrayData is None else ArrayData
    List1d = [[1,1],[2,2],[3,3],[4,4],[5,5],6]  if List1d is None else List1d
    List2d = [[[0]]*3 for i in range(10)]   if List2d is None else List2d 
    # Defining the file attributes as a nested dictonary
    FileAtributes = \
{'Clock':    {'FType':        'Clock',
              'FDescription': 'Master clock  data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(ArrayData[:,1])],
              'Transpose':    [False]*12,
              'VarName':      ['time','PulseDelay','GateDelay','DutyCycle','SwitchRate','PulseDuration','PRF','RiseTime','TSOA','Online','Offline','Gate'],
              'VarCol':       [0,9,10,11,12,13,14,15,4,5,6,7],
              'VarDim':       [('time')]*12,
              'VarType':      ['float'] + ['float32']*11,
              'VarUnit':      ['Fractional Hours','MicroSeconds','MicroSeconds','Unitless','Hz',
                               'MicroSeconds','Hz','MicroSeconds','Unitless','Unitless','Unitless','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
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
                               'Operating mode of the detector gate (0 = Operations, 1 = Off)']},               
'Container': {'FType':        'Container',
              'FDescription': 'Container data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(List1d[1])],
              'Transpose':    [False]*6,
              'VarName':      ['time','FunctionType','LastCheckin','CQueueEl','RQueueEl','Status'],
              'VarCol':       [1,0,2,3,4,5],
              'VarDim':       [('time')]*6,
              'VarType':      ['float','U','float','float32','float32','b'],
              'VarUnit':      ['Fractional Hours','Unitless','Fractional Hours','Unitless','Unitless','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Type of function reporting status',
                               'Last time a particular function reported a status',
                               'Number of elements currently reported in the child command queue',
                               'Number of elements currently reported in the child response queue',
                               'Status of the child. Bit tested with the order: Child exiting, Child COmmanded Stop, Child Responding']},
'Current':   {'FType':        'Current',
              'FDescription': 'Housekeeping data file: Current monitoring of major MPD elements',
              'FDimNames':    ['time', 'nSensors','nSensorLabels'],
              'FDimSize':     [len(List1d[0]),len(List1d[2]),len(List1d[2])],
              'Transpose':    [False]*3,
              'VarName':      ['time','Current','CurrentMonitorLocations'],
              'VarCol':       [0,1,2],
              'VarDim':       [('time'),('nSensors','time'),('nSensorLabels')],
              'VarType':      ['float','float32','U'],
              'VarUnit':      ['Fractional Hours','Amps','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Read current from measurement collars. Note: Must be multiplied by 2 to match Dranitz calibration.',
                               'Location of the thermocouples']},
'Etalon':    {'FType':        'Etalon',
              'FDescription': 'Etalon data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(List1d[1])],
              'Transpose':    [False]*5,
              'VarName':      ['time','EtalonNum','Temperature','TempDiff','IsLocked'],
              'VarCol':       [4,0,1,2,3],
              'VarDim':       [('time')]*5,
              'VarType':      ['float','U','float32','float32','b'],
              'VarUnit':      ['Fractional Hours','Unitless','Celcius','Celcius','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Name of the etalon that was being checked (Choices are: WVEtalon, HSRLEtalon, O2Etalon, or unknown)',
                               'Measured temperature of the etalon from the Thor 8000 thermo-electric cooler',
                               'Temperature difference of etalon measured - desired setpoint',
                               'Boolean value defining if the operational software considered the temperature difference low enough to be locked']},
'HK':        {'FType':        'HKeep',
              'FDescription': 'Housekeeping data file: Thermocouples monitoring internal temperature of container',
              'FDimNames':    ['time', 'nSensors'],
              'FDimSize':     [len(ArrayData[:,1]), len(ArrayData[1,:])-1],
              'Transpose':    [False,True],
              'VarName':      ['time','Temperature'],
              'VarCol':       [0,list(np.asarray(range(len(ArrayData)-1))+1)],
              'VarDim':       [('time'),('nSensors','time')],
              'VarType':      ['float','float32'],
              'VarUnit':      ['Fractional Hours','Celcius'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Temperature at various points within the container']},
'HKV2':      {'FType':        'HKeep',
              'FDescription': 'Housekeeping data file: Thermocouples monitoring internal temperature of container',
              'FDimNames':    ['time', 'nSensors','nSensorLabels'],
              'FDimSize':     [len(List1d[0]),len(List1d[2]),len(List1d[2])],
              'Transpose':    [False]*3,
              'VarName':      ['time','Temperature','ThermocoupleLocations'],
              'VarCol':       [0,1,2],
              'VarDim':       [('time'),('nSensors','time'),('nSensorLabels')],
              'VarType':      ['float','float32','U'],
              'VarUnit':      ['Fractional Hours','Celcius','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Temperature at various points within the container',
                               'Location of the thermocouples']},
'Humidity':  {'FType':        'Humidity',
              'FDescription': 'Humidity sensor data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(ArrayData[:,1])],
              'Transpose':    [False]*5,
              'VarName':      ['time','InternalTemperature','ExternalTemperature','DewPoint','RelativeHumidity'],
              'VarCol':       [4,0,1,3,2],
              'VarDim':       [('time')]*5,
              'VarType':      ['float','float32','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','Celcius','Celcius','Celcius','%'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Temperature measured by the humidity sensor base station',
                               'Temperature measured by the humidity sensor head',
                               'Dew point temperature measured by the humidity sensor head',
                               'The relative humidity measured by the humidity sensor head']},
'LL':        {'FType':        'LL',
              'FDescription': 'Laser Locking data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(List1d[1])],
              'Transpose':    [False]*9,
              'VarName':      ['time','LaserName','Wavelength','WaveDiff','IsLocked','TempDesired','TempMeas','Current','SeedPower'],
              'VarCol':       [7,0,1,2,3,4,5,6,9],
              'VarDim':       [('time')]*9,
              'VarType':      ['float','U','float32','float32','b','float32','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','Unitless','nm','nm','Unitless','Celcius','Celcius','Amp','dBm'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Name of the laser that was being locked (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or unknown)',
                               'Wavelength of the seed laser measured by the wavemeter (reference to vacuum)',
                               'Wavelength of the seed laser measured by the wavemeter (reference to vacuum) - Desired wavelenth',
                               'Boolean value defining if the operational software considered the wavelength difference low enough to be locked',
                               'Laser temperature setpoint',
                               'Measured laser temperature from the Thor 8000 diode thermo-electric cooler',
                               'Measured laser current from the Thor 8000 diode laser controller',
                               'Power of the seed laser measured by the wavemeter']},
'LaserScan': {'FType':        'ReceiverScanLaser',
              'FDescription': 'Laser Scanning data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(List1d[1])],
              'Transpose':    [False]*5,
              'VarName':      ['time','LaserName','TempDesired','TempMeas','Current'],
              'VarCol':       [7,0,4,5,6],
              'VarDim':       [('time')]*5,
              'VarType':      ['float','U','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','Unitless','Celcius','Celcius','Amp'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Name of the laser that was being locked (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or unknown)',
                               'Laser temperature setpoint',
                               'Measured laser temperature from the Thor 8000 diode thermo-electric cooler',
                               'Measured laser current from the Thor 8000 diode laser controller']},
'MCS':       {'FType':        'MCS',
              'FDescription': 'Multi-channel scalar (MCS) photon count histogram data file',
              'FDimNames':    ['time','nBins','nChannels'],
              'FDimSize':     [len(List2d[9]),len(List2d[3][0]),len(List2d[1])],
              'Transpose':    [False,False,False,False,False,True,False,False,False,False],
              'VarName':      ['time','ProfilesPerHist','Channel','nsPerBin','NBins','Data','ChannelAssignment','RTime','FrameCount','SyncSource'],
              'VarCol':       [9,6,0,2,5,3,1,7,4,8],
              'VarDim':       [('time'),('time'),('time'),('time'),('time'),('nBins','time'),('nChannels'),('time'),('time'),('time')],
              'VarType':      ['float','float32','float32','float32','float32','float32','U','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','Number of shots','Unitless','ns','Unitless','photons','unitless','ms','Unitless','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Number of laser shots summed to create a single verticle histogram',
                               'MCS hardware channel number for each measurement. There are 8 real valued inputs and 4 extra channels resulting from demuxing',
                               'The width of each altitude bin',
                               'Number of sequential altitude bins measured for each histogram profile',
                               'A profile containing the number of photons returned in each of the sequential altitude bin',
                               'String value defining what hardware was connected to the MCS digital detection channels (Choices are: WVOnline, WVOffline, HSRLCombined, HSRLMolecular, O2Online, O2Offline, or Unassigned)',
                               'Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)',
                               'Number of the data frame sent by the MCS. This should be sequential and incrimenting by 1 each new measurement',
                               'The number of the input sync source used on the MCS. There are 3 availible numbered 0-2.']},
'Power':     {'FType':        'Power',
              'FDescription': 'Multi-channel scalar (MCS) power monitor data file',
              'FDimNames':    ['time','nChannels'],
              'FDimSize':     [len(List1d[0]),len(List1d[1])],
              'Transpose':    [False]*6,
              'VarName':      ['time','RTime','Power','ChannelAssignment','AccumEx','Demux'],
              'VarCol':       [0,4,1,5,2,3],
              'VarDim':       [('time'),('time'),('nChannels','time'),('nChannels'),('nChannels','time'),('nChannels','time')],
              'VarType':      ['float','float32','float32','U','float32','float32'],
              'VarUnit':      ['Fractional Hours','Unitless','Pin count','Unitless','Unitless','Unitless'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Raw pin count from the MCS analog detectors (must be converted to power by _______)',
                               'String value defining what hardware was connected to each of the 12 MCS analog detection channels (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or Unknown)',
                               'Relative time counter, 20 bit time value relative to the most recent system reset (or time reset)',
                               'Number of shots to accumulate to average out the power (2^#)',
                               'The source of the demuxing signal used to split power measurements']},
'UPS':       {'FType':        'UPS',
              'FDescription': 'UPS data file',
              'FDimNames':    ['time'],
              'FDimSize':     [len(ArrayData[:,1])],
              'Transpose':    [False]*9,
              'VarName':      ['time','BatteryNominal','BatteryReplace','BatteryInUse','BatteryLow','BatteryCapacity','BatteryTimeLeft','UPSTemperature','HoursOnBattery'],
              'VarCol':       [0,1,2,3,4,5,6,7,8],
              'VarDim':       [('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time'),('time')],
              'VarType':      ['float','b','b','b','b','float32','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','unitless','unitless','unitless','unitless','percent','hours','Celcius','hours'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Boolean for Battery Nominal (1 = nominal, 0 = abnormal)',
                               'Boolean for Battery Replace (1 = replace, 0 = okay for now)',
                               'Boolean for if UPS is on Battery (1 = wall power, 0 = on battery)',
                               'Boolean for if battery is low (1 = okay, 0 = low)',
                               'Battery capacity remaining',
                               'Hours of runtime remaining on batteries',
                               'UPS temperature',
                               'Hours on battery since last on wall power']},
'Wavemeter': {'FType':        'ReceiverScanWavemeter',
              'FDescription': 'Wavemeter raw data',
              'FDimNames':    ['time'],
              'FDimSize':     [len(ArrayData[:,1])],
              'Transpose':    [False]*3,
              'VarName':      ['time','Wavelength','SeedPower'],
              'VarCol':       [0,3,4],
              'VarDim':       [('time'),('time'),('time')],
              'VarType':      ['float','float32','float32'],
              'VarUnit':      ['Fractional Hours','nm','dBm'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Wavelength of the seed laser measured by the wavemeter (reference to vacuum)',
                               'Power of the seed laser measured by the wavemeter']},
'WStation':  {'FType':        'WS',
              'FDescription': 'Weather Station data file: taken at surface level',
              'FDimNames':    ['time'],
              'FDimSize':     [len(ArrayData[:,1])],
              'Transpose':    [False]*5,
              'VarName':      ['time','Temperature','RelHum','Pressure','AbsHum'],
              'VarCol':       [4,0,1,2,3],
              'VarDim':       [('time'),('time'),('time'),('time'),('time')],
              'VarType':      ['float','float32','float32','float32','float32'],
              'VarUnit':      ['Fractional Hours','Celcius','%','Millibar','g/m^3'],
              'VarDescrip':   ['The time of collected data in UTC hours from the start of the day',
                               'Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)',
                               'Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)',
                               'Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)',
                               'Atmospheric water vapor mixing ratio measured by the weather station at ground level (actual height is 2 meters at the top of the container)']}
} 
    # Adding elements for the etalon scan 
    FileAtributes['EtalonScan'] = copy.deepcopy(FileAtributes['Etalon'])
    FileAtributes['EtalonScan']['FType'] ='ReceiverScanEtalon'
    FileAtributes['EtalonScan']['FDescription'] = 'Etalon scan data file'
    # Adding elements for the second version of the MCS data
    FileAtributes['MCSV2'] = copy.deepcopy(FileAtributes['MCS'])
    FileAtributes['MCSScanV2'] = copy.deepcopy(FileAtributes['MCS'])
    FileAtributes['MCSScanV2']['FType'] ='ReceiverScanMCS'
    FileAtributes['MCSScanV2']['FDescription'] = 'Multi-channel scalar (MCS) photon count histogram data file'
    FileAtributes['PowerV2'] = copy.deepcopy(FileAtributes['Power'])
    # Returning data for use elsewhere
    return(FileAtributes)
