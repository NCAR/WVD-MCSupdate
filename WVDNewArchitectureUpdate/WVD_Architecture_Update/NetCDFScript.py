#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [how many hours back in time to process]

import os
import sys
import time
import datetime
import struct
import binascii
import math

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
               
    if len(sys.argv) > 1:# check that enough arguments were passed

        # LastHour variables used to find NetCDF Logging files for error and other logging. 
        LastHour = (datetime.datetime.now()-timedelta(hours=float(1))).strftime("%H")
        LastMin = (datetime.datetime.now()-timedelta(hours=float(1))).strftime("%M")
        LastSec = (datetime.datetime.now()-timedelta(hours=float(1))).strftime("%S")
        LastMicroSec = (datetime.datetime.now()-timedelta(hours=float(1))).strftime("%f")
        LastTime = math.ceil(float(LastHour) + float(LastMin)/60 + float(LastSec)/3600 + float(LastMicroSec)/3600000000)
        
        if os.path.isdir(sys.argv[1]+"\\Data\\"): # the first should be the directory where the Data folder is located.

            #check if NetCDF directory exists & create if needed
            NetCDFOtuputPath = sys.argv[1]+"\\Data\\NetCDFOutput\\"
            ensure_dir(NetCDFOtuputPath)
            NowDate = datetime.datetime.now().strftime("%Y%m%d")

            if is_number(sys.argv[2]): # the second should be a number of hours worth of files that we want to process
                print ("go back",sys.argv[2],"hours")

                # create datestamps for now and for sys.argv[2] hours ago so we know which files to load
                ThenDate = (datetime.datetime.now() - timedelta(hours=float(sys.argv[2]))).strftime("%Y%m%d")
                print ("Now Date = " , NowDate)
                print ("Then Date = " , ThenDate)

                # create timestamp for now so we know which files to load  
                Hour = datetime.datetime.now().strftime("%H")
                Min = datetime.datetime.now().strftime("%M")
                Sec = datetime.datetime.now().strftime("%S")
                MicroSec = datetime.datetime.now().strftime("%f")
                NowTime = float(Hour) + float(Min)/60 + float(Sec)/3600 + float(MicroSec)/3600000000

                # create timestamp for sys.argv[2] hours ago so we know which files to load
                ThenHour = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%H")
                ThenMin = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%M")
                ThenSec = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%S")
                ThenMicroSec = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%f")
                ThenTime = float(ThenHour) + float(ThenMin)/60 + float(ThenSec)/3600 + float(ThenMicroSec)/3600000000
                               
                print ("Now Time = " , NowTime)
                print ("Then Time = " , ThenTime)
                print ("Last Time = " , LastTime)
                
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
                                    
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\")
                            LLncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\LLsample"+file[-10:-4]+".nc",'w')

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
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\")
                            Etalonncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\Etalonsample"+file[-10:-4]+".nc",'w')

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
                        
                        with open(MCSfile , 'rb') as file:
                            thing = file.read()
                            file_length=len(thing)
                            file.seek(0)

                            #as i read i will add to ReadIndex based on number of bytes read
                            ReadIndex=0
                        
                            while ReadIndex+38 < file_length:
                                # there are 38 bytes in the timestamp and header combo. 
                                data = file.read(38)
                                ReadIndex = ReadIndex+38
                                TS = struct.unpack('>d',data[:8])
                                Timestamp.append(TS[0])

                                profPerHist = ord(data[23:24]) * 2**8 + ord(data[22:23])
                                ProfPerHist.append(profPerHist)

                                channel = ord(data[25:26])
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

                                cntsPerBin = ord(data[27:28]) * 2**8 + ord(data[26:27])
                                CntsPerBin.append(cntsPerBin)

                                nBins = ord(data[29:30]) * 2**8 + ord(data[28:29])
                                NBins.append(nBins)

                                rTime = ord(data[32:33])*2**16 + ord(data[31:32])*2**8 + ord(data[30:31])
                                RTime.append(rTime)

                                frameCtr = ord(data[33:34])
                                FrameCtr.append(frameCtr)

                                v=0
                                DataVal = []
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
                                        ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+NowDate+"\\NetCDFPythonErrors"+LastTime+".txt"
                                        ensure_dir(ErrorFile)
                                        fh = open(ErrorFile, "a")
                                        write("ERROR: channel number read from data entry does not match header")
                                        fh.close
                                        
                                    DataVal.append( ord(data[2:3])*2**16 + ord(data[1:2])*2**8 + ord(data[0:1] ))
                                    v=v+1
                                DataArray.append(DataVal)
            
                                # confirming footer word was where expected
                                data = file.read(4)
                                ReadIndex = ReadIndex+4

                                if ord(data[0:1]) != 255:
                                    ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+NowDate+"\\NetCDFPythonErrors"+LastTime+".txt"
                                    ensure_dir(ErrorFile)
                                    fh = open(ErrorFile, "a")
                                    write("ERROR: Length of data frame does not match number of bins")
                                    fh.close
                                # throw away extra bits on end of data frame so next is alligned
                                data = file.read(8)
                                ReadIndex = ReadIndex+8

                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+MCSfile[-19:-11]+"\\")
                            MCSncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+MCSfile[-19:-11]+"\\MCSsample"+MCSfile[-10:-4]+".nc",'w')

                            MCSncfile.createDimension('Timestamp',len(Timestamp))
                            MCSncfile.createDimension('nBins',max(NBins))
                            
                            TimestampData = MCSncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            ProfPerHistData = MCSncfile.createVariable('ProfilesPerHist',dtype('float').char,('Timestamp'))
                            ChannelData = MCSncfile.createVariable('Channel',dtype('float').char,('Timestamp'))
                            SyncData = MCSncfile.createVariable('Sync',dtype('float').char,('Timestamp'))
                            CntsPerBinData = MCSncfile.createVariable('CntsPerBin',dtype('float').char,('Timestamp'))
                            NBinsData = MCSncfile.createVariable('NBins',dtype('float').char,('Timestamp'))
                            RTimeData = MCSncfile.createVariable('RTime',dtype('float').char,('Timestamp'))
                            FrameCtrData = MCSncfile.createVariable('FrameCtr',dtype('float').char,('Timestamp'))
                            DataArrayData = MCSncfile.createVariable('DataArray',dtype('float').char,('Timestamp','nBins'))

                            TimestampData[:] = Timestamp
                            ProfPerHistData[:] = ProfPerHist
                            ChannelData[:] = Channel
                            SyncData[:] = Sync
                            CntsPerBinData[:] = CntsPerBin
                            NBinsData[:] = NBins
                            RTimeData[:] = RTime
                            FrameCtrData[:] = FrameCtr
                            DataArrayData[:] = DataArray

                            MCSncfile.description = "MCS sample file"

                            TimestampData.units = "Fractional Hours"
                            ProfPerHistData.units = "n shots per histogram"
                            ChannelData.units = "Channel number"
                            CntsPerBinData.units = "MCS Clock Counts per bin"
                            NBinsData.units = "n Bins"
                            RTimeData.units = "ms operational"
                            FrameCtrData.units = "n Frames processed"
                            DataArrayData.units = "Photon Counts Returned"
                            
                            MCSncfile.close()

                    # read in and process power files
                    for Powerfile in MCSPowerList:
                        Timestamp = []
                        PowerCh = []

                        nChannels = 12
                        
                        i=0
                        while i < nChannels:
                            i=i+1
                            PowerCh.append([])
                        
                        with open(Powerfile, "rb") as file:
                            file.seek(0)  # Go to beginning

                            # k is the number of entries in the power file. Each power entry is 86 bytes long. 
                            k=0
                            while k < (os.path.getsize(Powerfile))/86:
                                k = k + 1

                                couple_bytes = file.read(86)

                                TS = struct.unpack('>d',couple_bytes[:8])
                                Timestamp.append(TS[0])

                                j=0
                                while j < nChannels:
                                    a = ord(couple_bytes[4*j+26:4*j+27])
                                    b = ord(couple_bytes[4*j+27:4*j+28])*2**8
                                    c = ord(couple_bytes[4*j+28:4*j+29])*2**16
                                    d = ord(couple_bytes[4*j+29:4*j+30])*2**24 
                                    PowerCh[j].append( a + b + c + d )
                                    j=j+1
                            
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+Powerfile[-19:-11]+"\\")
                            Powncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+Powerfile[-19:-11]+"\\Powsample"+Powerfile[-10:-4]+".nc",'w')

                            Powncfile.createDimension('Timestamp',len(Timestamp))
                            Powncfile.createDimension('nChannels',nChannels)
                            
                            TimestampData = Powncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            PowChData = Powncfile.createVariable('PowerChan',dtype('float').char,('Timestamp','nChannels'))

                            TimestampData[:] = Timestamp
                            PowChData[:] = PowerCh

                            Powncfile.description = "Power sample file"

                            TimestampData.units = "Fractional Hours"
                            PowChData.units = "PIN count"
                                                                             
                            Powncfile.close()

                                    
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
                                    
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\")
                            WSncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc",'w')

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

            # if is_number(sys.argv[2]):
            else:
                ErrorFile = sys.argv[1]+"\\Data\\NetCDFChild\\"+NowDate+"\\NetCDFPythonErrors"+LastTime+".txt"
                ensure_dir(ErrorFile)
                fh = open(ErrorFile, "a")
                write("ERROR:", sys.argv[1],"is a dir, but",sys.argv[2],"is not a number")
                fh.close
           
        # if os.path.isdir(sys.argv[1]+"\\Data\\"):        
        else:
            ErrorFile = sys.argv[1]+"\\NetCDFPythonErrors"+LastTime+".txt"
            ensure_dir(ErrorFile)
            fh = open(ErrorFile, "a")
            write("ERROR: ",sys.argv[1],"is not a dir, looking for directory containing Data")
            fh.close
            print (sys.argv[1],"is not a dir, looking for directory containing Data")

    print ("Goodnight World - the date and time is - ", datetime.datetime.now().strftime("%H:%M:%S:%f"))

if __name__ == '__main__':
    main()

