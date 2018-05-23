#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [location to write files] [how many hours back in time to process]

import os
import sys
import time
import csv
import datetime
import struct
import binascii
import math
import shutil
import numpy as np
import numpy.ma as ma
from datetime import timedelta 
from netCDF4 import Dataset
from numpy import arange, dtype 
from copy import copy

import decimal
decimal.getcontext().rounding = decimal.ROUND_DOWN

#checks if a value is a number
def is_number(n):
    try:
        float(n) 
    except ValueError:
        return False
    return True

#makes sure a directory exists
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

#MCS data is in binary format while others are in txt format. That is why we need dataname (the beginning of the names of the files) and the data type (to ensure proper extention) 
def getFiles(DataPath, dataname, datatype, ThenDate, ThenTime):
    DayList = os.listdir(DataPath)
    FileList = [] # will hold list of files needing to be processed

    for day in DayList:
        TempFileList = os.listdir(os.path.join(DataPath,day))
        if float(day) == float(ThenDate):
            for file in TempFileList:
                if file[:len(dataname)] == dataname and file[-1*len(datatype):] == datatype:
                    if int(file[-1*len(datatype)-6:-1*len(datatype)])/10000 > ThenTime:
                        FileList.append(os.path.join(DataPath,day,file))
        elif float(day) > float(ThenDate):
            for file in TempFileList:
                if file[:len(dataname)] == dataname and file[-1*len(datatype):] == datatype:
                    FileList.append(os.path.join(DataPath,day,file))
    return FileList

# not being used, but keeping this function here in case we wish to use it in the future.
# copies entire directory recursivly overwriting whatever is there. 
# def recursive_overwrite(src, dest, ignore=None):
#    if os.path.isdir(src):
#        if not os.path.isdir(dest):
#            os.makedirs(dest)
#        files = os.listdir(src)
#        if ignore is not None:
#            ignored = ignore(src, files)
#        else:
#            ignored = set()
#        for f in files:
#            if f not in ignored:
#                recursive_overwrite(os.path.join(src, f), os.path.join(dest, f), 
#                                    ignore)
#    else:
#        shutil.copyfile(src, dest)

# reads in config file which hold information for headers of NetCDF files
def readHeaderInfo():
    with open(os.path.join(sys.argv[1],"ConfigureFiles","Configure_WVDIALPythonNetCDFHeader.txt")) as f:
        reader = csv.reader(f, delimiter="\t")
        header = list(reader)
        #print (header)
        return header

def FillVar(dataset, varName):
    var = dataset.variables[varName][:]
    varFill = []
    i=0
    for entry in var:
        varFill.append(var[i])
        i=i+1
    return varFill
            
def Fill2DVar(dataset, varName):
    var = dataset.variables[varName][:]
    localvar = []
    for array in var:
        localvar.append([])
        localvar[int(len(localvar)-1)]=array
    localvar = np.array(localvar).T.tolist()
    return localvar

def Write2ErrorFile(ErrorFile, writeString):
    ensure_dir(ErrorFile)
    fh = open(ErrorFile, "a")
    fh.write(writeString)
    print (writeString, file=sys.stderr)



# ----------------------- UPS ------------------
def processUPS(UPSfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making UPS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = UPSfile[-19:-11]
    fileTime = UPSfile[-10:-4]
    print (fileDate)
    print (fileTime)

    Timestamp = []
    BatteryNominal = []
    BatteryReplace = []
    BatteryInUse = []
    BatteryLow = []
    BatteryCapacity = []
    BatteryTimeLeft = []
    UPSTemperature = []
    HoursOnBattery = []

    with open(UPSfile) as f: # read in file,
        for line in f:
            linelist = line.split()
            if len(linelist) == 9:
                Timestamp.append(linelist[0])
                BatteryNominal.append(linelist[1])
                BatteryReplace.append(linelist[2])
                BatteryInUse.append(linelist[3])
                BatteryLow.append(linelist[4])
                BatteryCapacity.append(linelist[5])
                BatteryTimeLeft.append(linelist[6])
                UPSTemperature.append(linelist[7])
                HoursOnBattery.append(linelist[8])

    # make sure output path exists
    ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))

    place = os.path.join(LocalNetCDFOutputPath,fileDate,"UPSsample"+fileTime+".nc")
    UPSncfile = Dataset(place,'w')
    # timestamp defines the dimentions of variables
    UPSncfile.createDimension('time',len(Timestamp))

    # creates variables
    TimestampData = UPSncfile.createVariable('time',dtype('float').char,('time'))
    BatteryNominalData = UPSncfile.createVariable('BatteryNominal',dtype('float').char,('time'))
    BatteryReplaceData = UPSncfile.createVariable('BatteryReplace',dtype('float').char,('time'))
    BatteryInUseData = UPSncfile.createVariable('BatteryInUse',dtype('float').char,('time'))
    BatteryLowData = UPSncfile.createVariable('BatteryLow',dtype('float').char,('time'))
    BatteryCapacityData = UPSncfile.createVariable('BatteryCapacity',dtype('float').char,('time'))
    BatteryTimeLeftData = UPSncfile.createVariable('BatteryTimeLeft',dtype('float').char,('time'))
    UPSTemperatureData = UPSncfile.createVariable('UPSTemperature',dtype('float').char,('time'))
    HoursOnBatteryData = UPSncfile.createVariable('HoursOnBattery',dtype('float').char,('time'))

    #fills variables
    TimestampData[:] = Timestamp
    BatteryNominalData[:] = BatteryNominal
    BatteryReplaceData[:] = BatteryReplace
    BatteryInUseData[:] = BatteryInUse
    BatteryLowData[:] = BatteryLow
    BatteryCapacityData[:] = BatteryCapacity
    BatteryTimeLeftData[:] = BatteryTimeLeft
    UPSTemperatureData[:] = UPSTemperature
    HoursOnBatteryData[:] = HoursOnBattery

    # brief description of file
    UPSncfile.description = "UPS data file"
    # load up header information for file
    for entry in header:
        UPSncfile.setncattr(entry[0],entry[1])

    # give variables units
    TimestampData.units = "Fractional Hours"
    BatteryNominalData.units = "unitless"
    BatteryReplaceData.units = "unitless"
    BatteryInUseData.units = "unitless"
    BatteryLowData.units = "unitless"
    BatteryCapacityData.units = "percent"
    BatteryTimeLeftData.units = "hours"
    UPSTemperatureData.units = "Celcius"
    HoursOnBatteryData.units = "hours"

    # give variables descriptions
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    BatteryNominalData.description = "Boolean for Battery Nominal (1 = nominal, 0 = abnormal)"
    BatteryReplaceData.description = "Boolean for Battery Replace (1 = replace, 0 = okay for now)"
    BatteryInUseData.description = "Boolean for if UPS is on Battery (1 = wall power, 0 = on battery)"
    BatteryLowData.description = "Boolean for if battery is low (1 = okay, 0 = low)"
    BatteryCapacityData.description = "Battery capacity remaining"
    BatteryTimeLeftData.description = "Hours of runtime remaining on batteries"
    UPSTemperatureData.description = "UPS temperature"
    HoursOnBatteryData.description = "Hours on battery since last on wall power"

    # and finally close file
    UPSncfile.close()



# ----------------------- Housekeeping ------------------
def processHKeep(HKeepfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making HKeep Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = HKeepfile[-19:-11]
    fileTime = HKeepfile[-10:-4]
    print (fileDate)
    print (fileTime)

    Temperature = []
    Timestamp = []

    nSensors = 0

    with open(HKeepfile) as f: # read in file,
        for line in f:
            linelist = line.split()
            Timestamp.append(linelist[0])
            while len(Temperature) < len(linelist)-1: # the -1 is because one column is the timestamp
                Temperature.append([])
                nSensors = nSensors + 1
            for f in range(1,len(linelist)):
                Temperature[f-1].append(linelist[f])

    # make sure output path exists
    ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))

    place = os.path.join(LocalNetCDFOutputPath,fileDate,"HKeepsample"+fileTime+".nc")
    HKeepncfile = Dataset(place,'w')
    # timestamp defines the dimentions of variables
    HKeepncfile.createDimension('time',len(Timestamp))
    HKeepncfile.createDimension('nSensors',nSensors)

    # creates variables
    TimestampData = HKeepncfile.createVariable('time',dtype('float').char,('time'))
    TemperatureData = HKeepncfile.createVariable('Temperature',dtype('float').char,('nSensors','time'))

    #fills variables
    TimestampData[:] = Timestamp
    TemperatureData[:] = Temperature

    # brief description of file
    HKeepncfile.description = "Housekeeping data file: Thermocouples monitoring internal temperature of container"
    # load up header information for file
    for entry in header:
        HKeepncfile.setncattr(entry[0],entry[1])

    # give variables units
    TimestampData.units = "Fractional Hours"
    TemperatureData.units = "Celcius"

    # give variables descriptions
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    TemperatureData.description = "Temperature of the inside of the container"

    # and finally close file
    HKeepncfile.close()



# ----------------------- Weather Station ------------------                 
def processWS(WSfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making WS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = WSfile[-19:-11]
    fileTime = WSfile[-10:-4]
    print (fileDate)
    print (fileTime)    
    
    Temperature = []
    RelHum = []
    Pressure = []
    AbsHum = []
    Timestamp = []
    
    with open(WSfile) as f: # read in file,
        for line in f:
            linelist = line.split()
            if len(linelist) == 5:
                Temperature.append(linelist[0])
                RelHum.append(linelist[1])
                Pressure.append(linelist[2])
                AbsHum.append(linelist[3])
                Timestamp.append(linelist[4])
                
    # make sure output path exists

    ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
    
    place = os.path.join(LocalNetCDFOutputPath,fileDate,"WSsample"+fileTime+".nc")
    WSncfile = Dataset(place,'w')
    # timestamp defines the dimentions of variables
    WSncfile.createDimension('time',len(Timestamp))
    
    # creates variables
    TimestampData = WSncfile.createVariable('time',dtype('float').char,('time'))
    TemperatureData = WSncfile.createVariable('Temperature',dtype('float').char,('time'))
    RelHumData = WSncfile.createVariable('RelHum',dtype('float').char,('time'))
    PressureData = WSncfile.createVariable('Pressure',dtype('float').char,('time'))
    AbsHumData = WSncfile.createVariable('AbsHum',dtype('float').char,('time'))
    
    #fills variables
    TimestampData[:] = Timestamp
    TemperatureData[:] = Temperature
    RelHumData[:] = RelHum
    PressureData[:] = Pressure
    AbsHumData[:] = AbsHum
    
    # brief description of file
    WSncfile.description = "Weather Station data file: taken at surface level "
    # load up header information for file
    for entry in header:
        WSncfile.setncattr(entry[0],entry[1])
        
    # give variables units
    TimestampData.units = "Fractional Hours"
    TemperatureData.units = "Celcius"
    RelHumData.units = "%"
    PressureData.units = "Millibar"
    AbsHumData.units = "g/kg"
    
    # give variables descriptions
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    TemperatureData.description = "Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)"
    RelHumData.description = "Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"
    PressureData.description = "Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)"
    AbsHumData.description = "Atmospheric absolute humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"
    
    # and finally close file 
    WSncfile.close()
    

    
# ----------------------- Laser Locking ------------------
def processLL(LLfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making LL Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = LLfile[-19:-11]
    fileTime = LLfile[-10:-4]
    print (fileDate)
    print (fileTime)    
    
    LaserNum = []
    Wavelength = []
    WaveDiff = []
    IsLocked = []
    TempDesired = []
    TempMeas = []
    Current = []
    Timestamp = []
    
    #read in file line by line
    with open(LLfile) as f:
        for line in f:
            # split up the line into numbers in list
            linelist = line.split()
            # making sure the line has the appropriate number of entries for the expected format
            if len(linelist) == 9: 
                LaserNum.append(str(linelist[0]))
                Wavelength.append(linelist[1])
                WaveDiff.append(linelist[2])
                IsLocked.append(linelist[3])
                TempDesired.append(linelist[4])
                TempMeas.append(linelist[5])
                Current.append(linelist[6])
                Timestamp.append(linelist[7])
                # Datestamp.append(linelist[8]) # not using the date
                
    ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
    
    place = os.path.join(LocalNetCDFOutputPath,fileDate,"LLsample"+fileTime+".nc")
    LLncfile = Dataset(place,'w')
    
    # create the time dimention
    LLncfile.createDimension('time',len(Timestamp))
    
    # add in variables that are expected to be the same size as timestamp which is the master dimension 
    TimestampData = LLncfile.createVariable('time',dtype('float').char,('time'))
    LaserNumData = LLncfile.createVariable('LaserName','str',('time'))
    WavelengthData = LLncfile.createVariable('Wavelength',dtype('float').char,('time'))
    WaveDiffData = LLncfile.createVariable('WaveDiff',dtype('float').char,('time'))
    IsLockedData = LLncfile.createVariable('IsLocked',dtype('float').char,('time'))
    TempDesiredData = LLncfile.createVariable('TempDesired',dtype('float').char,('time'))
    TempMeasData = LLncfile.createVariable('TempMeas',dtype('float').char,('time'))
    CurrentData = LLncfile.createVariable('Current',dtype('float').char,('time'))
    
    # filling the variables that are now in the NetCDF file
    TimestampData[:] = Timestamp
    LaserNumData[:] = np.asarray(LaserNum, dtype='str')
    WavelengthData[:] = Wavelength
    WaveDiffData[:] = WaveDiff
    IsLockedData[:] = IsLocked
    TempDesiredData[:] = TempDesired
    TempMeasData[:] = TempMeas
    CurrentData[:] = Current
    
    LLncfile.description = "Laser Locking data file"
    
    for entry in header:
        LLncfile.setncattr(entry[0],entry[1])
        
    TimestampData.units = "Fractional Hours"
    LaserNumData.units = "Unitless"
    WavelengthData.units = "nm"
    WaveDiffData.units = "nm"
    IsLockedData.units = "Unitless"
    TempDesiredData.units = "Celcius"
    TempMeasData.units = "Celcius"
    CurrentData.units = "Amp"
    
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    LaserNumData.description = "Name of the laser that was being locked (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or unknown)"
    WavelengthData.description = "Wavelength of the seed laser measured by the wavemeter (reference to vacuum)"
    WaveDiffData.description = "Wavelength of the seed laser measured by the wavemeter (reference to vacuum) - Desired wavelenth "
    IsLockedData.description = "Boolean value defining if the operational software considered the wavelength difference low enough to be locked"
    TempDesiredData.description = "Laser temperature setpoint"
    TempMeasData.description = "Measured laser temperature from the Thor 8000 diode thermo-electric cooler"
    CurrentData.description = "Measured laser current from the Thor 8000 diode laser controller"
    
    LLncfile.close()
    


# ----------------------- Etalon Data ------------------
def processEtalons(EtalonFile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making Etalon Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = EtalonFile[-19:-11]
    fileTime = EtalonFile[-10:-4]
    print (fileDate)
    print (fileTime)
    
    EtalonNum = []
    Temperature = []
    TempDiff = []
    IsLocked = []
    Timestamp = []
    Datestamp = [] # was removed to avoid confusion. redundant information anyway
    
    with open(EtalonFile) as f:
        for line in f:
            linelist = line.split()
            if len(linelist) == 6:
                EtalonNum.append(str(linelist[0]))
                Temperature.append(linelist[1])
                TempDiff.append(linelist[2])
                IsLocked.append(linelist[3])
                Timestamp.append(linelist[4])
                Datestamp.append(linelist[5]) 
                
    ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
    Etalonncfile = Dataset(os.path.join(LocalNetCDFOutputPath,fileDate,"Etalonsample"+fileTime+".nc"),'w')
    
    Etalonncfile.createDimension('time',len(Timestamp))
    
    TimestampData = Etalonncfile.createVariable('time',dtype('float').char,('time'))
    EtalonNumData = Etalonncfile.createVariable('EtalonNum','str',('time'))
    TemperatureData = Etalonncfile.createVariable('Temperature',dtype('float').char,('time'))
    TempDiffData = Etalonncfile.createVariable('TempDiff',dtype('float').char,('time'))
    IsLockedData = Etalonncfile.createVariable('IsLocked',dtype('float').char,('time'))
    
    TimestampData[:] = Timestamp
    EtalonNumData[:] = np.asarray(EtalonNum, dtype='str')
    TemperatureData[:] = Temperature
    TempDiffData[:] = TempDiff
    IsLockedData[:] = IsLocked
    
    Etalonncfile.description = "Etalon data file"
    
    for entry in header:
        Etalonncfile.setncattr(entry[0],entry[1])
        
    TimestampData.units = "Fractional Hours"
    EtalonNumData.units = "Unitless"
    TemperatureData.units = "Celcius"
    TempDiffData.units = "Celcius"
    IsLockedData.units = "Unitless"
    
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    EtalonNumData.description = "Name of the etalon that was being checked (Choices are: WVEtalon, HSRLEtalon, O2Etalon, or unknown)"
    TemperatureData.description = "Measured temperature of the etalon from the Thor 8000 thermo-electric cooler"
    TempDiffData.description = "Temperature difference of etalon measured - desired setpoint"
    IsLockedData.description = "Boolean value defining if the operational software considered the temperature difference low enough to be locked"
    
    Etalonncfile.close()
    
    

# ----------------------- MCS Power ------------------
def processPower(Powerfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making Power Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Powerfile[-19:-11]
    fileTime = Powerfile[-10:-4]
    print (fileDate)
    print (fileTime)
    
    Timestamp = []
    RTime = []
    PowerCh = []
    HSRLPowCh = 0
    OnlineH2OCh = 0
    OfflineH2OCh = 0
    OnlineO2Ch = 0
    OfflineO2Ch = 0
    ChannelAssign = []
    
    nChannels = 12
    i=0
    while i < nChannels:
        i=i+1
        PowerCh.append([])
        ChannelAssign.append("Unassigned")
    with open(Powerfile, "rb") as file:
        file.seek(0)  # Go to beginning
        
        k=0 # k is the number of entries in the power file. 
        Mybytes = 146 # this is the number of bytes per power return.
       
        while k < (os.path.getsize(Powerfile))/Mybytes:
            k = k + 1
            couple_bytes = file.read(Mybytes)
                        
            if k != 1:
                # checking if channel assignments changed mid file.
                # The resulting NetCDF file will have assignments based on the assignments that are in the last entry
                # but will log the error as below. 
                               
                if HSRLPowCh != ord(couple_bytes[23:24])-48 or OnlineH2OCh != ord(couple_bytes[34:35])-48 or OfflineH2OCh != ord(couple_bytes[46:47])-48 or OnlineO2Ch != ord(couple_bytes[56:57])-48 or OfflineO2Ch != ord(couple_bytes[67:68])-48:
                    ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonErrors",str(LastTime),".txt")
                    writeString = "ERROR: Power Channel Assignments changed mid file in " + Powerfile + " - " + str(NowTime) + '\n'
                    Write2ErrorFile(ErrorFile, writeString)
              
            HSRLPowCh = ord(couple_bytes[23:24])-48
            OnlineH2OCh = ord(couple_bytes[34:35])-48 
            OfflineH2OCh = ord(couple_bytes[46:47])-48
            OnlineO2Ch = ord(couple_bytes[56:57])-48
            OfflineO2Ch = ord(couple_bytes[67:68])-48
            
            ChannelAssign[HSRLPowCh] = str("HSRL")
            ChannelAssign[OnlineH2OCh] = str("OnlineH2O")
            ChannelAssign[OfflineH2OCh] = str("OfflineH2O")
            ChannelAssign[OnlineO2Ch] = str("OnlineO2")
            ChannelAssign[OfflineO2Ch] = str("OfflineO2")

            TS = struct.unpack('>d',couple_bytes[0:8])
            Timestamp.append(TS[0])
                       
            a = ord(couple_bytes[82:83])
            b = ord(couple_bytes[83:84])*2**8
            c = ord(couple_bytes[84:85])*2**16
            d = ord(couple_bytes[85:86])*2**24

            RTime.append( a + b + c + d ) 
                        
            j=0
            while j < nChannels:
                a = ord(couple_bytes[4*j+86:4*j+87])
                b = ord(couple_bytes[4*j+87:4*j+88])*2**8
                c = ord(couple_bytes[4*j+88:4*j+89])*2**16
                
                PowerCh[j].append( a + b + c )
                j=j+1

        ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
        place = os.path.join(LocalNetCDFOutputPath,fileDate,"Powsample"+fileTime+".nc")
        Powncfile = Dataset(place,'w')
    
        Powncfile.createDimension('time',len(Timestamp))
        Powncfile.createDimension('nChannels',nChannels)
        
        TimestampData = Powncfile.createVariable('time',dtype('float32').char,('time'))
        RTimeData= Powncfile.createVariable('RTime',dtype('float32').char,('time'))
        PowChData = Powncfile.createVariable('Power',dtype('float32').char,('nChannels','time'))
        ChannelAssignData = Powncfile.createVariable('ChannelAssignment','str',('nChannels'))
        
        TimestampData[:] = Timestamp
        RTimeData[:] = RTime
        PowChData[:] = PowerCh
        ChannelAssignData[:] =  np.asarray(ChannelAssign, dtype='str')
        
        Powncfile.description = "Multi-channel scalar (MCS) power monitor data file"
        for entry in header:
            Powncfile.setncattr(entry[0],entry[1])
            
        TimestampData.units = "Fractional Hours"
        RTimeData.units = "ms"
        PowChData.units = "PIN count"
        ChannelAssignData.units = "Unitless"
        
        TimestampData.description = "The time of collected data in UTC hours from the start of the day"
        PowChData.description = "Raw pin count from the MCS analog detectors (must be converted to power by _______)"
        ChannelAssignData.description = "String value defining what hardware was connected to each of the 12 MCS analog detection channels (Choices are: WVOnline, WVOffline, HSRL, O2Online, O2Offline, or Unknown)"
        RTimeData.description = "Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)."
        Powncfile.close()
        


# ----------------------- MCS Data ------------------
def processMCS(MCSfile,LocalNetCDFOutputPath,header,NowDate,NowTime,LastTime):
    print ("Making MCS Data File", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = MCSfile[-19:-11] 
    fileTime = MCSfile[-10:-4]
    print (fileDate)
    print (fileTime)
    Timestamp = []
    ProfPerHist = []
    Channel = []
    Sync = []
    CntsPerBin = []
    NBins = []
    RTime = []
    FrameCtr = []
    DataArray = []
    np.array(DataArray, dtype='f')
    ChannelAssign = []
    
    nChannels = 12
    i=0
    while i < nChannels:
        i=i+1
        ChannelAssign.append("Unassigned")
    with open(MCSfile , 'rb') as file:
        thing = file.read()
        file_length=len(thing)
        file.seek(0)
        
        #as i read i will add to ReadIndex based on number of bytes read
        ReadIndex=0
        headerBytes = 127
        
        while ReadIndex+headerBytes < file_length:
            
            data = file.read(headerBytes)
            #print (data[:headerBytes])
            
            ReadIndex = ReadIndex+headerBytes
            TS = struct.unpack('>d',data[:8])
            #print (TS)
            Timestamp.append(TS[0])
            
            if ReadIndex != headerBytes:
                # checking if channel assignments changed mid file.
                # The resulting NetCDF file will have assignments based on the assignments that are in the last entry
                # but will log the error as below. 
                if OnlineH2OCh != ord(data[29:30])-48 or OfflineH2OCh != ord(data[42:43])-48 or CombinedHSRLCh != ord(data[57:58])-48 or MolecularHSRLCh != ord(data[73:74])-48 or OnlineO2Ch != ord(data[84:85])-48 or OfflineO2Ch != ord(data[96:97])-48:
                    ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonErrors",str(LastTime),".txt")
                    writeString = "ERROR: Data Channel Assignments changed mid file in " + str(MCSfile) + " - " + str(NowTime) + '\n'
                    Write2ErrorFile(ErrorFile, writeString)

            OnlineH2OCh = ord(data[29:30])-48 # 48 is the number to subtract from ascii to get the numerical values
            if ord(data[28:29]) == 49: # a two digit channel assignment so add 10 
                OnlineH2OCh = OnlineH2OCh + 10                             
            OfflineH2OCh = ord(data[42:43])-48
            if ord(data[41:42]) == 49: 
                OfflineH2OCh = OfflineH2OCh + 10     
            CombinedHSRLCh = ord(data[57:58])-48
            if ord(data[56:57]) == 49: 
                CombinedHSRLCh = CombinedHSRLCh + 10     
            MolecularHSRLCh = ord(data[73:74])-48
            if ord(data[72:73]) == 49: 
                MolecularHSRLCh = MolecularHSRLCh + 10     
            OnlineO2Ch = ord(data[84:85])-48
            if ord(data[83:84]) == 49: 
                OnlineO2Ch = OnlineO2Ch + 10     
            OfflineO2Ch = ord(data[96:97])-48
            if ord(data[95:96]) == 49: 
                OfflineO2Ch = OfflineO2Ch + 10
                
            ChannelAssign[OnlineH2OCh] = str("WVOnline")
            ChannelAssign[OfflineH2OCh] = str("WVOffline")
            ChannelAssign[CombinedHSRLCh] = str("HSRLCombined")
            ChannelAssign[MolecularHSRLCh] = str("HSRLMolecular")
            ChannelAssign[OnlineO2Ch] = str("O2Online")
            ChannelAssign[OfflineO2Ch] = str("O2Offline")
            
            profPerHist = ord(data[112:113]) * 2**8 + ord(data[111:112])
            #print (profPerHist)
            ProfPerHist.append(profPerHist)
            
            # tempBytes has 8 bits which hold both the channel and sync bits. 
            tempBytes = ord(data[114:115])
            sync = tempBytes%16
            channel = (tempBytes-sync)/16
            
            #print ("channel = ",channel)
            #print ("sync = ",sync)
            
            Channel.append(channel)
            Sync.append(sync)
            
            cntsPerBin = ord(data[116:117]) * 2**8 + ord(data[115:116])
            #print (cntsPerBin)
            CntsPerBin.append(cntsPerBin)
            
            nBins = ord(data[118:119]) * 2**8 + ord(data[117:118])
            #print (nBins)
            NBins.append(nBins)
            
            rTime = ord(data[121:122])*2**16 + ord(data[120:121])*2**8 + ord(data[119:120])
            #print (rTime)
            RTime.append(rTime)
            
            frameCtr = ord(data[122:123])
            #print (frameCtr)
            FrameCtr.append(frameCtr)
            
            if len(DataArray) == 0:
                for k in range(0,nBins):
                    DataArray.append([])
                    
            for v in range(0, nBins):
                data = file.read(4)
                ReadIndex = ReadIndex+4

                chan = ord(data[3:4])/16
                
                if chan != channel:
                    print (str(sys.argv[1]))
                    print (str(NowDate))
                    print (str(LastTime))
                    ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonErrors",str(LastTime),".txt")
                    writeString = "ERROR: channel number read from data entry does not match header - "+str(NowTime) + '\n'
                    Write2ErrorFile(ErrorFile, writeString)

                thisVal = ord(data[2:3])*2**16 + ord(data[1:2])*2**8 + ord(data[0:1])
                DataArray[v].append(thisVal)
            
            # confirming footer word was where expected
            data = file.read(4)
            ReadIndex = ReadIndex+4
            #print ("footer? = " , data)
            if ord(data[0:1]) != 255:
                ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonErrors",str(LastTime),".txt")
                writeString = "ERROR: Length of data frame does not match number of bins - " + str(NowTime) + '\n'
                Write2ErrorFile(ErrorFile, writeString)

            # throw away extra bits on end of data frame so next is alligned
            data = file.read(8)
            ReadIndex = ReadIndex+8
                
        ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
        path = os.path.join(LocalNetCDFOutputPath,fileDate,"MCSsample"+fileTime+".nc")
        MCSncfile = Dataset(path,'w')
        
        MCSncfile.createDimension('time',len(Timestamp))
        MCSncfile.createDimension('nBins',max(NBins))
        MCSncfile.createDimension('nChannels',nChannels)
        
        TimestampData = MCSncfile.createVariable('time',dtype('float32').char,('time'))
        ProfPerHistData = MCSncfile.createVariable('ProfilesPerHist',dtype('float32').char,('time'))
        ChannelData = MCSncfile.createVariable('Channel',dtype('float32').char,('time'))
        CntsPerBinData = MCSncfile.createVariable('CntsPerBin',dtype('float32').char,('time'))
        NBinsData = MCSncfile.createVariable('NBins',dtype('float32').char,('time'))
        DataArrayData = MCSncfile.createVariable('Data',dtype('float32').char,('nBins','time'))
        ChannelAssignData = MCSncfile.createVariable('ChannelAssignment','str',('nChannels'))
        RTimeData = MCSncfile.createVariable('RTime',dtype('float32').char,('time'))
     
        TimestampData[:] = Timestamp
        ProfPerHistData[:] = ProfPerHist
        ChannelData[:] = Channel
        CntsPerBinData[:] = CntsPerBin
        NBinsData[:] = NBins
        DataArrayData[:] = DataArray
        ChannelAssignData[:] = np.asarray(ChannelAssign, dtype='str')
        RTimeData[:] = RTime
        
        MCSncfile.description = "Multi-channel scalar (MCS) photon count histogram data file"
        for entry in header:
            MCSncfile.setncattr(entry[0],entry[1])
                
        TimestampData.units = "Fractional Hours"
        ProfPerHistData.units = "Number of shots"
        ChannelData.units = "Unitless"
        CntsPerBinData.units = "Unitless"
        NBinsData.units = "Unitless"
        DataArrayData.units = "Photons"
        ChannelAssignData.units = "Unitless"
        RTimeData.units = "ms"
        
        TimestampData.description = "The time of collected data in UTC hours from the start of the day"
        ProfPerHistData.description = "Number of laser shots summed to create a single verticle histogram"
        ChannelData.description = "MCS hardware channel number for each measurement. There are 8 real valued inputs and 4 extra channels resulting from demuxing. "
        CntsPerBinData.description = "The number of 5 ns clock counts that defines the width of each altitude bin. To convert to range take the value here and multiply by 5 ns then convert to range with half the speed of light"
        NBinsData.description = "Number of sequential altitude bins measured for each histogram profile"
        DataArrayData.description = "A profile containing the number of photons returned in each of the sequential altitude bin"
        ChannelAssignData.description = "String value defining what hardware was connected to the MCS digital detection channels (Choices are: WVOnline, WVOffline, HSRLCombined, HSRLMolecular, O2Online, O2Offline, or Unassigned)"
        RTimeData.description = "Relative time counter, 20 bit time valuerelative to the most recent system reset (or time reset)."
        MCSncfile.close()
        
    

def toSec(fracHour):
    return (float(fracHour) - int(fracHour))*3600 



#=========== called by various merging functions to interpolate sparse data onto
# a timeseries that is determined by MCS data if available, or to a 1/2 Hz timeseries
# if data is unavailable ===========
def interpolate(ArrayIn,MasterIn, VarTimestamp, MasterTimestamp):
        
    LocalArrayIn = copy(ArrayIn)
    LocalMasterIn = copy(MasterIn)
    LocalVarTimestamp = copy(VarTimestamp)
    LocalMasterTimestamp = copy(MasterTimestamp)
    ArrayOut = LocalMasterIn
    
    timedeltaSum = 0
    timecounter = 0
    for i in range(0,len(LocalMasterTimestamp)-1):
        timecounter = timecounter + 1
        timedeltaSum = timedeltaSum + (LocalMasterTimestamp[i+1] - LocalMasterTimestamp[i])
    if len(LocalMasterTimestamp) == 1:
        ArrayOut = ma.array([float('NaN')])
        return ArrayOut
    if len(LocalMasterTimestamp) == 0:
        ArrayOut = ma.array([])
        return ArrayOut
        
    AveTimeDelta = timedeltaSum/timecounter
    
    placeOututArray = 0 # this hold where in the output array we want

    if len(LocalVarTimestamp) > 0:
        for localTime in LocalMasterTimestamp:
            if toSec(LocalVarTimestamp[0]) > localTime - AveTimeDelta:
                placeOututArray = placeOututArray + 1
            else:
                while len(LocalVarTimestamp) > 1 and toSec(LocalVarTimestamp[1]) < localTime:
                    LocalVarTimestamp.pop(0)
                    LocalArrayIn.pop(0)
                if len(LocalVarTimestamp) > 1:    
                    deltaT = toSec(LocalVarTimestamp[1]) - toSec(LocalVarTimestamp[0])
                    deltaTau = localTime - toSec(LocalVarTimestamp[0])
                    fracT = deltaTau/deltaT 
                    deltaVal = LocalArrayIn[1] - LocalArrayIn[0]
                    newVal = LocalArrayIn[0] + (fracT * deltaVal)
                    ArrayOut[placeOututArray]=newVal
                placeOututArray = placeOututArray + 1
    return ArrayOut


    
#=========== called by power merging function to appfileTimely frequent data onto
# a timeseries that is determined by MCS data if available, or to a 1/2 Hz timeseries
# if data is unavailable ===========
def assign(ArrayIn,MasterIn,VarTimestamp,MasterTimestamp):
    LocalArrayIn = copy(ArrayIn)
    LocalMasterIn = copy(MasterIn)
    LocalVarTimestamp = copy(VarTimestamp)
    LocalMasterTimestamp = copy(MasterTimestamp)

    ArrayOut = LocalMasterIn

    timedeltaSum = 0
    timecounter = 0
    for i in range(0,len(LocalMasterTimestamp)-1):
        timecounter = timecounter + 1
        timedeltaSum = timedeltaSum + (LocalMasterTimestamp[i+1] - LocalMasterTimestamp[i])
    if len(LocalMasterTimestamp) == 1:
        ArrayOut = ma.array([float('NaN')])
        return ArrayOut
    if len(LocalMasterTimestamp) == 0:
        ArrayOut = ma.array([])
        return ArrayOut
    
    AveTimeDelta = timedeltaSum/timecounter

    placeOututArray = 0 # this hold where in the output array we want

    if len(LocalVarTimestamp) > 0:
        for localTime in LocalMasterTimestamp:
            if toSec(LocalVarTimestamp[0]) > localTime - AveTimeDelta:
                placeOututArray = placeOututArray + 1
            else:
                tempsum = 0
                tempcount = 0
                while len(LocalVarTimestamp) > 1 and len(LocalArrayIn) > 1 and toSec(LocalVarTimestamp[0]) < localTime:
                    if toSec(LocalVarTimestamp[0]) > (localTime - AveTimeDelta) :
                        tempsum = tempsum + LocalArrayIn[0]
                        tempcount = tempcount + 1
                    LocalVarTimestamp.pop(0)
                    LocalArrayIn.pop(0)
                if tempcount > 0:
                    ArrayOut[placeOututArray] = (tempsum/tempcount)
                placeOututArray = placeOututArray + 1

    return ArrayOut



#=========== called by merging function to conform to CFRadial standards ===========
def CFRadify(MergedFile,CFRadPath,header):
    print ("formatting merged file into CFRadial", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = MergedFile[-29:-21]
    fileTime = MergedFile[-9:-3]
    print (fileDate)
    print (fileTime) 
    
    Mergedncfile = Dataset(MergedFile,'a')
        
    # brief description of file
    Mergedncfile.description = "Water Vapor Dial data file"
        
    # load up header information for file global attributes
    for entry in header:
        Mergedncfile.setncattr(entry[0],entry[1])
        
    # these two dimensions should already exist
    # Mergedncfile.createDimension('time',len(MasterTimestamp))
    # Mergedncfile.createDimension('range',MasterNBins[0])

    # these dimentions are being added here
    try:
        Mergedncfile.createDimension('sweep',1)
        Mergedncfile.createDimension('string_length',20)
        Mergedncfile.createDimension('string_length_DataType',5)
    except:
        pass
    
    # thse are the coordinate variables - time is already built, range is not. 
    TimestampData = Mergedncfile['time']

    try:
        RangeData = Mergedncfile.createVariable('range',dtype('float').char,('range'))
        RangeData.standard_name = 'projection_range_coordinate'
        RangeData.long_name = 'range_to_measurement_volume'           
        RangeData.units = "meters"
        RangeData.spacing_is_constant = 'true'
        RangeData.meters_to_center_of_first_gate = 0
        RangeData.axis = "radial_range_coordinate"
        RangeData.description = "The range variable for collected data as distance from DIAL unit"
    except:
        RangeData = Mergedncfile.variables["range"][:]
    
    # global variables
    try:
        VolNumData = Mergedncfile.createVariable('volume_number',dtype('float').char,())
        InstTypeData = Mergedncfile.createVariable('instrument_type','S1','string_length_DataType')
    except:
        InstTypeData = Mergedncfile.variables["instrument_type"][:]

    InstTypeData[:] = list("lidar")

    try:
        TimeStartData = Mergedncfile.createVariable('time_coverage_start','S1','string_length')
        TimeEndData = Mergedncfile.createVariable('time_coverage_end','S1','string_length')
    except:
        TimeStartData = Mergedncfile.variables["time_coverage_start"][:]
        TimeEndData = Mergedncfile.variables["time_coverage_end"][:]
        
    year = int(int(fileDate)/10000)
    month = int((int(fileDate) - year*10000)/100)
    day = int((int(fileDate) - year*10000 - month*100))
    hour = int(int(fileTime)/10000)
    minute = int((int(fileTime) - hour*10000)/100)
    sec = int(int(fileTime) - hour*10000 - minute*100)
    TimeStart = format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')+"T"+format(hour,'02d')+":"+format(minute,'02d')+":"+format(sec,'02d')+"Z"
    TimeStartData[:] = list(TimeStart)
    lastTime = TimestampData[len(TimestampData)-1]
    hour = int(int(fileTime)/10000)
    minute = int(float(lastTime)/60)
    sec = int(float(lastTime)%60)
    TimeEnd = format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')+"T"+format(hour,'02d')+":"+format(minute,'02d')+":"+format(sec,'02d')+"Z"

    TimeEndData[:] = list(TimeEnd)

    # set attributes for time 
    TimestampData.standard_name = 'time'
    TimestampData.long_name = 'time_in_seconds_since_volume_start'           
    TimestampData.units = "seconds since " + TimeStart
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"
    
    # setting value of range variable
    MasterRange = []
    try:
        NBinsData = dataset.variables['NBins'][:]
        for i in range (0,int(NBinsData[0])):
            MasterRange.append(i*37.5)
            # hard coded 37.5 for now which is conversion 
            # from bin number to actual range in meters     
    except:
        for i in range (0,560):
            MasterRange.append(i*37.5) 
            # hard coded for fixed number of bins in case there was no MCS data
            # also hard coded for range bins. 
    RangeData[:] = MasterRange

    # Location Variables
    try:
        LatitudeData = Mergedncfile.createVariable('latitude',dtype('double').char,())
        LongitudeData = Mergedncfile.createVariable('longitude',dtype('double').char,())
        AltitudeData = Mergedncfile.createVariable('altitude',dtype('double').char,())
        for entry in header:
            if entry[0] == "latitude":
                LatitudeData[:] = entry[1]
            if entry[0] == "longitude":
                LongitudeData[:] = entry[1]
            if entry[0] == "altitude":
                AltitudeData[:] = entry[1]            
        LatitudeData.units = "degrees_north"
        LongitudeData.units = "degrees_east"
        AltitudeData.units = "meters"
    except:
        pass
    
    # sweep variables
    try:
        SweepNumData = Mergedncfile.createVariable('sweep_number',dtype('int').char,('sweep'))
        SweepModeData = Mergedncfile.createVariable('sweep_mode','S1',('sweep','string_length'))
        FixedAngleData = Mergedncfile.createVariable('fixed_angle',dtype('float').char,('sweep'))
        SweepStartData = Mergedncfile.createVariable('sweep_start_ray_index',dtype('int').char,('sweep'))
        SweepEndData = Mergedncfile.createVariable('sweep_end_ray_index',dtype('int').char,('sweep'))
        FixedAngleData.units = "degrees"
    except:
        pass
    
    # sensor pointing variables
    try:
        AzimuthData = Mergedncfile.createVariable('azimuth',dtype('float').char,('time'))
        ElevationData = Mergedncfile.createVariable('elevation',dtype('float').char,('time'))

        # set attributes for Azimuth & Elevation
        AzimuthData.standard_name = "ray_azimuth_angle"
        AzimuthData.long_name = "azimuth_angle_from_true_north"
        AzimuthData.units = "degrees"
        AzimuthData.axis = "radial_azimuth_coordinate"
        ElevationData.standard_name = "ray_elevation_angle"
        ElevationData.long_name = "elevation_angle_from_horizontal_plane"
        ElevationData.units = "degrees"
        ElevationData.axis = "radial_elevation_coordinate"
    except:
        pass
    
    
    
    # moving platform geo-reference variables
    try:
        HeadingData = Mergedncfile.createVariable('heading',dtype('float').char,('time'))
        RollData = Mergedncfile.createVariable('roll',dtype('float').char,('time'))
        PitchData = Mergedncfile.createVariable('pitch',dtype('float').char,('time'))
        DriftData = Mergedncfile.createVariable('drift',dtype('float').char,('time'))
        RotationData = Mergedncfile.createVariable('rotation',dtype('float').char,('time'))
        TiltData = Mergedncfile.createVariable('tilt',dtype('float').char,('time'))
    
        HeadingData.units = "degrees"
        RollData.units = "degrees"
        PitchData.units = "degrees"
        DriftData.units = "degrees"
        RotationData.units = "degrees"
        TiltData.units = "degrees"
    except:
        pass
    
    
    # giving attributes to any present data fields
    try:
        WVOnlineData = dataset.variables['WVOnline'][:]
        WVOnlineData.long_name = "Water Vapor Online"
        WVOnlineData.standard_name = "WVOnline"
        WVOnlineData.units = "Photons"
        WVOnlineData._FillValue = ""
        WVOnlineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        WVOfflineData = dataset.variables['WVOffline'][:]
        WVOfflineData.long_name = "Water Vapor Offline"
        WVOfflineData.standard_name = "WVOffline"
        WVOfflineData.units = "Photons"
        WVOfflineData._FillValue = ""
        WVOfflineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        HSRLCombinedData = dataset.variables['HSRLCombined'][:]
        HSRLCombinedData.long_name = "HSRL Combined"
        HSRLCombinedData.standard_name = "HSRLCombined"
        HSRLCombinedData.units = "Photons"
        HSRLCombinedData._FillValue = ""
        HSRLCombinedData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        HSRLMolecularData = dataset.variables['HSRLMolecular'][:]
        HSRLMolecularData.long_name = "HSRL Molecular"
        HSRLMolecularData.standard_name = "HSRLMolecular"
        HSRLMolecularData.units = "Photons"
        HSRLMolecularData._FillValue = ""
        HSRLMolecularData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        O2OnlineData = dataset.variables['O2Online'][:]
        O2OnlineData.long_name = "Oxygen Online"
        O2OnlineData.standard_name = "O2Online"
        O2OnlineData.units = "Photons"
        O2OnlineData._FillValue = ""
        O2OnlineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        O2OfflineData = dataset.variables['O2Offline'][:]
        O2OfflineData.long_name = "Oxygen Offline"
        O2OfflineData.standard_name = "O2Offline"
        O2OfflineData.units = "Photons"
        O2OfflineData._FillValue = ""
        O2OfflineData.coordinates = "elevation azimuth range"            
    except:
        pass
        


# ==========called by mergeNetCDF to process MCS photon counting data============
def mergeData(Datafile, CFRadPath):
    print ("Merging MCS Data", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Datafile[-27:-19]
    fileTime = Datafile[-9:-3]
    
    print (fileDate)
    print (fileTime)
    
    DataTimestamp = []
    DataChannelAssign = []
    DataProfPerHist = []
    DataChannel = []
    DataCntsPerBin = []
    DataNBins = []
    DataDataArray = []
    
    Datadataset = Dataset(Datafile)
    
    DataTimestamp = FillVar(Datadataset, "time")
    DataProfPerHist = FillVar(Datadataset, "ProfilesPerHist")
    DataChannel = FillVar(Datadataset, "Channel")
    DataCntsPerBin = FillVar(Datadataset, "CntsPerBin")
    DataNBins = FillVar(Datadataset, "NBins")
    DataDataArray = Fill2DVar(Datadataset, "Data")
    DataChannelAssign = FillVar(Datadataset, "ChannelAssignment")
    
    #print ("hey")
    #print (len(DataTimestamp))
    #print (len(DataProfPerHist))
    #print (len(DataChannel))
    #print (len(DataCntsPerBin))
    #print (len(DataNBins))
    #print (len(DataDataArray))
    #print (len(DataChannelAssign))
    #print ("listen")

    firstChan=-1
    i=0
    for entry in DataChannelAssign:
        if firstChan < 0:
            if entry != "Unnassigned":
                firstChan = i
        i=i+1
                
    #print ("firstChan = " , firstChan)
    
    MasterTimestamp = []
    MasterWVOnline = []
    MasterWVOffline = []
    MasterHSRLCombined = []
    MasterHSRLMolecular = []
    MasterO2Online = []
    MasterO2Offline = []
    MasterProfPerHist = []
    MasterCntsPerBin = []
    MasterNBins = []
    
    NaNArray = []
    for x in range(0,int(DataNBins[0])):
        NaNArray.append(float('nan'))
        
    i=0
    for time in DataTimestamp:
        if DataChannel[i] == firstChan:
            # the following ifs are needed if a timestamp got added but data did not
            # this is likely due to the file beginning between reported channels
            # the first three should realistically never be hit. 
            if len(MasterTimestamp) > len(MasterProfPerHist):
                MasterProfPerHist.append(float('nan'))
            if len(MasterTimestamp) > len(MasterCntsPerBin):
                MasterCntsPerBin.append(float('nan'))
            if len(MasterTimestamp) > len(MasterNBins):
                MasterNBins.append(float('nan'))
            if len(MasterTimestamp) > len(MasterWVOnline):
                MasterWVOnline.append(NaNArray)
            if len(MasterTimestamp) > len(MasterWVOffline):
                MasterWVOffline.append(NaNArray)
            if len(MasterTimestamp) > len(MasterHSRLCombined):
                MasterHSRLCombined.append(NaNArray)
            if len(MasterTimestamp) > len(MasterHSRLMolecular):
                MasterHSRLMolecular.append(NaNArray)
            if len(MasterTimestamp) > len(MasterO2Online):
                MasterO2Online.append(NaNArray)
            if len(MasterTimestamp) > len(MasterO2Offline):
                MasterO2Offline.append(NaNArray)
                
            if len(MasterTimestamp) != len(MasterProfPerHist):
                print ("MasterProfPerHist")
                print (len(MasterTimestamp))
                print (len(MasterProfPerHist))
            if len(MasterTimestamp) != len(MasterCntsPerBin):
                print ("MasterCntsPerBin")
                print (len(MasterTimestamp))
                print (len(MasterCntsPerBin))
            if len(MasterTimestamp) != len(MasterNBins):
                print ("MasterNBins")
                print (len(MasterTimestamp))
                print (len(MasterNBins))
            if len(MasterTimestamp) != len(MasterWVOnline):
                print ("MasterWVOnline")
                print (len(MasterTimestamp))
                print (len(MasterWVOnline))
            if len(MasterTimestamp) != len(MasterWVOffline):
                print ("MasterWVOffline")
                print (len(MasterTimestamp))
                print (len(MasterWVOffline))
            if len(MasterTimestamp) != len(MasterHSRLCombined):
                print ("MasterHSRLCombined")
                print (len(MasterTimestamp))
                print (len(MasterHSRLCombined))
            if len(MasterTimestamp) != len(MasterHSRLMolecular):
                print ("MasterHSRLMolecular")
                print (len(MasterTimestamp))
                print (len(MasterHSRLMolecular))
            if len(MasterTimestamp) != len(MasterO2Online):
                print ("MasterO2Online")
                print (len(MasterTimestamp))
                print (len(MasterO2Online))
            if len(MasterTimestamp) != len(MasterO2Offline):
                print ("MasterO2Offline")
                print (len(MasterTimestamp))
                print (len(MasterO2Offline))
            
            MasterTimestamp.append(time)
            MasterProfPerHist.append(DataProfPerHist[i])
            MasterCntsPerBin.append(DataCntsPerBin[i])
            MasterNBins.append(DataNBins[i])

        if DataChannelAssign[int(DataChannel[i])] == "WVOnline":
            # the next if statement is needed if we start in the middle of transmitting 
            # data and don't get the first few channels. 
            # The timestamp should be one longer at this point because we haven't 
            # yet added the data for this channel yet, but should have added the timestamp. 
            if len(MasterTimestamp) == len(MasterWVOnline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterWVOnline.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "WVOffline":
            if len(MasterTimestamp) == len(MasterWVOffline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterWVOffline.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "HSRLCombined":
            if len(MasterTimestamp) == len(MasterHSRLCombined):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterHSRLCombined.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "HSRLMolecular":
            if len(MasterTimestamp) == len(MasterHSRLMolecular):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterHSRLMolecular.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "O2Online":
            if len(MasterTimestamp) == len(MasterO2Online):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterO2Online.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "O2Offline":
            if len(MasterTimestamp) == len(MasterO2Offline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterO2Offline.append(DataDataArray[i])
        i=i+1

    # check if last entry is missing
    # this is needed if the end of file cuts off between channels
    # and is used to give one last entry to channels which are turned off
    if len(MasterTimestamp) == len(MasterProfPerHist)+1:
        MasterProfPerHist.append(float('nan'))
    if len(MasterTimestamp) == len(MasterCntsPerBin)+1:
        MasterCntsPerBin.append(float('nan'))
    if len(MasterTimestamp) == len(MasterNBins)+1:
        MasterNBins.append(float('nan'))
    if len(MasterTimestamp) == len(MasterWVOnline)+1:
        MasterWVOnline.append(NaNArray)
    if len(MasterTimestamp) == len(MasterWVOffline)+1:
        MasterWVOffline.append(NaNArray)
    if len(MasterTimestamp) == len(MasterHSRLCombined)+1:
        MasterHSRLCombined.append(NaNArray)
    if len(MasterTimestamp) == len(MasterHSRLMolecular)+1:
        MasterHSRLMolecular.append(NaNArray)
    if len(MasterTimestamp) == len(MasterO2Online)+1:
        MasterO2Online.append(NaNArray)
    if len(MasterTimestamp) == len(MasterO2Offline)+1:
        MasterO2Offline.append(NaNArray)
        
    # make sure output path exists
    ensure_dir(os.path.join(CFRadPath,fileDate,""))
    
    place = os.path.join(CFRadPath,fileDate,"MergedFiles"+fileTime+".nc")
    Mergedncfile = Dataset(place,'w')
    # timestamp defines the dimentions of variables
    Mergedncfile.createDimension('time',len(MasterTimestamp))
    Mergedncfile.createDimension('range',MasterNBins[0])
    
    # creates variables
    TimestampData = Mergedncfile.createVariable('time',dtype('float').char,('time'))
    
    WVOnlineData = Mergedncfile.createVariable('WVOnline',dtype('float').char,('time','range'))
    WVOfflineData = Mergedncfile.createVariable('WVOffline',dtype('float').char,('time','range'))
    HSRLCombinedData = Mergedncfile.createVariable('HSRLCombined',dtype('float').char,('time','range'))
    HSRLMolecularData = Mergedncfile.createVariable('HSRLMolecular',dtype('float').char,('time','range'))
    #O2OnlineData = Mergedncfile.createVariable('O2Online',dtype('float').char,('time','range'))
    #O2OfflineData = Mergedncfile.createVariable('O2Offline',dtype('float').char,('time','range'))
    ProfPerHistData = Mergedncfile.createVariable('ProfPerHist',dtype('float').char,('time'))
    CntsPerBinData = Mergedncfile.createVariable('CntsPerBin',dtype('float').char,('time'))
    NBinsData = Mergedncfile.createVariable('NBins',dtype('float').char,('time'))
    
    EmptyArray = []
    for entry in MasterTimestamp:
        EmptyArray.append(float('nan'))
    Empty2DArray = []
    for entry in MasterTimestamp:
        for x in range(0,int(MasterNBins[0])):
            Empty2DArray.append(float('nan'))
            
    # converting from fractional hours to fractional seconds for CFRadial compliance
    for i in range(0,len(MasterTimestamp)):
        MasterTimestamp[i] = (MasterTimestamp[i] - int(MasterTimestamp[i])) *3600
        
    TimestampData[:] = MasterTimestamp
    
    if len(MasterTimestamp) == len(MasterWVOnline):
        WVOnlineData[:] = MasterWVOnline
    else: 
        print ("ERROR: WVOnlineData is full Empty2DArray")
        WVOnlineData[:] = Empty2DArray
    if len(MasterTimestamp) == len(MasterWVOffline):
        WVOfflineData[:] = MasterWVOffline
    else: 
        print ("ERROR: WVOfflineData is full Empty2DArray")
        WVOfflineData[:] = Empty2DArray
    if len(MasterTimestamp) == len(MasterHSRLCombined):
        HSRLCombinedData[:] = MasterHSRLCombined
    else: 
        print ("ERROR: HSRLCombinedData is full Empty2DArray")
        HSRLCombinedData[:] = Empty2DArray
    if len(MasterTimestamp) == len(MasterHSRLMolecular):
        HSRLMolecularData[:] = MasterHSRLMolecular
    else: 
        print ("ERROR: HSRLMolecularData is full Empty2DArray")
        HSRLMolecularData[:] = Empty2DArray
    #if len(MasterTimestamp) == len(MasterO2Online):
    #    O2OnlineData[:] = MasterO2Online
    #else: 
    #    print ("ERROR: O2OfflineData is full Empty2DArray")
    #    O2OnlineData[:] = Empty2DArray
    #if len(MasterTimestamp) == len(MasterO2Offline):
    #    O2OfflineData[:] = MasterO2Offline
    #else: 
    #    print ("ERROR: O2OfflineData is full Empty2DArray")
    #    O2OfflineData[:] = Empty2DArray
    if len(MasterTimestamp) == len(MasterProfPerHist):
        ProfPerHistData[:] = MasterProfPerHist
    else: 
        print ("ERROR: ProfPerHistData is full Empty2DArray")
        ProfPerHistData[:] = EmptyArray
    if len(MasterTimestamp) == len(MasterCntsPerBin):
        CntsPerBinData[:] = MasterCntsPerBin
    else: 
        print ("ERROR: CntsPerBinData is full Empty2DArray")
        CntsPerBinData[:] = EmptyArray
    if len(MasterTimestamp) == len(MasterNBins):
        NBinsData[:] = MasterNBins
    else: 
        print ("ERROR: NBinsData is full Empty2DArray")
        NBinsData[:] = EmptyArray

    WVOnlineData.units = "Photons"
    WVOfflineData.units = "Photons"
    HSRLCombinedData.units = "Photons"
    HSRLMolecularData.units= "Photons"
    #O2OnlineData.units = "Photons"
    #O2OfflineData.units = "Photons"
    ProfPerHistData.units = "Number of shots"
    CntsPerBinData.units = "Unitless"
    NBinsData.units = "Unitless"
    
    WVOnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Water Vapor"
    WVOfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"
    HSRLCombinedData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for HSRL Combined"
    HSRLMolecularData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for HSRL Molecular"
    #O2OnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Oxygen"
    #O2OfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Oxygen"
    ProfPerHistData.description = "Number of laser shots summed to create a single vertical histogram"
    CntsPerBinData.description = "The number of 5 ns clock counts that defines the width of each altitude bin. To convert to range take the value here and multiply by 5 ns then convert to range with half the speed of light"
    NBinsData.description = "Number of sequential altitude bins measured for each histogram profile"
    
    Mergedncfile.close()



# ==========called to create files for periods where there is no photon counting data============
def createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,fromTime,toTime,AveTimeDelta):
    print ("Making Merged File Without Data", datetime.datetime.utcnow().strftime("%H:%M:%S"))

    fileTime = decimal.Decimal(fromTime*10000) # decimal.Decimal is used to round down
    fileTime = str(round(fileTime,0)).zfill(6)# append extra 0s so the file names are of constant width.

    print (fileDate)
    print (fileTime)

    CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
    NetCDFPath = os.path.join(LocalOutputPath, "NetCDFOutput", "")

    ensure_dir(CFRadPath)
    ensure_dir(NetCDFPath)

    path = os.path.join(CFRadPath,fileDate,"MergedFiles"+fileTime+".nc")

    if os.path.isfile(path):
       pass
    else:
        MCSPowerFileList = getFiles(NetCDFPath, "Powsample", ".nc", ThenDate, ThenTime)
        LLFileList = getFiles(NetCDFPath, "LLsample", ".nc", ThenDate, ThenTime)
        EtalonFileList = getFiles(NetCDFPath, "Etalonsample", ".nc", ThenDate, ThenTime)
        WSFileList = getFiles(NetCDFPath, "WSsample", ".nc", ThenDate, ThenTime)

        MCSPowerFileList.sort()
        LLFileList.sort()
        EtalonFileList.sort()
        WSFileList.sort()

        needToMake = False

        for PowerFile in MCSPowerFileList:
            if needToMake == False:
                powFileDate = PowerFile[-27:-19]
                if powFileDate == fileDate:
                    MyDataset = Dataset(PowerFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for LLFile in LLFileList:
            if needToMake == False:
                LLFileDate = LLFile[-26:-18]
                if LLFileDate == fileDate:
                    MyDataset = Dataset(LLFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for EtalonFile in EtalonFileList:
            if needToMake == False:
                EtalonFileDate = EtalonFile[-30:-22]
                if EtalonFileDate == fileDate:
                    MyDataset = Dataset(EtalonFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for WSFile in WSFileList:
            if needToMake == False:
                WSFileDate = WSFile[-26:-18]
                if WSFileDate == fileDate:
                    MyDataset = Dataset(WSFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True
                        needToMake = True

        # int ("needToMake = ",needToMake)
            # if needToMake:
        if True: # if i fix this if statement i get a segfault for reasons i do not understand.
            ensure_dir(path)
            Mergedncfile = Dataset(path,'w')
            # master timestamp is filled as 1/2 Hz if no file available
            MasterTimestamp = []
            time = (float(fromTime) - int(fromTime))*3600
            while time < (float(toTime) - int(fromTime))*3600:
                MasterTimestamp.append(time)
                time = time + AveTimeDelta*3600
            Mergedncfile.createDimension('time',len(MasterTimestamp))
            Mergedncfile.createDimension('range',0)
            TimestampData = Mergedncfile.createVariable('time',dtype('float').char,('time'))
            TimestampData[:] = MasterTimestamp

            WVOnlineData = Mergedncfile.createVariable('WVOnline',dtype('float').char,('time','range'))
            WVOfflineData = Mergedncfile.createVariable('WVOffline',dtype('float').char,('time','range'))

            WVOnlineTemp=[]
            WVOfflineTemp=[]

            for i in range(0,len(TimestampData)):
                WVOnlineTemp.append([])
                WVOfflineTemp.append([])
                for j in range(0,560):
                    WVOnlineTemp[i].append(float('NaN'))
                    WVOfflineTemp[i].append(float('NaN'))

            WVOfflineData[:] = WVOfflineTemp
            WVOnlineData[:] = WVOnlineTemp

            WVOnlineData.units = "Photons"
            WVOfflineData.units = "Photons"

            WVOnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Water Vapor"
            WVOfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Power data============
def mergePower(Powerfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Power", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Powerfile[-27:-19]
    fileTime = Powerfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    PowTimestamp = []
    PowData = []
    PowChannelAssign = []
    
    Powerdataset = Dataset(Powerfile)
    
    PowTimestamp = FillVar(Powerdataset, "time")
    PowData = FillVar(Powerdataset, "Power")
    PowChannelAssign = FillVar(Powerdataset, "ChannelAssignment")
    
    # ChannelsIn and ChannelsOut need to be the same length, 
    # In is used to read from the device file while 
    # Out is used to name the variables in the merged file 
    #ChannelsIn = ["OnlineH2O", "OfflineH2O", "HSRL", "OnlineO2", "OfflineO2"]
    #ChannelsOut = ["WVOnline", "WVOffline", "HSRL", "O2Online", "O2Offline"]
    ChannelsIn = ["OnlineH2O", "OfflineH2O", "HSRL"]
    ChannelsOut = ["WVOnline", "WVOffline", "HSRL"]
  
    PowChan = []
    for i in range (0,len(ChannelsIn)):
        PowChan.append([])
        
    for i in range(0,len(ChannelsIn)):
        for j in range(0,len(PowChannelAssign)):
            if ChannelsIn[i] == PowChannelAssign[j]:
                PowChan[i]= PowData[j].tolist()

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        PowerHour = Powerfile[-9:-7]
        if MergedHour == PowerHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstPowTime = PowTimestamp[0]
            LastPowTime = PowTimestamp[len(PowTimestamp)-1]

            if FirstPowTime < LastMergedTime or LastPowTime > FirstMergedTime:
                PowChanData = []

                for i in range (0,len(ChannelsIn)):
                    PowChanData.append([])

                for i in range (0,len(ChannelsIn)):
                    powthing = ChannelsOut[i]+"Power"
                    try: # create the variable if you can, fill it with nans until the mergeing
                        PowChanData[i] = Mergedncfile.createVariable(powthing,dtype('float').char,('time'))
                        for time in MasterTimestamp:
                            PowChanData[i].append(float('nan'))
                    except: # variable already existed
                        PowChanData[i] = Mergedncfile.variables[powthing][:]

                    # do the merging
                    PowChanData[i][:] = assign(PowChan[i],PowChanData[i],PowTimestamp,MasterTimestamp)

            for i in range (0,len(ChannelsIn)):
                PowChanData[i].units = "PIN count"
                PowChanData[i].description = "Raw pin count from the MCS analog detectors (must be converted to power using ???)"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Laser data============
def mergeLaser(LLfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Lasers", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = LLfile[-26:-18]
    fileTime = LLfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    
    #ChanAssign = ["WVOnline","WVOffline","HSRL","O2Online","O2Offline"]
    ChanAssign = ["WVOnline","WVOffline","HSRL"]
    Variables = ["Wavelength", "WaveDiff", "TempDesired", "TempMeas", "Current"]
    VarUnits = ["nm","nm","Celcius","Celcius","Amp"]
    VarDescr = ["Wavelength of the seed laser measured by the wavemeter (reference to vacuum)","Wavelength of the seed laser measured by the wavemeter (reference to vacuum) Minus Desired wavelenth (reference to vacuum)","Laser temperature setpoint","Measured laser temperature from the Thor 8000 diode thermo-electric cooler","Measured laser current from the Thor 8000 diode laser controller"]
    
    LLTimestamp = []
    LLLaserName = []
    
    LLBlockData = [] # has dimentions Variables, Timestamp
    for entry in Variables:
        LLBlockData.append([])
        
    Laserdataset = Dataset(LLfile)
    
    LLTimestamp = FillVar(Laserdataset, "time")
    LLLaserName = FillVar(Laserdataset, "LaserName")
    
    i=0
    for entry in Variables:
        LLBlockData[i] = FillVar(Laserdataset, entry)
        i=i+1
        
    ArrayTimestamp = []
    LLArrayBlockData = [] #dimentions are Variables, ChanAssign, timestamp
    
    for i in range (0,len(Variables)):
        LLArrayBlockData.append([])
        for j in range(0,len(ChanAssign)):
            LLArrayBlockData[i].append([])
            
    for i in range(0,len(ChanAssign)):
        ArrayTimestamp.append([])
        
    for i in range (0,len(LLTimestamp)):
        for j in range (0,len(ChanAssign)):
            if LLLaserName[i] == ChanAssign[j]: 
                ArrayTimestamp[j].append(LLTimestamp[i])
                for k in range(0,len(Variables)):
                    LLArrayBlockData[k][j].append(LLBlockData[k][i])

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        LLHour = LLfile[-9:-7]
        if MergedHour == LLHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstLLTime = LLTimestamp[0]
            LastLLTime = LLTimestamp[len(LLTimestamp)-1]

            if FirstLLTime < LastMergedTime or LastLLTime > FirstMergedTime:
                ChanVarData = []

                for i in range (0,len(Variables)):
                    ChanVarData.append([])
                    for j in range (0,len(ChanAssign)):
                        ChanVarData[i].append([])

                i=0
                for var in Variables:
                    j=0
                    for chan in ChanAssign:
                        thing = chan+"Laser"+var
                        try: # create the variable if you can, fill it with nans until the mergeing
                            ChanVarData[i][j] = Mergedncfile.createVariable(thing ,dtype('float').char,('time'))
                            for time in MasterTimestamp:
                                ChanVarData[i][j].append(float('nan'))
                        except:
                            ChanVarData[i][j] = Mergedncfile.variables[thing][:]
                        j=j+1
                    i=i+1

                # do the merging
                for k in range (0,len(Variables)):
                    for l in range (0,len(ChanAssign)):
                        ChanVarData[k][l] = interpolate(LLArrayBlockData[k][l],ChanVarData[k][l], ArrayTimestamp[l], MasterTimestamp)
            # add variable units and descriptions
            for i in range (0,len(Variables)):
                for j in range (0,len(ChanAssign)):
                    ChanVarData[i][j].units = VarUnits[i]
                    ChanVarData[i][j].description = VarDescr[i] + " for " + ChanAssign[j]

            Mergedncfile.close()
      


# ==========called by mergeNetCDF to process Etalon data============
def mergeEtalon(Etalonfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Etalons", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Etalonfile[-30:-22]
    fileTime = Etalonfile[-9:-3]
    print (fileDate)
    print (fileTime)
    EtalonTimestamp = []
    EtalonNum = []
    EtalonTemp = []
    EtalonTempDiff = []
    
    #Channels = ["WVEtalon", "HSRLEtalon", "O2Etalon"]
    Channels = ["WVEtalon", "HSRLEtalon"]
    
    Etalondataset = Dataset(Etalonfile)
    
    EtalonTimestamp = FillVar(Etalondataset, "time")
    EtalonNum = FillVar(Etalondataset, "EtalonNum")
    EtalonTemp = FillVar(Etalondataset, "Temperature")
    EtalonTempDiff = FillVar(Etalondataset, "TempDiff")
    
    EtalonTimestampBlock = [] # has dimentions Channel, Timestamp
    EtalonTemperatureBlock = [] # has dimentions Channel, Timestamp
    EtalonTempDiffBlock = [] # has dimentions Channel, Timestamp
    
    for entry in Channels:
        EtalonTimestampBlock.append([])
        EtalonTemperatureBlock.append([])
        EtalonTempDiffBlock.append([])
        
    for i in range(0,len(EtalonTimestamp)):
        for j in range(0,len(Channels)):
            if EtalonNum[i] == Channels[j]:
                EtalonTimestampBlock[j].append(EtalonTimestamp[i])
                EtalonTemperatureBlock[j].append(EtalonTemp[i])
                EtalonTempDiffBlock[j].append(EtalonTempDiff[i])

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        EtalonHour = Etalonfile[-9:-7]
        if MergedHour == EtalonHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstEtalonTime = EtalonTimestamp[0]
            LastEtalonTime = EtalonTimestamp[len(EtalonTimestamp)-1]

            if FirstEtalonTime < LastMergedTime or LastEtalonTime > FirstMergedTime:
                ChanTempData = []
                ChanTempDiffData = []

                for i in range (0,len(Channels)):
                    ChanTempData.append([])
                    ChanTempDiffData.append([])

                for i in range (0,len(Channels)):
                    tempstr = Channels[i]+"Temperature"
                    tempDiffstr = Channels[i]+"TempDiff"
                    try: # create the variable if you can, fill it with nans until the mergeing
                        ChanTempData[i] =  Mergedncfile.createVariable(tempstr,dtype('float').char,('time'))
                        ChanTempDiffData[i] =  Mergedncfile.createVariable(tempDiffstr,dtype('float').char,('time'))
                        for time in MasterTimestamp:
                            ChanTempData[i].append(float('nan'))
                            ChanTempDiffData[i].append(float('nan'))
                    except:
                        ChanTempData[i] = Mergedncfile.variables[tempstr][:]
                        ChanTempDiffData[i] = Mergedncfile.variables[tempDiffstr][:]

                # do the merging
                for i in range (0,len(Channels)):
                     ChanTempData[i] = interpolate(EtalonTemperatureBlock[i], ChanTempData[i], EtalonTimestampBlock[i], MasterTimestamp)
                     ChanTempDiffData[i] = interpolate(EtalonTempDiffBlock[i], ChanTempDiffData[i], EtalonTimestampBlock[i], MasterTimestamp)

            for i in range (0,len(Channels)):
                ChanTempData[i].units = "Celcius"
                ChanTempDiffData[i].units = "Celcius"
                ChanTempData[i].description = "Measured temperature of the etalon from the Thor 8000 thermo-electric cooler for " + Channels[i]
                ChanTempDiffData[i].description = "Temperature difference of etalon measured Minus desired setpoint for " + Channels[i]

            Mergedncfile.close()



# ==========called by mergeNetCDF to process WeatherStation data============
def mergeWS(WSfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging WeatherStation", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = WSfile[-26:-18]
    fileTime = WSfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    WSTimestamp = []
    WSTemperature = []
    WSRelHum = []
    WSPressure = []
    WSAbsHum = []
    
    WSdataset = Dataset(WSfile)
    
    WSTimestamp = FillVar(WSdataset, "time")
    WSTemperature = FillVar(WSdataset, "Temperature")
    WSRelHum = FillVar(WSdataset, "RelHum")
    WSPressure = FillVar(WSdataset, "Pressure")
    WSAbsHum = FillVar(WSdataset, "AbsHum")

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        WSHour = WSfile[-9:-7]
        if MergedHour == WSHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstWSTime = WSTimestamp[0]
            LastWSTime = WSTimestamp[len(WSTimestamp)-1]

            if FirstWSTime < LastMergedTime or LastWSTime > FirstMergedTime:

                try: #create the variable if you can, fill it with nans until the mergeing
                    WSTemperatureData = Mergedncfile.createVariable("WSTemperature",dtype('float').char,('time'))
                    WSRelHumData = Mergedncfile.createVariable("WSRelHum",dtype('float').char,('time'))
                    WSPressureData = Mergedncfile.createVariable("WSPressure",dtype('float').char,('time'))
                    WSAbsHumData = Mergedncfile.createVariable("WSAbsHum",dtype('float').char,('time'))
                    for time in MasterTimestamp:
                        WSTemperatureData.append(float('nan'))
                        WSRelHumData.append(float('nan'))
                        WSPressureData.append(float('nan'))
                        WSAbsHumData.append(float('nan'))
                except:
                    WSTemperatureData = Mergedncfile.variables["WSTemperature"][:]
                    WSRelHumData = Mergedncfile.variables["WSRelHum"][:]
                    WSPressureData = Mergedncfile.variables["WSPressure"][:]
                    WSAbsHumData = Mergedncfile.variables["WSAbsHum"][:]

                WSTemperatureData = interpolate(WSTemperature, WSTemperatureData, WSTimestamp, MasterTimestamp)
                WSRelHumData = interpolate(WSRelHum, WSRelHumData, WSTimestamp, MasterTimestamp)
                WSPressureData = interpolate(WSPressure, WSPressureData, WSTimestamp, MasterTimestamp)
                WSAbsHumData = interpolate(WSAbsHum, WSAbsHumData, WSTimestamp, MasterTimestamp)

            WSTemperatureData.units = "Celcius"
            WSRelHumData.units = "%"
            WSPressureData.units = "Millibar"
            WSAbsHumData.units = "g/m^3"

            WSTemperatureData.description = "Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)"
            WSRelHumData.description = "Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"
            WSPressureData.description = "Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)"
            WSAbsHumData.description = "Atmospheric absolute humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Housekeeping data============
def mergeHKeep(HKeepfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Housekeeping", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = HKeepfile[-29:-21]
    fileTime = HKeepfile[-9:-3]
    print (fileDate)
    print (fileTime)

    HKeepTimestamp = []
    HKeepTemperature = []
    
    HKeepdataset = Dataset(HKeepfile)
    
    HKeepTimestamp = FillVar(HKeepdataset, "time")
    HKeepTemperature = FillVar(HKeepdataset, "Temperature")

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        HKeepHour = HKeepfile[-9:-7]
        if MergedHour == HKeepHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstHKeepTime = HKeepTimestamp[0]
            LastHKeepTime = HKeepTimestamp[len(HKeepTimestamp)-1]

            if FirstHKeepTime < LastMergedTime or LastHKeepTime > FirstMergedTime:
                try: #create the variable if you can, fill it with nans until the mergeing
                    nSensors = len(HKeepTemperature)
                    Mergedncfile.createDimension('nInternalThermalSensors',nSensors)
                    HKeepTemperatureData = Mergedncfile.createVariable("HKeepTemperature",dtype('float').char,('nInternalThermalSensors','time'))
                except:
                    HKeepTemperatureData = Mergedncfile.variables["HKeepTemperature"][:]

                for i in range(0,len(HKeepTemperature)-1):
                    HKeepTemperatureData[i] = interpolate(list(HKeepTemperature[i]), HKeepTemperatureData[i], HKeepTimestamp, MasterTimestamp)

            HKeepTemperatureData.units = "Celcius"

            HKeepTemperatureData.description = "Temperature measured inside the container by nInternalThermalSensors"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process UPS data============
def mergeUPS(UPSfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging UPS", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = UPSfile[-27:-19]
    fileTime = UPSfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    UPSTimestamp = []
    UPSTemperature = []
    UPSHoursOnBattery = []
    
    UPSdataset = Dataset(UPSfile)

    UPSTimestamp = FillVar(UPSdataset, "time")
    UPSTemperature = FillVar(UPSdataset, "UPSTemperature")
    UPSHoursOnBattery = FillVar(UPSdataset, "HoursOnBattery")

    MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        UPSHour = UPSfile[-9:-7]
        if MergedHour == UPSHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstUPSTime = UPSTimestamp[0]
            LastUPSTime = UPSTimestamp[len(UPSTimestamp)-1]

            if FirstUPSTime < LastMergedTime or LastUPSTime > FirstMergedTime:

                try: #create the variable if you can, fill it with nans until the mergeing
                    UPSTemperatureData = Mergedncfile.createVariable("UPSTemperature",dtype('float').char,('time'))
                    UPSHoursOnBatteryData = Mergedncfile.createVariable("UPSHoursOnBattery",dtype('float').char,('time'))
                    for time in MasterTimestamp:
                        UPSTemperatureDataData.append(float('nan'))
                        UPSHoursOnBatteryData.append(float('nan'))
                except:
                    UPSTemperatureData = Mergedncfile.variables["UPSTemperature"][:]
                    UPSHoursOnBatteryData = Mergedncfile.variables["UPSHoursOnBattery"][:]

                UPSTemperatureData = interpolate(UPSTemperature, UPSTemperatureData, UPSTimestamp, MasterTimestamp)
                UPSHoursOnBatteryData = interpolate(list(UPSHoursOnBattery), UPSHoursOnBatteryData, UPSTimestamp, MasterTimestamp)

            UPSTemperatureData.units = "Celcius"
            UPSHoursOnBatteryData.units = "hours"

            UPSTemperatureData.description = "Temperature of the UPS"
            UPSHoursOnBatteryData.description = "Hours operating on UPS Battery"

            Mergedncfile.close()



# ------------------------------merged files ------------------------------
# read in raw NetCDF files and merge them into one file. 
def mergeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,LocalOutputPath,header,ErrorFile):
    print ("Creating Merged files", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    ensure_dir(LocalOutputPath)
    NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
    ensure_dir(NetCDFPath)
    CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
    ensure_dir(CFRadPath)
    if os.path.isdir(NetCDFPath):
        MCSDataFileList = getFiles(NetCDFPath, "MCSsample", ".nc", ThenDate, ThenTime)
        MCSPowerFileList = getFiles(NetCDFPath, "Powsample", ".nc", ThenDate, ThenTime)
        LLFileList = getFiles(NetCDFPath, "LLsample", ".nc", ThenDate, ThenTime)
        EtalonFileList = getFiles(NetCDFPath, "Etalonsample", ".nc", ThenDate, ThenTime)
        WSFileList = getFiles(NetCDFPath, "WSsample", ".nc", ThenDate, ThenTime)
        HKeepFileList = getFiles(NetCDFPath, "HKeepsample", ".nc", ThenDate, ThenTime)
        UPSFileList = getFiles(NetCDFPath, "UPSsample", ".nc", ThenDate, ThenTime)

        MCSDataFileList.sort()
        MCSPowerFileList.sort()
        LLFileList.sort()
        EtalonFileList.sort()
        WSFileList.sort()

        # ==========creates merged files and processes data==========

        firstTime = -1
        lastTime = -1

        for Datafile in MCSDataFileList:
            fileDate = Datafile[-27:-19]
            fileTime = Datafile[-9:-3]

            # begin with checking for gaps in data files and create placeholder files for missing data
            Datadataset = Dataset(Datafile)
            DataTimestamp = FillVar(Datadataset, "time")

            firstTime = DataTimestamp[0]

            timedeltaSum = 0
            timecounter = 0
            for i in range(0,len(DataTimestamp)-1):
                timecounter = timecounter + 1
                timedeltaSum = timedeltaSum + (DataTimestamp[i+1] - DataTimestamp[i])
            AveTimeDelta = timedeltaSum/timecounter
            nTimeDeltasGap = 3

            #print ("FT=",firstTime)
            #print ("LT=",lastTime)
            #print ("ATD=",AveTimeDelta)
            #print ("Diff=",firstTime - lastTime)

            if lastTime < 0:  # this case covers the beginning of the running period

                okDate = 0  # I'm limiting how long it will make files before the beginning of data taking
                # once createEmptyDataFile is fixed and no longer segfaulting okDate will not be needed.
                if int(ThenDate) < (int(fileDate) - 1):
                    okDate = int(fileDate) - 1
                else:
                    okDate = ThenDate

                # for date in range (int(ThenDate),int(ileDate)+1):
                for date in range(int(okDate), int(fileDate) + 1):
                    # print ("date=",date)
                    startTime = 0
                    endTime = 0
                    if date == int(fileDate):
                        startTime = 0
                        endTime = int(int(fileTime) / 10 + 1000)
                    elif date == int(NowDate):
                        startTime = 0
                        endTime = int((int(NowTime)) * 1000)
                    else:
                        startTime = 0
                        endTime = 24000

                    for time in range(int(startTime / 1000), int(endTime / 1000)):
                        createEmptyDataFile(LocalOutputPath, str(date), ThenDate, ThenTime, int(time), int(time + 1), AveTimeDelta)

                if firstTime - int(firstTime) > nTimeDeltasGap * AveTimeDelta:  # covers the fractional hour potentially missed at beginning of data collection
                    createEmptyDataFile(LocalOutputPath, fileDate, ThenDate, ThenTime, int(firstTime), firstTime, AveTimeDelta)

            else: # if this is not our first time through
                if firstTime - lastTime > nTimeDeltasGap*AveTimeDelta:
                    intDiff = int(firstTime)-int(lastTime)
                    if intDiff > 0: # we crossed at least one hour boundry
                        for i in range(0,intDiff+1): # number of files needed to account for crossing hour boundries without data
                            if i ==0: # first partial hour missed
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta)
                            elif i == intDiff: # last partial hour potentially missed
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,int(firstTime),firstTime,AveTimeDelta)
                            else: # any full hours that were missed in the middle
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,int(lastTime)+i,int(lastTime)+i+1,AveTimeDelta)
                    else:# the gap is contained within one hour
                        createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,firstTime,AveTimeDelta)

            try:
                mergeData(Datafile, CFRadPath)
            except:
                writeString = "ERROR: unable to merge MCSData into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

            lastTime = DataTimestamp[len(DataTimestamp)-1]

            if Datafile == MCSDataFileList[len(MCSDataFileList)-1]: # this case covers the end of the running period
                if fileDate != NowDate:
                    if int(lastTime) + 1 - lastTime > nTimeDeltasGap*AveTimeDelta:# covers last fractional hour at end of list
                        createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta)
                else:
                    if int(lastTime) + 1 < NowTime:
                        if int(lastTime) + 1 - lastTime > nTimeDeltasGap*AveTimeDelta:# covers last fractional hour at end of list
                            createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta)

                # I'm limiting how long it will make files past the end of data taking
                # when createEmptyDataFile is fixed i can replace the for loop
                #for date in range (int(fileDate),int(NowDate)+1):
                for date in range (int(fileDate),int(fileDate) +1):
                    #print ("date=",date)
                    startTime = 0
                    endTime = 0
                    if date == int(fileDate):
                        startTime = int(int(fileTime)/10+1000)
                        endTime = 24000
                    elif date == int(NowDate):
                        startTime = 0
                        endTime = int((int(NowTime))*1000)
                    else:
                        startTime = 0
                        endTime = 24000

                    for time in range (int(startTime/1000),int(endTime/1000)):
                        createEmptyDataFile(LocalOutputPath,str(date),ThenDate,ThenTime,int(time),int(time+1),AveTimeDelta)

        for Powerfile in MCSPowerFileList:
            try:
                mergePower(Powerfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge MCSPower into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

        for LLfile in LLFileList:
            try:
                mergeLaser(LLfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge LaserLocking into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

        for Etalonfile in EtalonFileList:
            try:
                mergeEtalon(Etalonfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge Etalons into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

        for WSfile in WSFileList:
            try:
                mergeWS(WSfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge WeatherStation into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

        for HKeepfile in HKeepFileList:
            try:
                mergeHKeep(HKeepfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge Housekeeping into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)

        for UPSfile in UPSFileList:
            try:
                mergeUPS(UPSfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge WeatherStation into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)
        
        MergedFileList = getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
        MergedFileList.sort() 
        for Mergedfile in MergedFileList:

            # need to check that all variables are present in merged file, WVOnline, Temperatures, etc.... *************************

            try:
                CFRadify(Mergedfile,CFRadPath,header)
            except:
                writeString = "ERROR: unable to put CFRadial formatting into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                Write2ErrorFile(ErrorFile, writeString)



# --------------------------------main------------------------------------
def main():
    print ("Hello World - the date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))
       
    # create timestamp for now so we know which files to load
    Hour = datetime.datetime.utcnow().strftime("%H")
    Min = datetime.datetime.utcnow().strftime("%M")
    Sec = datetime.datetime.utcnow().strftime("%S")
    MicroSec = datetime.datetime.utcnow().strftime("%f")
    NowTime = float(Hour) + float(Min)/60 + float(Sec)/3600 + float(MicroSec)/3600000000
    NowDate = datetime.datetime.utcnow().strftime("%Y%m%d")

    # LastHour variables used to find NetCDF Logging files for error and other logging. 
    LastHour = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%H")
    LastMin = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%M")
    LastSec = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%S")
    LastMicroSec = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%f")
    LastTime = math.ceil(float(LastHour) + float(LastMin)/60 + float(LastSec)/3600 + float(LastMicroSec)/3600000000)
    
    # creating Error file variable for use if needed ... which of course it never will be ... right? 
    ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild","NetCDFPythonErrors_"+str(NowDate)+"_"+str(NowTime)+".txt")

    print ("Loction of error file if needed = ", ErrorFile)
    
    LocalOutputPath = os.path.join(sys.argv[1],"Data","")
    if os.path.isdir(LocalOutputPath): # the first should be the directory where the Data folder is located.

        ensure_dir(LocalOutputPath)
        NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
        ensure_dir(NetCDFPath)
        CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
        ensure_dir(CFRadPath)

        if is_number(sys.argv[3]): # the second should be a number of hours worth of files that we want to process
            HoursBack = sys.argv[3]

        else:
            HoursBack = 3
            writeString = "ERROR: argument 3 (hours to back process) - "+sys.argv[3]+" - is not a number. Using default "+HoursBack+" hours instead. - "+str(NowTime) + '\n'
            Write2ErrorFile(ErrorFile, writeString)

        print ("go back "+str(sys.argv[3])+" hours")

        # create timestamp for sys.argv[3] hours ago so we know which files to load
        ThenHour = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%H")
        ThenMin = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%M")
        ThenSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%S")
        ThenMicroSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%f")
        ThenTime = float(ThenHour) + float(ThenMin)/60 + float(ThenSec)/3600 + float(ThenMicroSec)/3600000000
        ThenDate = (datetime.datetime.utcnow() - timedelta(hours=float(sys.argv[3]))).strftime("%Y%m%d")
     
        header = readHeaderInfo()


        UPSDataPath = os.path.join(sys.argv[1],"Data","UPS")
        if os.path.isdir(UPSDataPath):
            UPSFileList = getFiles(UPSDataPath , "UPS", ".txt", ThenDate, ThenTime)
            UPSFileList.sort()
            for UPSfile in UPSFileList: # read in file, process into NetCDF, and write out file
                try:
                    processUPS(UPSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process weather station data - " + "UPSfile = " + str(UPSfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)


        HKeepDataPath = os.path.join(sys.argv[1],"Data","Housekeeping")
        if os.path.isdir(HKeepDataPath):
            HKeepFileList = getFiles(HKeepDataPath , "Housekeeping", ".txt", ThenDate, ThenTime)
            HKeepFileList.sort()
            for HKeepfile in HKeepFileList: # read in file, process into NetCDF, and write out file
                try:
                    processHKeep(HKeepfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process weather station data - " + "HKeepfile = " + str(HKeepfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)

        WSDataPath = os.path.join(sys.argv[1],"Data","WeatherStation")
        if os.path.isdir(WSDataPath):
            WSFileList = getFiles(WSDataPath , "WeatherStation", ".txt", ThenDate, ThenTime)
            WSFileList.sort()
            for WSfile in WSFileList: # read in file, process into NetCDF, and write out file        
                try:
                    processWS(WSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process weather station data - " + "WSfile = " + str(WSfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)

        LLDataPath = os.path.join(sys.argv[1],"Data","LaserLocking")
        if os.path.isdir(LLDataPath):
            LLFileList = getFiles(LLDataPath , "LaserLocking", ".txt", ThenDate, ThenTime)
            LLFileList.sort()
            for LLfile in LLFileList: 
                try:
                    processLL(LLfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process laser locking data - " + "LLfile = " + str(LLfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)
            EtalonFileList = getFiles(LLDataPath , "Etalon", ".txt", ThenDate, ThenTime)
            EtalonFileList.sort()
            for EtalonFile in EtalonFileList:
                try:
                    processEtalons(EtalonFile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process etalon data - " + "Etalonfile = " + str(EtalonFile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)
                    
        MCSDataPath = os.path.join(sys.argv[1],"Data","MCS")
        if os.path.isdir(MCSDataPath):
            MCSFileList = getFiles(MCSDataPath , "MCSData", ".bin", ThenDate, ThenTime)
            MCSFileList.sort()
            for MCSfile in MCSFileList:
                try:
                    processMCS(MCSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process MCS data - " + "MCSfile = " + str(MCSFile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)
            MCSPowerList = getFiles(MCSDataPath , "MCSPower", ".bin", ThenDate, ThenTime)
            MCSFileList.sort()
            MCSPowerList.sort()
            for Powerfile in MCSPowerList:
                try:
                    processPower(Powerfile,NetCDFPath,header,NowDate,NowTime,LastTime)
                except:
                    writeString = "ERROR: Failure to process Power data - " + "Powerfile = " + str(Powerfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                    Write2ErrorFile(ErrorFile, writeString)
        
        #merge into one combined file
        mergeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,LocalOutputPath,header,ErrorFile)

        #copy NetCDF files to external drive if applicable.
        copyFiles = True
        #copyFiles = False
        if copyFiles:
            print ("Copying files", datetime.datetime.utcnow().strftime("%H:%M:%S"))
            OutputPath = LocalOutputPath

            if os.path.isdir(sys.argv[2]):
                #ensure output directory exists
                OutputPath = os.path.join(sys.argv[2],"Data","")
                ensure_dir(OutputPath)
            else:
                writeString = "WARNING: argument 2 (path to external hard drive to copy data onto) - "+sys.argv[2]+" - is not a valid directory to write to. Writing to local data directory instead. - "+str(NowTime) + '\n'
                Write2ErrorFile(ErrorFile, writeString)
        
            if LocalOutputPath != OutputPath:
                #recursive_overwrite(LocalOutputPath,OutputPath,ignore=None)
                data_dirs_list = os.listdir(LocalOutputPath)
                #print (data_dirs_list)
                for data_dir in data_dirs_list:
                    print ("Copying hardware level",data_dir, datetime.datetime.utcnow().strftime("%H:%M:%S"))
                    if os.path.isfile(os.path.join(LocalOutputPath,data_dir)):
                        shutil.copy(os.path.join(LocalOutputPath,data_dir), os.path.join(OutputPath,data_dir))
                    else:
                        day_dirs_list = os.listdir(os.path.join(LocalOutputPath,data_dir))
                        for day_dir in day_dirs_list:
                            if os.path.isfile(day_dir):
                                shutil.copy(os.path.join(LocalOutputPath,data_dir,day_dir), os.path.join(OutputPath,data_dir,day_dir))
                            else:
                                if day_dir >= ThenDate:
                                    print ("Copying day level ", day_dir, datetime.datetime.utcnow().strftime("%H:%M:%S"))
                                    LocalCopyFrom = os.path.join(LocalOutputPath,data_dir,day_dir)
                                    src_file_names = ""
                                    if os.path.isfile(os.path.join(LocalOutputPath,data_dir,day_dir)):
                                        fromi = os.path.join(LocalCopyFrom,os.path.join(LocalOutputPath,data_dir,day_dir))
                                        toi = os.path.join(OutputPath,data_dir,day_dir)
                                        ensure_dir(os.path.join(OutputPath,data_dir,""))
                                        shutil.copy(fromi,toi)
                                    else:
                                        src_file_names = os.listdir(os.path.join(LocalOutputPath,data_dir,day_dir))
                                    ensure_dir(os.path.join(OutputPath,data_dir,day_dir,""))
                                    for file_name in src_file_names:
                                        if (os.path.isfile(os.path.join(LocalCopyFrom,file_name))):
                                            fromt = os.path.join(LocalCopyFrom,file_name)
                                            tot = os.path.join(OutputPath,data_dir,day_dir,"")
                                            shutil.copy(fromt,tot)

    # if os.path.isdir(os.path.join(sys.argv[1],"Data"):        
    else:
        writeString = "ERROR: argument 1 (path to directory containing Data folder) - "+sys.argv[1]+" - is not a dir, looking for directory containing Data. - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        Write2ErrorFile(ErrorFile, writeString)

    print ("Goodnight World - the date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))



if __name__ == '__main__':
    main()

