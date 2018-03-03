#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [how many hours back in time to process]

import os
import sys
import time
import datetime
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
    print ("Hello World - the date and time is - ", time.ctime())
    print ("These are the arguments I passed in to my test script:")
    for i in range(0,len(sys.argv)-1):
        print (sys.argv[i+1])
    
    print (" ")
    print (" ")
    
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

                #check for children data dirs
                LaserLockingDataPath = sys.argv[1]+"\\Data\\"+"LaserLocking\\"
                if os.path.isdir(LaserLockingDataPath):
                    print (LaserLockingDataPath)

                MCSDataPath = sys.argv[1]+"\\Data\\"+"MCS\\"
                if os.path.isdir(MCSDataPath):
                    print (MCSDataPath)

                WSDataPath = sys.argv[1]+"\\Data\\"+"WeatherStation\\"
                if os.path.isdir(WSDataPath):
                    print (WSDataPath)

                    DayList = os.listdir(WSDataPath)
                    WSFileList = [] # will hold list of files needing to be processed
                    for day in DayList:
                        TempFileList = os.listdir(WSDataPath + day)
                        if float(day) == float(ThenDate):
                            for file in TempFileList:
                                if file[:14] == "WeatherStation":
                                    if float(file[24:-4]) > ThenTime:
                                        WSFileList.append(WSDataPath + day + "\\" + file)
                        elif float(day) > float(ThenDate):
                            for file in TempFileList:
                                if file[:14] == "WeatherStation":
                                    WSFileList.append(WSDataPath + day + "\\" + file)
                    #print (WSFileList)
                    for file in WSFileList: # read in file, process into NetCDF, and write out file
                        print (file)
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
                            print (sys.argv[1]+"\\Data\\NetCDFOutput\\"+file[-19:-11]+"\\WSsample"+file[-10:-4]+".nc")
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

if __name__ == '__main__':
    main()

