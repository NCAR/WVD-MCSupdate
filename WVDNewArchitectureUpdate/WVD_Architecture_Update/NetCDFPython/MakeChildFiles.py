
import os
import sys
import datetime
import struct

import SharedPythonFunctions as SPF

from netCDF4 import Dataset

import numpy as np
from numpy import arange, dtype


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
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))

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
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))

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

    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
    
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
                
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
    
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
                
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
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
                    WarningFile = os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),"NetCDFPythonWarnings",str(LastTime),".txt")
                    writeString = "WARNING: Power Channel Assignments changed mid file in " + Powerfile + " - " + str(NowTime) + '\n'
                    SPF.Write2ErrorFile(WarningFile, writeString)
              
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

        SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
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
                    ErrorFile = os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),"NetCDFPythonWarnings",str(LastTime),".txt")
                    writeString = "Warning: Data Channel Assignments changed mid file in " + str(MCSfile) + " - " + str(NowTime) + '\n'
                    SPF.Write2ErrorFile(ErrorFile, writeString)

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
                    ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonWarnings",str(LastTime),".txt")
                    writeString = "WARNING: channel number read from data entry does not match header - "+str(NowTime) + '\n'
                    SPF.Write2ErrorFile(ErrorFile, writeString)

                thisVal = ord(data[2:3])*2**16 + ord(data[1:2])*2**8 + ord(data[0:1])
                DataArray[v].append(thisVal)
            
            # confirming footer word was where expected
            data = file.read(4)
            ReadIndex = ReadIndex+4
            #print ("footer? = " , data)
            if ord(data[0:1]) != 255:
                ErrorFile = os.path.join(sys.argv[1],"Data","NetCDFChild",str(NowDate),"NetCDFPythonErrors",str(LastTime),".txt")
                writeString = "ERROR: Length of data frame does not match number of bins - " + str(NowTime) + '\n'
                SPF.Write2ErrorFile(ErrorFile, writeString)

            # throw away extra bits on end of data frame so next is alligned
            data = file.read(8)
            ReadIndex = ReadIndex+8
                
        SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,fileDate,""))
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
        



def makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,header):
    UPSDataPath = os.path.join(sys.argv[1],"Data","UPS")
    if os.path.isdir(UPSDataPath):
        UPSFileList = SPF.getFiles(UPSDataPath , "UPS", ".txt", ThenDate, ThenTime)
        UPSFileList.sort()
        for UPSfile in UPSFileList: # read in file, process into NetCDF, and write out file
            try:
                processUPS(UPSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "WARNING: Failure to process UPS data - " + "UPSfile = " + str(UPSfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

    HKeepDataPath = os.path.join(sys.argv[1],"Data","Housekeeping")
    if os.path.isdir(HKeepDataPath):
        HKeepFileList = SPF.getFiles(HKeepDataPath , "Housekeeping", ".txt", ThenDate, ThenTime)
        HKeepFileList.sort()
        for HKeepfile in HKeepFileList: # read in file, process into NetCDF, and write out file
            try:
                processHKeep(HKeepfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "WARNING: Failure to process Housekeeping data - " + "HKeepfile = " + str(HKeepfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

    WSDataPath = os.path.join(sys.argv[1],"Data","WeatherStation")
    if os.path.isdir(WSDataPath):
        WSFileList = SPF.getFiles(WSDataPath , "WeatherStation", ".txt", ThenDate, ThenTime)
        WSFileList.sort()
        for WSfile in WSFileList: # read in file, process into NetCDF, and write out file
            try:
                processWS(WSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "WARNING: Failure to process weather station data - " + "WSfile = " + str(WSfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

    LLDataPath = os.path.join(sys.argv[1],"Data","LaserLocking")
    if os.path.isdir(LLDataPath):
        LLFileList = SPF.getFiles(LLDataPath , "LaserLocking", ".txt", ThenDate, ThenTime)
        LLFileList.sort()
        for LLfile in LLFileList:
            try:
                processLL(LLfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "ERROR: Failure to process laser locking data - " + "LLfile = " + str(LLfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(ErrorFile, writeString)
        EtalonFileList = SPF.getFiles(LLDataPath , "Etalon", ".txt", ThenDate, ThenTime)
        EtalonFileList.sort()
        for EtalonFile in EtalonFileList:
            try:
                processEtalons(EtalonFile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "WARNING: Failure to process etalon data - " + "Etalonfile = " + str(EtalonFile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

    MCSDataPath = os.path.join(sys.argv[1],"Data","MCS")
    if os.path.isdir(MCSDataPath):
        MCSFileList = SPF.getFiles(MCSDataPath , "MCSData", ".bin", ThenDate, ThenTime)
        MCSFileList.sort()
        for MCSfile in MCSFileList:
            try:
                processMCS(MCSfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "ERROR: Failure to process MCS data - " + "MCSfile = " + str(MCSFile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(ErrorFile, writeString)
        MCSPowerList = SPF.getFiles(MCSDataPath , "MCSPower", ".bin", ThenDate, ThenTime)
        MCSFileList.sort()
        MCSPowerList.sort()
        for Powerfile in MCSPowerList:
            try:
                processPower(Powerfile,NetCDFPath,header,NowDate,NowTime,LastTime)
            except:
                writeString = "WARNING: Failure to process Power data - " + "Powerfile = " + str(Powerfile) + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)



