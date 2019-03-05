from __future__ import print_function
import os
import sys
import datetime


# write an error message to a file
def Write2ErrorFile(ErrorFile, writeString):
    ensure_dir(ErrorFile)
    fh = open(ErrorFile, "a")
    fh.write(writeString)
    print (writeString, file=sys.stderr)

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

def getFractionalHours(HoursBack):
    ThenTime = float((datetime.datetime.utcnow()-datetime.timedelta(hours=float(HoursBack))).strftime("%H")) + \
               float((datetime.datetime.utcnow()-datetime.timedelta(hours=float(HoursBack))).strftime("%M"))/60 + \
               float((datetime.datetime.utcnow()-datetime.timedelta(hours=float(HoursBack))).strftime("%S"))/3600 + \
               float((datetime.datetime.utcnow()-datetime.timedelta(hours=float(HoursBack))).strftime("%f"))/3600000000
    return ThenTime



def convertString2CWSyntax(String):
    Before, After = String.split(":\\",1)
    
    NewString = '/cygdrive/' + Before + '/' + After.replace("\\",'/')
    return NewString
