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
import numpy

from ast import literal_eval

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
        
        
# --------------------------------main------------------------------------
def main():
    print ("Hello World - the date and time is - ", datetime.datetime.now().strftime("%H:%M:%S:%f"))
    print ("These are the arguments I passed in to my test script:")
    for i in range(0,len(sys.argv)-1):
        print (sys.argv[i+1])
           
    if len(sys.argv) > 1:# check that enough arguments were passed
        if os.path.isdir(sys.argv[1]+"\\Data\\"): # the first should be the directory where the Data folder is located.
            if is_number(sys.argv[2]): # the second should be a number of hours worth of files that we want to process
                print ("go back",sys.argv[2],"hours")
                
                #check if NetCDF directory exists & create if needed
                NetCDFOtuputPath = sys.argv[1]+"\\Data\\NetCDFOutput\\"
                ensure_dir(NetCDFOtuputPath)

                # create timestamps and datestamps for now, and for sys.argv[2] hours ago so we know which files to load
                NowDate = datetime.datetime.now().strftime("%Y%m%d")
                ThenDate = (datetime.datetime.now() - timedelta(hours=float(sys.argv[2]))).strftime("%Y%m%d")
                print ("Now Date = " , NowDate)
                print ("Then Date = " , ThenDate)
                    
                Hour = datetime.datetime.now().strftime("%H")
                Min = datetime.datetime.now().strftime("%M")
                Sec = datetime.datetime.now().strftime("%S")
                MicroSec = datetime.datetime.now().strftime("%f")
                NowTime = float(Hour) + float(Min)/60 + float(Sec)/3600 + float(MicroSec)/3600000000

                ThenHour = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%H")
                ThenMin = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%M")
                ThenSec = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%S")
                ThenMicroSec = (datetime.datetime.now()-timedelta(hours=float(sys.argv[2]))).strftime("%f")
                ThenTime = float(ThenHour) + float(ThenMin)/60 + float(ThenSec)/3600 + float(ThenMicroSec)/3600000000
                  
                print ("Now Time = " , NowTime )
                print ("Then Time = " , ThenTime)

                # ----------------------- Laser Locking ------------------
                #check for children data dirs
                LLDataPath = sys.argv[1]+"\\Data\\"+"LaserLocking\\"
                if os.path.isdir(LLDataPath):
                    print (LLDataPath)

                    LLDayList = os.listdir(LLDataPath)
                    LLFileList = [] # will hold list of files needing to be processed
                    EtalonFileList = [] # will hold list of files needing to be processed
                    for day in LLDayList:
                        TempFileList = os.listdir(LLDataPath + day)
                        #print (TempFileList)
                        if float(day) == float(ThenDate):
                            for file in TempFileList:
                                if file[:12] == "LaserLocking":
                                    if float(file[-10:-4]) > ThenTime:
                                        LLFileList.append(LLDataPath + day + "\\" + file)
                                elif file[:6] == "Etalon":
                                    if float(file[-10:-4]) > ThenTime:
                                        EtalonFileList.append(LLDataPath + day + "\\" + file)
                        elif float(day) > float(ThenDate):
                            for file in TempFileList:
                                if file[:12] == "LaserLocking":
                                    LLFileList.append(LLDataPath + day + "\\" + file)
                                elif file[:6] == "Etalon":
                                    EtalonFileList.append(LLDataPath + day + "\\" + file)

                    #print (LLFileList)
                    for file in LLFileList: # read in file, process into NetCDF, and write out file
                        #print (file)
                        LaserNum = []
                        Wavelength = []
                        WaveDiff = []
                        IsLocked = []
                        Current = []
                        CurrDiff = []
                        Timestamp = []

                        with open(file) as f:
                            for line in f:
                                linelist = line.split()
                                if len(linelist) == 8:
                                    LaserNum.append(linelist[0])
                                    Wavelength.append(linelist[1])
                                    WaveDiff.append(linelist[2])
                                    IsLocked.append(linelist[3])
                                    Current.append(linelist[4])
                                    CurrDiff.append(linelist[5])
                                    Timestamp.append(linelist[6])
                                    # linelist[7] is date, but that is not needed. 
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\")
                            #print (sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc")
                            LLncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\LLsample"+file[-10:-4]+".nc",'w')

                            LLncfile.createDimension('Timestamp',len(Timestamp))

                            TimestampData = LLncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            LaserNumData = LLncfile.createVariable('LaserNum',dtype('float').char,('Timestamp'))
                            WavelengthData = LLncfile.createVariable('Wavelength',dtype('float').char,('Timestamp'))
                            WaveDiffData = LLncfile.createVariable('WaveDiff',dtype('float').char,('Timestamp'))
                            IsLockedData = LLncfile.createVariable('IsLocked',dtype('float').char,('Timestamp'))
                            CurrentData = LLncfile.createVariable('Current',dtype('float').char,('Timestamp'))
                            CurrDiffData = LLncfile.createVariable('CurrDiff',dtype('float').char,('Timestamp'))

                            TimestampData[:] = Timestamp
                            LaserNumData[:] = LaserNum
                            WavelengthData[:] = Wavelength
                            WaveDiffData[:] = WaveDiff
                            IsLockedData[:] = IsLocked
                            CurrentData[:] = Current
                            CurrDiffData[:] = CurrDiff
                            
                            LLncfile.close()

                    #print (EtalonFileList)
                    for file in EtalonFileList: # read in file, process into NetCDF, and write out file
                        #print (file)
                        EtalonNum = []
                        Temperature = []
                        TempDiff = []
                        IsLocked = []
                        Timestamp = []

                        with open(file) as f:
                            for line in f:
                                linelist = line.split()
                                if len(linelist) == 6:
                                    EtalonNum.append(linelist[0])
                                    Temperature.append(linelist[1])
                                    TempDiff.append(linelist[2])
                                    IsLocked.append(linelist[3])
                                    Timestamp.append(linelist[4])
                                    # linelist[5] is date, but that is not needed. 
                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\")
                            #print (sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc")
                            Etalonncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\Etalonsample"+file[-10:-4]+".nc",'w')

                            Etalonncfile.createDimension('Timestamp',len(Timestamp))

                            TimestampData = Etalonncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            EtalonNumData = Etalonncfile.createVariable('EtalonNum',dtype('float').char,('Timestamp'))
                            TemperatureData = Etalonncfile.createVariable('Temperature',dtype('float').char,('Timestamp'))
                            TempDiffData = Etalonncfile.createVariable('TempDiff',dtype('float').char,('Timestamp'))
                            IsLockedData = Etalonncfile.createVariable('IsLocked',dtype('float').char,('Timestamp'))

                            TimestampData[:] = Timestamp
                            EtalonNumData[:] = EtalonNum
                            TemperatureData[:] = Temperature
                            TempDiffData[:] = TempDiff
                            IsLockedData[:] = IsLocked
                            
                            Etalonncfile.close()
                                    
                # ----------------------- MCS ------------------
                MCSDataPath = sys.argv[1]+"\\Data\\"+"MCS\\"
                if os.path.isdir(MCSDataPath):
                    print (MCSDataPath)

                    MCSDayList = os.listdir(MCSDataPath)
                    MCSFileList = [] # will hold list of files needing to be processed
                    MCSPowerList = [] 
                    for day in MCSDayList:
                        TempFileList = os.listdir(MCSDataPath + day)
                        if float(day) == float(ThenDate):
                            for file in TempFileList:
                                if file[:7] == "MCSData" and file[-4:] == ".bin":
                                    if float(file[-10:-4]) > ThenTime:
                                        MCSFileList.append(MCSDataPath + day + "\\" + file)
                                elif file[:8] == "MCSPower" and file[-4:] == ".bin":
                                    if float(file[-10:-4]) > ThenTime:
                                        MCSPowerList.append(MCSDataPath + day + "\\" + file)
                        elif float(day) > float(ThenDate):
                            for file in TempFileList:
                                if file[:7] == "MCSData" and file[-4:] == ".bin":
                                    MCSFileList.append(MCSDataPath + day + "\\" + file)
                                elif file[:8] == "MCSPower" and file[-4:] == ".bin":
                                    MCSPowerList.append(MCSDataPath + day + "\\" + file)
                    #print (MCSFileList)
                    #print (MCSPowerList)

                    y=0
                    for MCSfile in MCSFileList:
                        y=y+1
                        Timestamp = []
                        with open(MCSfile , 'rb') as file:
                            if y == 1 :
                                data = file.read(25)
                                print (data)
                                #print (struct.unpack('f', file.read(8)))
                            Timestamp.append(0)







                        
                    for Powerfile in MCSPowerList:
                        Timestamp = []
                        PowerCh = []
                        i=0
                        while i < 12:
                            i=i+1
                            PowerCh.append([])
                        
                        with open(Powerfile, "rb") as file:
                            file.seek(0)  # Go to beginning
                            i=0
                            while i < (os.path.getsize(Powerfile))/86:
                                i = i + 1
                                couple_bytes = file.read(86)
                                j=0
                                while j < 12:
                                    a = ord(couple_bytes[4*j+26:4*j+27])
                                    b = ord(couple_bytes[4*j+27:4*j+28])*2**8
                                    c = ord(couple_bytes[4*j+28:4*j+29])*2**16
                                    d = ord(couple_bytes[4*j+29:4*j+30])*2**24 
                                    PowerCh[j].append( a + b + c + d )
                                    j=j+1
                                  
                                #----stuff to get timestamp... trouble
                                Timestamp.append(0)
                                if i%5000 == 0:
                                    print ("------" , i)
                                    print (couple_bytes[:8])
                                    #print (hex(ord(couple_bytes[0:1])))
                                    #print (hex(ord(couple_bytes[1:2])))
                                    #print (hex(ord(couple_bytes[2:3])))
                                    #print (hex(ord(couple_bytes[3:4])))
                                    #print (hex(ord(couple_bytes[4:5])))
                                    #print (hex(ord(couple_bytes[5:6])))
                                    #print (hex(ord(couple_bytes[6:7])))
                                    #print (hex(ord(couple_bytes[7:8])))
                                    print (binascii.hexlify(couple_bytes[:8]))
                                    lkj = bin(int(binascii.hexlify(couple_bytes[:8]), 16))
                                    print (lkj)
                                    print ("0x%x" % int(lkj, 2))


                            ensure_dir(sys.argv[1]+"\\Data\\NetCDFOutput\\"+Powerfile[-19:-11]+"\\")
                            Powncfile = Dataset(sys.argv[1]+"\\Data\\NetCDFOutput\\"+Powerfile[-19:-11]+"\\Powsample"+Powerfile[-10:-4]+".nc",'w')

                            Powncfile.createDimension('Timestamp',len(Timestamp))

                            TimestampData = Powncfile.createVariable('Timestamp',dtype('float').char,('Timestamp'))
                            PowCh1Data = Powncfile.createVariable('PowerChan1',dtype('float').char,('Timestamp'))
                            PowCh2Data = Powncfile.createVariable('PowerChan2',dtype('float').char,('Timestamp'))
                            PowCh3Data = Powncfile.createVariable('PowerChan3',dtype('float').char,('Timestamp'))
                            PowCh4Data = Powncfile.createVariable('PowerChan4',dtype('float').char,('Timestamp'))
                            PowCh5Data = Powncfile.createVariable('PowerChan5',dtype('float').char,('Timestamp'))
                            PowCh6Data = Powncfile.createVariable('PowerChan6',dtype('float').char,('Timestamp'))
                            PowCh7Data = Powncfile.createVariable('PowerChan7',dtype('float').char,('Timestamp'))
                            PowCh8Data = Powncfile.createVariable('PowerChan8',dtype('float').char,('Timestamp'))
                            PowCh9Data = Powncfile.createVariable('PowerChan9',dtype('float').char,('Timestamp'))
                            PowCh10Data = Powncfile.createVariable('PowerChan10',dtype('float').char,('Timestamp'))
                            PowCh11Data = Powncfile.createVariable('PowerChan11',dtype('float').char,('Timestamp'))
                            PowCh12Data = Powncfile.createVariable('PowerChan12',dtype('float').char,('Timestamp'))
                           
                            TimestampData[:] = Timestamp
                            PowCh1Data[:] = PowerCh[0]
                            PowCh2Data[:] = PowerCh[1]
                            PowCh3Data[:] = PowerCh[2]
                            PowCh4Data[:] = PowerCh[3]
                            PowCh5Data[:] = PowerCh[4]
                            PowCh6Data[:] = PowerCh[5]
                            PowCh7Data[:] = PowerCh[6]
                            PowCh8Data[:] = PowerCh[7]
                            PowCh9Data[:] = PowerCh[8]
                            PowCh10Data[:] = PowerCh[9]
                            PowCh11Data[:] = PowerCh[10]
                            PowCh12Data[:] = PowerCh[11]
                                                        
                            Powncfile.close()

                                    
                # ----------------------- Weather Station ------------------
                WSDataPath = sys.argv[1]+"\\Data\\"+"WeatherStation\\"
                if os.path.isdir(WSDataPath):
                    print (WSDataPath)

                    WSDayList = os.listdir(WSDataPath)
                    WSFileList = [] # will hold list of files needing to be processed
                    for day in WSDayList:
                        TempFileList = os.listdir(WSDataPath + day)
                        if float(day) == float(ThenDate):
                            for file in TempFileList:
                                if file[:14] == "WeatherStation":
                                    if float(file[-10:-4]) > ThenTime:
                                        WSFileList.append(WSDataPath + day + "\\" + file)
                        elif float(day) > float(ThenDate):
                            for file in TempFileList:
                                if file[:14] == "WeatherStation":
                                    WSFileList.append(WSDataPath + day + "\\" + file)
                    #print (WSFileList)
                    for file in WSFileList: # read in file, process into NetCDF, and write out file
                        #print (file)
                        Temperature = []
                        RelHum = []
                        Pressure = []
                        AbsHum = []
                        Timestamp = []
                        
                        #file_object  = open(file, "r") #where file_object is the variable to add the file object. 
                        #print (file_object.read(5))
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
                            #print (sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc")
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
                            
                            WSncfile.close()
               
            else:
                print (sys.argv[1],"is a dir, but",sys.argv[2],"is not a number")
        else:
            print (sys.argv[1],"is not a dir, looking for directory containing Data")

    print ("Goodnight World - the date and time is - ", datetime.datetime.now().strftime("%H:%M:%S:%f"))

if __name__ == '__main__':
    main()

