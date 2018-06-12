#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [location to write files] [how many hours back in time to process]

import os
import sys
import csv
import math
import datetime
from datetime import timedelta

from SyncBackup import DoRSync
from MakeMergedFiles import mergeNetCDF
from MakeChildFiles import makeNetCDF
import SharedPythonFunctions as SPF


#checks if a value is a number
def is_number(n):
    try:
        float(n) 
    except ValueError:
        return False
    return True

# reads in config file which hold information for headers of NetCDF files
def readHeaderInfo():
    with open(os.path.join(sys.argv[1],"ConfigureFiles","Configure_WVDIALPythonNetCDFHeader.txt")) as f:
        reader = csv.reader(f, delimiter="\t")
        header = list(reader)
        #print (header)
        return header



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
    SPF.ensure_dir(os.path.join(sys.argv[1],"Data","Errors",str(NowDate)))
    SPF.ensure_dir(os.path.join(sys.argv[1],"Data","Warnings",str(NowDate)))
    ErrorFile = os.path.join(sys.argv[1],"Data","Errors",str(NowDate),"NetCDFPythonErrors_"+str(NowDate)+"_"+str(NowTime)+".txt")
    WarningFile = os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),"NetCDFPythonWarnings_"+str(NowDate)+"_"+str(NowTime)+".txt")

    print ("Loction of error file if needed = ", ErrorFile)
    print ("Loction of warning file if needed = ", WarningFile)

    LocalOutputPath = os.path.join(sys.argv[1],"Data","")
    if os.path.isdir(LocalOutputPath): # the first should be the directory where the Data folder is located.

        SPF.ensure_dir(LocalOutputPath)
        NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
        SPF.ensure_dir(NetCDFPath)
        CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
        SPF.ensure_dir(CFRadPath)

        if is_number(sys.argv[3]): # the second should be a number of hours worth of files that we want to process
            HoursBack = sys.argv[3]

        else:
            HoursBack = 3
            writeString = "Warning: argument 3 (hours to back process) - "+sys.argv[3]+" - is not a number. Using default "+HoursBack+" hours instead. - "+str(NowTime) + '\n'
            SPF.Write2ErrorFile(WarningFile, writeString)

        print ("go back "+str(sys.argv[3])+" hours")

        # create timestamp for sys.argv[3] hours ago so we know which files to load
        ThenHour = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%H")
        ThenMin = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%M")
        ThenSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%S")
        ThenMicroSec = (datetime.datetime.utcnow()-timedelta(hours=float(sys.argv[3]))).strftime("%f")
        ThenTime = float(ThenHour) + float(ThenMin)/60 + float(ThenSec)/3600 + float(ThenMicroSec)/3600000000
        ThenDate = (datetime.datetime.utcnow() - timedelta(hours=float(sys.argv[3]))).strftime("%Y%m%d")
     
        header = readHeaderInfo()

        makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,header)

        #merge into one combined file
        mergeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,LocalOutputPath,header,WarningFile,ErrorFile)

        #copy NetCDF files to external drive if applicable.
        print ("RSync files to backup drive ", datetime.datetime.utcnow().strftime("%H:%M:%S"))
        OutputPath = os.path.join(sys.argv[2],"Data","")
        # Rsync can't be performed when both source and destination are remote
        # so we have to change directory so that one of the locations isn't remote
        # windows sees anything with a : in the path to be remote
        # the cygdrive also apears to be treated as remote
        # when we are done with the RSync then we get to change directories back
        try:
            cwd = os.getcwd()
            os.chdir(sys.argv[2])
            DoRSync("/cygdrive/c/Users/h2odial/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data",".",WarningFile,ErrorFile)
            os.chdir(cwd)
        except:
            writeString = "WARNING: unable to RSync to external hard drive - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(WarningFile, writeString)
    # if os.path.isdir(os.path.join(sys.argv[1],"Data"):        
    else:
        writeString = "ERROR: argument 1 (path to directory containing Data folder) - "+sys.argv[1]+" - is not a dir, looking for directory containing Data. - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)

    print ("Goodnight World - the date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))



if __name__ == '__main__':
    main()

