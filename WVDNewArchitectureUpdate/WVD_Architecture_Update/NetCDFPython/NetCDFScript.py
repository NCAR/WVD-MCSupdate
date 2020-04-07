#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] 
#                    [location to write files]
#                    [how many hours back in time to process]
# Importing needed modules
import os, sys, csv, math, datetime, SharedPythonFunctions as SPF
from SyncBackup import DoRSync
from MakeChildFilesV2 import makeNetCDF


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
        return list(csv.reader(f, delimiter="\t"))
         

# --------------------------------main------------------------------------
def main():
    print ("Start Processing: The date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))
       
    # Creating timestamps used to find which files should be processed
    NowTime  = SPF.getFractionalHours(0)
    NowDate  = datetime.datetime.utcnow().strftime("%Y%m%d")
    LastTime = math.ceil(SPF.getFractionalHours(1))
    
    # creating Error file variable for use if needed 
    FileEnding = NowDate + '_' + datetime.datetime.utcnow().strftime("%H%M%S") + '.txt'
    ErrorFile = os.path.join(sys.argv[1],"Data","Errors",str(NowDate),"NetCDFPythonErrors_"+FileEnding)
    WarningFile = os.path.join(sys.argv[1],"Data","Warnings",str(NowDate),"NetCDFPythonWarnings_"+FileEnding)

    # Processing files
    LocalOutputPath = os.path.join(sys.argv[1],"Data","")
    if os.path.isdir(LocalOutputPath): # the first should be the directory where the Data folder is located.
        # Making sure the filepath is availible 
        NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
        SPF.ensure_dir(NetCDFPath)
        # Checking how far back to process
        HoursBack = sys.argv[3] if is_number(sys.argv[3]) else 3
        # Create timestamp so we know which files to load
        ThenTime = float(SPF.getFractionalHours(HoursBack))
        ThenDate = (datetime.datetime.utcnow() - datetime.timedelta(hours=float(HoursBack))).strftime("%Y%m%d")
        # Making the netcdf child files
        makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,NetCDFPath,readHeaderInfo())
        # Copy NetCDF files to external drive
        print ("RSync files to backup drive ", datetime.datetime.utcnow().strftime("%H:%M:%S"))
        try:
            12#Response = DoRSync(os.getcwd(),sys.argv[2],WarningFile,ErrorFile)
            #print(Response)
        except:
            writeString = "WARNING: unable to RSync to external hard drive - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(WarningFile, writeString)        
    else:
        writeString = "ERROR: argument 1 (path to directory containing Data folder) - "+sys.argv[1]+" - is not a dir, looking for directory containing Data. - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)

    print ("End Processing: The date and time is - ", datetime.datetime.utcnow().strftime("%H:%M:%S"))

if __name__ == '__main__':
    main()

