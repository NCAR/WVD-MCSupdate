#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] 
#                    [location to write files]
#                    [how many hours back in time to process]

import os
import sys
import csv
import math
import datetime

from SyncBackup import DoRSync
from MakeChildFilesV2 import makeNetCDF
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
    NowTime = SPF.getFractionalHours(0)
    NowDate = datetime.datetime.utcnow().strftime("%Y%m%d")

    # LastHour variables used to find NetCDF Logging files for error and other logging. 
    LastTime = math.ceil(SPF.getFractionalHours(1))

    # creating Error file variable for use if needed ... which of course it never will be ... right?
    SPF.ensure_dir(os.path.join(sys.argv[1],"Data","Errors",str(NowDate),""))
    SPF.ensure_dir(os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),""))
    ErrorFile = os.path.join(sys.argv[1],"Data","Errors",str(NowDate),"NetCDFPythonErrors_"+str(NowDate)+"_"+str(NowTime)+".txt")
    WarningFile = os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),"NetCDFPythonWarnings_"+str(NowDate)+"_"+str(NowTime)+".txt")

    print ("Loction of error file if needed = ", ErrorFile)
    print ("Loction of warning file if needed = ", WarningFile)

    LocalOutputPath = os.path.join(sys.argv[1],"Data","")
    if os.path.isdir(LocalOutputPath): # the first should be the directory where the Data folder is located.

        SPF.ensure_dir(LocalOutputPath)
        NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
        SPF.ensure_dir(NetCDFPath)

        if is_number(sys.argv[3]): # the second should be a number of hours worth of files that we want to process
            HoursBack = sys.argv[3]
        else:
            HoursBack = 3
            writeString = "Warning: argument 3 (hours to back process) - "+sys.argv[3]+" - is not a number. Using default "+HoursBack+" hours instead. - "+str(NowTime) + '\n'
            SPF.Write2ErrorFile(WarningFile, writeString)

        print ("go back "+str(sys.argv[3])+" hours")

        # create timestamp for sys.argv[3] hours ago so we know which files to load
        ThenTime = float(SPF.getFractionalHours(HoursBack))
        ThenDate = (datetime.datetime.utcnow() - datetime.timedelta(hours=float(sys.argv[3]))).strftime("%Y%m%d")
     
        # Making the netcdf child files
        makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,readHeaderInfo())

        #copy NetCDF files to external drive if applicable.
        print ("RSync files to backup drive ", datetime.datetime.utcnow().strftime("%H:%M:%S"))
        OutputPath = os.path.join(sys.argv[2],"Data","")
        try:
            12#DoRSync(os.getcwd(),sys.argv[2],WarningFile,ErrorFile)
        except:
            writeString = "WARNING: unable to RSync to external hard drive - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(WarningFile, writeString)        
    else:
        writeString = "ERROR: argument 1 (path to directory containing Data folder) - "+sys.argv[1]+" - is not a dir, looking for directory containing Data. - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)

    print ("Goodnight World - the date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))



if __name__ == '__main__':
    main()

