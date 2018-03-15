#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [location to write files] [how many hours back in time to process]

import os
import sys
import time
import datetime
import struct
import binascii
import math
import shutil
import numpy as np
from datetime import timedelta 
from netCDF4 import Dataset
from numpy import arange, dtype # array module from http://numpy.scipy.org

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

#MCS data is in binary format while others are in txt format. That is why we need dataname (the beginning of the names of the files) and the data type (to ensure proper extention) 
def getFiles(DataPath, dataname, datatype, ThenDate, ThenTime):
    DayList = os.listdir(DataPath)
    FileList = [] # will hold list of files needing to be processed

    for day in DayList:
        TempFileList = os.listdir(DataPath + day)
        if float(day) == float(ThenDate):
            for file in TempFileList:
                if file[:len(dataname)] == dataname and file[-4:] == datatype:
                    if float(file[-10:-4])/10000 > ThenTime:
                        FileList.append(DataPath + day + "\\" + file)
        elif float(day) > float(ThenDate):
            for file in TempFileList:
                if file[:len(dataname)] == dataname and file[-4:] == datatype:
                    FileList.append(DataPath + day + "\\" + file)
    return FileList
                                    
        
        
# --------------------------------main------------------------------------
def main():
    print ("Hello World - the date and time is - ", datetime.datetime.now().strftime("%H:%M:%S:%f"))
    # create timestamp for now so we know which files to load
    Hour = datetime.datetime.utcnow().strftime("%H")
    Min = datetime.datetime.utcnow().strftime("%M")
    Sec = datetime.datetime.utcnow().strftime("%S")
    MicroSec = datetime.datetime.utcnow().strftime("%f")
    NowTime = float(Hour) + float(Min)/60 + float(Sec)/3600 + float(MicroSec)/3600000000
    NowDate = datetime.datetime.now().strftime("%Y%m%d")

    if len(sys.argv) > 1:# check that enough arguments were passed

        # LastHour variables used to find NetCDF Logging files for error and other logging. 
        LastHour = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%H")
        LastMin = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%M")
        LastSec = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%S")
        LastMicroSec = (datetime.datetime.utcnow()-timedelta(hours=float(1))).strftime("%f")
        LastTime = math.ceil(float(LastHour) + float(LastMin)/60 + float(LastSec)/3600 + float(LastMicroSec)/3600000000)
        
        if os.path.isdir(sys.argv[1]+"\\Data\\"): # the first should be the directory where the Data folder is located.

            LocalNetCDFOutputPath = sys.argv[1]+"\\Data\\"+"\\NetCDFOutput\\"
            ensure_dir(LocalNetCDFOutputPath)

            NetCDFOutputPath = LocalNetCDFOutputPath
            if os.path.isdir(sys.argv[2]):
                #ensure output directory exists
                NetCDFOutputPath = sys.argv[1]+"\\NetCDFOutput\\"
                ensure_dir(NetCDFOutputPath)
            else:
                ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+NowDate+"\\NetCDFPythonErrors"+LastTime+".txt"
                ensure_dir(ErrorFile)
                fh = open(ErrorFile, "a")
                write("WARNING: argument 2 - ",sys.argv[2]," - is not a dir to write to. Writing to local data directory instead. - ",NowTime)
                fh.close


            if is_number(sys.argv[3]): # the second should be a number of hours worth of files that we want to process
                print ("go back",sys.argv[3],"hours")

                # create timestamp for sys.argv[3] hours ago so we know which files to load
                ThenHour = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%H")
                ThenMin = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%M")
                ThenSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%S")
                ThenMicroSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%f")
                ThenTime = float(ThenHour) + float(ThenMin)/60 + float(ThenSec)/3600 + float(ThenMicroSec)/3600000000
                ThenDate = (datetime.datetime.utcnow() - timedelta(hours=float(sys.argv[3]))).strftime("%Y%m%d")
                
                print ("Now Date = " , NowDate)
                print ("Then Date = " , ThenDate)          
                print ("Now Time = " , NowTime)
                print ("Then Time = " , ThenTime)
                print ("Last Time = " , LastTime)
                                             
                # ----------------------- Weather Station ------------------
                WSDataPath = sys.argv[1]+"\\Data\\"+"WeatherStation\\"
                if os.path.isdir(WSDataPath):
                    print (WSDataPath)

                    WSFileList = getFiles(WSDataPath , "WeatherStation", ".txt", ThenDate, ThenTime)
                                
                    for file in WSFileList: # read in file, process into NetCDF, and write out file
                        Temperature = []
                        RelHum = []
                        Pressure = []
                        AbsHum = []
                        Timestamp = []
                                                
                        with open(file) as f:
                            for line in f:
                                linelist = line.split()
                                if len(linelist) == 5:
                                    Temperature.append(linelist[0])
                                    RelHum.append(linelist[1])
                                    Pressure.append(linelist[2])
                                    AbsHum.append(linelist[3])
                                    Timestamp.append(linelist[4])
                                    
                            ensure_dir(NetCDFOutputPath+file[-19:-11]+"\\")
                            ensure_dir(LocalNetCDFOutputPath+file[-19:-11]+"\\")
                            WSncfile = Dataset(LocalNetCDFOutputPath+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc",'w')

                            WSncfile.createDimension('Timestamp',len(Timestamp))

                            TimestampData = WSncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            TemperatureData = WSncfile.createVariable('Temperature',dtype('float').char,('Timestamp'))
                            RelHumData = WSncfile.createVariable('RelHum',dtype('float').char,('Timestamp'))
                            PressureData = WSncfile.createVariable('Pressure',dtype('float').char,('Timestamp'))
                            AbsHumData = WSncfile.createVariable('AbsHum',dtype('float').char,('Timestamp'))

                            TimestampData[:] = Timestamp
                            TemperatureData[:] = Temperature
                            RelHumData[:] = RelHum
                            PressureData[:] = Pressure
                            AbsHumData[:] = AbsHum

                            WSncfile.description = "WSsample file"
                            
                            TimestampData.units = "Fractional Hours"
                            TemperatureData.units = "C"
                            RelHumData.units = "%"
                            PressureData.units = "mb"
                            AbsHumData.units = "g/kg"
                            
                            WSncfile.close()


                # ----------------------- Laser Locking ------------------
                LLDataPath = sys.argv[1]+"\\Data\\"+"LaserLocking\\"
                if os.path.isdir(LLDataPath):
                    print (LLDataPath)

                    LLDayList = os.listdir(LLDataPath)

                    LLFileList = getFiles(LLDataPath , "LaserLocking", ".txt", ThenDate, ThenTime)
                    EtalonFileList = getFiles(LLDataPath , "Etalon", ".txt", ThenDate, ThenTime)

                    # read in laser locking file, process into NetCDF, and write out file
                    for file in LLFileList: 
                        LaserNum = []
                        Wavelength = []
                        WaveDiff = []
                        IsLocked = []
                        TempDesired = []
                        TempMeas = []
                        Current = []
                        Timestamp = []
                        Datestamp = []
                        
                        #read in file line by line
                        with open(file) as f:
                            for line in f:
                                # split up the line into numbers in list
                                linelist = line.split()
                                # making sure the line has the appropriate number of entries for the expected format
                                if len(linelist) == 9: 
                                    LaserNum.append(linelist[0])
                                    Wavelength.append(linelist[1])
                                    WaveDiff.append(linelist[2])
                                    IsLocked.append(linelist[3])
                                    TempDesired.append(linelist[4])
                                    TempMeas.append(linelist[5])
                                    Current.append(linelist[6])
                                    Timestamp.append(linelist[7])
                                    Datestamp.append(linelist[8])

                            ensure_dir(NetCDFOutputPath+file[-19:-11]+"\\")
                            ensure_dir(LocalNetCDFOutputPath+file[-19:-11]+"\\")
                            LLncfile = Dataset(LocalNetCDFOutputPath+file[-19:-11]+"\\LLsample"+file[-10:-4]+".nc",'w')

                            # create the time dimention
                            LLncfile.createDimension('Timestamp',len(Timestamp))

                            # add in variables that are expected to be the same size as timestamp which is the master dimension 
                            TimestampData = LLncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            DatestampData = LLncfile.createVariable('Datestamp',dtype('float').char,('Timestamp'))
                            LaserNumData = LLncfile.createVariable('LaserNum',dtype('float').char,('Timestamp'))
                            WavelengthData = LLncfile.createVariable('Wavelength',dtype('float').char,('Timestamp'))
                            WaveDiffData = LLncfile.createVariable('WaveDiff',dtype('float').char,('Timestamp'))
                            IsLockedData = LLncfile.createVariable('IsLocked',dtype('float').char,('Timestamp'))
                            TempDesiredData = LLncfile.createVariable('TempDesired',dtype('float').char,('Timestamp'))
                            TempMeasData = LLncfile.createVariable('TempMeas',dtype('float').char,('Timestamp'))
                            CurrentData = LLncfile.createVariable('Current',dtype('float').char,('Timestamp'))

                            # filling the variables that are now in the NetCDF file
                            TimestampData[:] = Timestamp
                            DatestampData[:] = Datestamp
                            LaserNumData[:] = LaserNum
                            WavelengthData[:] = Wavelength
                            WaveDiffData[:] = WaveDiff
                            IsLockedData[:] = IsLocked
                            TempDesiredData[:] = TempDesired
                            TempMeasData[:] = TempMeas
                            CurrentData[:] = Current

                            LLncfile.description = "Laser Locking sample file"

                            TimestampData.units = "Fractional Hours"
                            DatestampData.units = "yyyymmdd"
                            WavelengthData.units = "nm"
                            WaveDiffData.units = "nm"
                            TempDesiredData.units = "C"
                            TempMeasData.units = "C"
                            CurrentData.units = "amp"

                            LLncfile.close()

                    # read in file, process into NetCDF, and write out file
                    for file in EtalonFileList: 
                        EtalonNum = []
                        Temperature = []
                        TempDiff = []
                        IsLocked = []
                        Timestamp = []
                        Datestamp = []

                        with open(file) as f:
                            for line in f:
                                linelist = line.split()
                                if len(linelist) == 6:
                                    EtalonNum.append(linelist[0])
                                    Temperature.append(linelist[1])
                                    TempDiff.append(linelist[2])
                                    IsLocked.append(linelist[3])
                                    Timestamp.append(linelist[4])
                                    Datestamp.append(linelist[5]) 

                            ensure_dir(NetCDFOutputPath+file[-19:-11]+"\\")
                            ensure_dir(LocalNetCDFOutputPath+file[-19:-11]+"\\")
                            Etalonncfile = Dataset(LocalNetCDFOutputPath+file[-19:-11]+"\\Etalonsample"+file[-10:-4]+".nc",'w')

                            Etalonncfile.createDimension('Timestamp',len(Timestamp))

                            TimestampData = Etalonncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            DatestampData = Etalonncfile.createVariable('Datestamp',dtype('float').char,('Timestamp'))
                            EtalonNumData = Etalonncfile.createVariable('EtalonNum',dtype('float').char,('Timestamp'))
                            TemperatureData = Etalonncfile.createVariable('Temperature',dtype('float').char,('Timestamp'))
                            TempDiffData = Etalonncfile.createVariable('TempDiff',dtype('float').char,('Timestamp'))
                            IsLockedData = Etalonncfile.createVariable('IsLocked',dtype('float').char,('Timestamp'))

                            TimestampData[:] = Timestamp
                            DatestampData[:] = Datestamp
                            EtalonNumData[:] = EtalonNum
                            TemperatureData[:] = Temperature
                            TempDiffData[:] = TempDiff
                            IsLockedData[:] = IsLocked

                            Etalonncfile.description = "Etalon sample file"

                            TimestampData.units = "Fractional Hours"
                            DatestampData.units = "yyyymmdd"
                            EtalonNumData.units = "Assigned Etalon Number"
                            TemperatureData.units = "C"
                            TempDiffData.units = "C"

                            Etalonncfile.close()
                                    
                # ----------------------- MCS ------------------
                MCSDataPath = sys.argv[1]+"\\Data\\"+"MCS\\"
                if os.path.isdir(MCSDataPath):
                    print (MCSDataPath)
                    
                    MCSDayList = os.listdir(MCSDataPath)
                    MCSFileList = getFiles(MCSDataPath , "MCSData", ".bin", ThenDate, ThenTime)
                    MCSPowerList = getFiles(MCSDataPath , "MCSPower", ".bin", ThenDate, ThenTime)

                    # read in and process power files
                    for Powerfile in MCSPowerList:
                        Timestamp = []
                        PowerCh = []
                        HSRLPowCh = 0
                        OnlineH2OCh = 0
                        OfflineH2OCh = 0
                        OnlineO2Ch = 0
                        OfflineO2Ch = 0

                        nChannels = 12
                        
                        i=0
                        while i < nChannels:
                            i=i+1
                            PowerCh.append([])
                        
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
                                        ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+str(NowDate)+"\\NetCDFPythonErrors"+str(LastTime)+".txt"
                                        ensure_dir(ErrorFile)
                                        fh = open(ErrorFile, "a")
                                        fh.write("ERROR: Power Channel Assignments changed mid file in " + Powerfile + " - " + str(NowTime))
                                        fh.close    
                                        
                                HSRLPowCh = ord(couple_bytes[23:24])-48
                                OnlineH2OCh = ord(couple_bytes[34:35])-48 
                                OfflineH2OCh = ord(couple_bytes[46:47])-48
                                OnlineO2Ch = ord(couple_bytes[56:57])-48
                                OfflineO2Ch = ord(couple_bytes[67:68])-48
                                
                                TS = struct.unpack('>d',couple_bytes[:8])
                                Timestamp.append(TS[0])

                                j=0
                                while j < nChannels:
                                    a = ord(couple_bytes[4*j+82:4*j+83])
                                    b = ord(couple_bytes[4*j+83:4*j+84])*2**8
                                    c = ord(couple_bytes[4*j+84:4*j+85])*2**16
                                    d = ord(couple_bytes[4*j+85:4*j+86])*2**24
                                    PowerCh[j].append( a + b + c + d )
                                    j=j+1

                            ensure_dir(NetCDFOutputPath+Powerfile[-19:-11]+"\\")
                            ensure_dir(LocalNetCDFOutputPath+Powerfile[-19:-11]+"\\")
                            Powncfile = Dataset(LocalNetCDFOutputPath+Powerfile[-19:-11]+"\\Powsample"+Powerfile[-10:-4]+".nc",'w')

                            Powncfile.createDimension('Timestamp',len(Timestamp))
                            Powncfile.createDimension('nChannels',nChannels)
                            
                            TimestampData = Powncfile.createVariable('Timestamp',dtype('float32').char,('Timestamp'))
                            PowChData = Powncfile.createVariable('PowerChan',dtype('float32').char,('Timestamp','nChannels'))
                            HSRLPowChData = Powncfile.createVariable('HSRLPowCh',dtype('int').char,())
                            OnlineH2OChData = Powncfile.createVariable('OnlineH2OChannel',dtype('int').char,())
                            OfflineH2OChData = Powncfile.createVariable('OfflineH2OChannel',dtype('int').char,())
                            OnlineO2ChData = Powncfile.createVariable('OnlineO2Channel',dtype('int').char,())
                            OfflineO2ChData = Powncfile.createVariable('OfflineO2Channel',dtype('int').char,())
                                                            
                            TimestampData[:] = Timestamp
                            PowChData[:] = PowerCh
                            HSRLPowChData[:] = HSRLPowCh
                            OnlineH2OChData[:] = OnlineH2OCh
                            OfflineH2OChData[:] = OfflineH2OCh
                            OnlineO2ChData[:] = OnlineO2Ch
                            OfflineO2ChData[:] = OfflineO2Ch
                            
                            Powncfile.description = "Power sample file"

                            TimestampData.units = "Fractional Hours"
                            PowChData.units = "PIN count"
                                        
                            HSRLPowChData.description = "MCS Power Channel Assignment for HSRL"
                            OnlineH2OChData.description = "MCS Power Channel Assignment for H2O Online"
                            OfflineH2OChData.description = "MCS Power Channel Assignment for H2O Offline"
                            OnlineO2ChData.description = "MCS Power Channel Assignment for O2 Online"
                            OfflineO2ChData.description = "MCS Power Channel Assignment for O2 Offline"
                                                                
                            Powncfile.close()

                    # read in and process MCS Data files
                    for MCSfile in MCSFileList:

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
                        
                        OnlineH2OCh = 0 
                        OfflineH2OCh = 0
                        CombinedHSRLCh = 0
                        MolecularHSRLCh = 0
                        OnlineO2Ch = 0
                        OfflineO2Ch = 0
                        
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
                                        ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+str(NowDate)+"\\NetCDFPythonErrors"+str(LastTime)+".txt"
                                        ensure_dir(ErrorFile)
                                        fh = open(ErrorFile, "a")
                                        fh.write("ERROR: Data Channel Assignments changed mid file in " + file + " - " + str(NowTime))
                                        fh.close    
  
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

                                profPerHist = ord(data[112:113]) * 2**8 + ord(data[111:112])
                                #print (profPerHist)
                                ProfPerHist.append(profPerHist)

                                channel = ord(data[114:115])
                                sync = 0;
                                #seperating sync bits from channel
                                if(channel >= 128):
                                    channel = channel - 128
                                    sync = sync + 2
                                if(channel >= 64):
                                    channel = channel - 64
                                    sync = sync + 1
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

                                v=0
                                DataVal = []
                                np.array(DataVal,dtype='f')

                                while v < nBins:
                                    data = file.read(4)
                                    ReadIndex = ReadIndex+4

                                    chan = ord(data[3:4])
                                    # it looks like the sync variable is making it into data frames
                                    # which is not in line with Josh's documentation
                                    if(chan >= 128):
                                        chan = chan - 128
                                    if(chan >= 64):
                                        chan = chan - 64
                                     
                                    if chan != channel:
                                        print (str(sys.argv[1]))
                                        print (str(NowDate))
                                        print (str(LastTime))
                                        ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+str(NowDate)+"\\NetCDFPythonErrors"+str(LastTime)+".txt"
                                        ensure_dir(ErrorFile)
                                        fh = open(ErrorFile, "a")
                                        write("ERROR: channel number read from data entry does not match header - ",NowTime)
                                        fh.close
                                        
                                    DataVal.append(ord(data[2:3])*2**16 + ord(data[1:2])*2**8 + ord(data[0:1]))
                                    v=v+1
                                DataArray.append(DataVal)
            
                                # confirming footer word was where expected
                                data = file.read(4)
                                ReadIndex = ReadIndex+4
                                #print ("footer? = " , data)
                                if ord(data[0:1]) != 255:
                                    ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+str(NowDate)+"\\NetCDFPythonErrors"+str(LastTime)+".txt"
                                    ensure_dir(ErrorFile)
                                    fh = open(ErrorFile, "a")
                                    fh.write("ERROR: Length of data frame does not match number of bins - " + str(NowTime))
                                    fh.close
                                # throw away extra bits on end of data frame so next is alligned
                                data = file.read(8)
                                ReadIndex = ReadIndex+8

                            ensure_dir(NetCDFOutputPath+MCSfile[-19:-11]+"\\")
                            ensure_dir(LocalNetCDFOutputPath+MCSfile[-19:-11]+"\\")
                            MCSncfile = Dataset(LocalNetCDFOutputPath+MCSfile[-19:-11]+"\\MCSsample"+MCSfile[-10:-4]+".nc",'w')

                            MCSncfile.createDimension('Timestamp',len(Timestamp))
                            MCSncfile.createDimension('nBins',max(NBins))
                            
                            TimestampData = MCSncfile.createVariable('Timestamp',dtype('float32').char,('Timestamp'))
                            ProfPerHistData = MCSncfile.createVariable('ProfilesPerHist',dtype('float32').char,('Timestamp'))
                            ChannelData = MCSncfile.createVariable('Channel',dtype('float32').char,('Timestamp'))
                            SyncData = MCSncfile.createVariable('Sync',dtype('float32').char,('Timestamp'))
                            CntsPerBinData = MCSncfile.createVariable('CntsPerBin',dtype('float32').char,('Timestamp'))
                            NBinsData = MCSncfile.createVariable('NBins',dtype('float32').char,('Timestamp'))
                            RTimeData = MCSncfile.createVariable('RTime',dtype('float32').char,('Timestamp'))
                            FrameCtrData = MCSncfile.createVariable('FrameCtr',dtype('float32').char,('Timestamp'))
                            DataArrayData = MCSncfile.createVariable('DataArray',dtype('float32').char,('nBins','Timestamp'))
                            OnlineH2OChData = MCSncfile.createVariable('OnlineH2OCh',dtype('int').char,())
                            OfflineH2OChData = MCSncfile.createVariable('OfflineH2OCh',dtype('int').char,())
                            CombinedHSRLChData = MCSncfile.createVariable('CombinedHSRLCh',dtype('int').char,())
                            MolecularHSRLChData = MCSncfile.createVariable('MolecularHSRLCh',dtype('int').char,())
                            OnlineO2ChData = MCSncfile.createVariable('OnlineO2Ch',dtype('int').char,())
                            OfflineO2ChData = MCSncfile.createVariable('OfflineO2Ch',dtype('int').char,())

                            TimestampData[:] = Timestamp
                            ProfPerHistData[:] = ProfPerHist
                            ChannelData[:] = Channel
                            SyncData[:] = Sync
                            CntsPerBinData[:] = CntsPerBin
                            NBinsData[:] = NBins
                            RTimeData[:] = RTime
                            FrameCtrData[:] = FrameCtr
                            DataArrayData[:] = DataArray
                            OnlineH2OChData[:] = OnlineH2OCh
                            OfflineH2OChData[:] = OfflineH2OCh
                            CombinedHSRLChData[:] = CombinedHSRLCh
                            MolecularHSRLChData[:] = MolecularHSRLCh
                            OnlineO2ChData[:] = OnlineO2Ch
                            OfflineO2ChData[:] = OfflineO2Ch

                            MCSncfile.description = "MCS sample file"

                            TimestampData.units = "Fractional Hours"
                            ProfPerHistData.units = "n shots per histogram"
                            ChannelData.units = "Channel number"
                            CntsPerBinData.units = "MCS Clock Counts per bin"
                            NBinsData.units = "n Bins"
                            RTimeData.units = "ms operational"
                            FrameCtrData.units = "n Frames processed"
                            DataArrayData.units = "Photon Counts Returned"
                            
                            OnlineH2OChData.description = "MCS Channel Assignment for H2O Online"
                            OfflineH2OChData.description = "MCS Channel Assignment for H2O Offline"
                            CombinedHSRLChData.description = "MCS Channel Assignment for HSRL Combined"
                            MolecularHSRLChData.description = "MCS Channel Assignment for HSRL Molecular"
                            OnlineO2ChData.description = "MCS Channel Assignment for O2 Online"
                            OfflineO2ChData.description = "MCS Channel Assignment for O2 Online"
                            
                            MCSncfile.close()
       
            if LocalNetCDFOutputPath != NetCDFOutputPath:
                #print ("in here")
                day_dirs_list = os.listdir(LocalNetCDFOutputPath)
                for day_dir in day_dirs_list:
                    #print (day_dir)
                    src_file_names = os.listdir(LocalNetCDFOutputPath+day_dir)
                    ensure_dir(NetCDFOutputPath+day_dir)
                    for file_name in src_file_names:
                        full_file_name = os.path.join(LocalNetCDFOutputPath+day_dir, file_name)
                        if (os.path.isfile(full_file_name)):
                            #print (full_file_name)
                            #print (NetCDFOutputPath+day_dir)
                            shutil.copy(full_file_name, NetCDFOutputPath+day_dir)
        
            # if is_number(sys.argv[3]):
            else:
                ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+NowDate+"\\NetCDFPythonErrors"+LastTime+".txt"
                ensure_dir(ErrorFile)
                fh = open(ErrorFile, "a")
                write("ERROR: argument 3 - ",sys.argv[3]," - is not a number. - ",NowTime)
                fh.close

        # if os.path.isdir(sys.argv[1]+"\\Data\\"):        
        else:
            ErrorFile = sys.argv[1]+"\\NetCDFPythonErrors"+LastTime+".txt"
            ensure_dir(ErrorFile)
            fh = open(ErrorFile, "a")
            write("ERROR: argument 1 - ",sys.argv[1]," - is not a dir, looking for directory containing Data. - ",NowTime)
            fh.close
            print (sys.argv[1],"is not a dir, looking for directory containing Data")

    print ("Goodnight World - the date and time is - ", datetime.datetime.now().strftime("%H:%M:%S:%f"))

if __name__ == '__main__':
    main()

