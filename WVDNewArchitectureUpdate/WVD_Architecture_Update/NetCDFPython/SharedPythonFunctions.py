from __future__ import print_function
import os, sys, datetime

#%% Write an error message to a file
def Write2ErrorFile(ErrorFile, writeString):
    ensure_dir(ErrorFile)
    fh = open(ErrorFile, "a")
    fh.write(writeString)
    print (writeString, file=sys.stderr)
#%% Makes sure a directory exists or creates it
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory): os.makedirs(directory)
#%% Checking data directory for all possible files 
def getFiles(DataPath, dataname, datatype, ThenDate, ThenTime):
    DayList = os.listdir(DataPath)
    FileList = [] # will hold list of files needing to be processed
    for day in DayList:
        TempFileList = os.listdir(os.path.join(DataPath,day))
        if float(day) == float(ThenDate):
            for file in TempFileList:
                # Checking if the file type and extension are as expected
                if file[:len(dataname)] == dataname and file[-1*len(datatype):] == datatype:
                    # Checking if the file timestamp is after the "ThenTime" variable
                    if int(file[-1*len(datatype)-6:-1*len(datatype)])/10000 > ThenTime:
                        FileList.append(os.path.join(DataPath,day,file))
        elif float(day) > float(ThenDate):
            for file in TempFileList:
                # Checking if the file type and extension are as expected
                if file[:len(dataname)] == dataname and file[-1*len(datatype):] == datatype:
                    FileList.append(os.path.join(DataPath,day,file))
    FileList.sort()
    return FileList
#%% Determine the time of data in fractional hours
def getFractionalHours(HoursBack):  
    Time2Use = datetime.datetime.utcnow() - datetime.timedelta(hours=float(HoursBack)) 
    Types = ["%H","%M","%S","%f"]; Conversions = [1,60,3600,3600000000]
    return sum([float(Time2Use.strftime(Type))/Div for Type, Div in zip(Types,Conversions)])   
#%% Converting windows file paths to paths that can be understood by cwrsync
def convertString2CWSyntax(String):
    Before, After = String.split(":\\",1)
    NewString = '/cygdrive/' + Before + '/' + After.replace("\\",'/')
    return NewString