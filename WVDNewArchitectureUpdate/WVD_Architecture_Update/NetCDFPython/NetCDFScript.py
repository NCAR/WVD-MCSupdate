# Written By: Brad Schoenrock, Robert Stillwell
# Written For: National Center for Atmospheric Researc
# This is the main function used to convert MPD data from their raw data format 
# to netcdf file format. When called from labview, the function is called with 
# 4 arguements: the working directory, the target directory for rsyncing, the 
# number of hours to back process, & a boolean defining if rsyncing is desired.
#%% Importing needed modules
import os, sys, csv, math, datetime, SharedPythonFunctions as SPF
from rsync import DoRSync
from MakeChildFilesV3 import makeNetCDF

#%% Simple utilities 
#checks if a value is a number
def is_number(n):
    try:
        float(n) 
    except ValueError:
        return False
    return True

# reads in config file which hold information for headers of NetCDF files
def readHeaderInfo(WorkingDir):
    with open(os.path.join(WorkingDir,"ConfigureFiles","Configure_WVDIALPythonNetCDFHeader.txt")) as f:
        return list(csv.reader(f, delimiter="\t"))
         
#%%  Main program 
def main(WorkingDir,RSyncTargetDirs,HoursBack,RSync):
    print ("Start Processing: The date and time is - ", datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S"))
    # Creating timestamps used to find which files should be processed
    NowTime  = SPF.getFractionalHours(0)
<<<<<<< Updated upstream
    NowDate  = datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S")
    LastTime = math.ceil(SPF.getFractionalHours(1))
    # creating Error file variable for use if needed 
    FileEnding = NowDate + '_' + datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S") + '.txt'
=======
    NowDate  = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d")
    LastTime = math.ceil(SPF.getFractionalHours(1))
    # creating Error file variable for use if needed 
    FileEnding = NowDate + '_' + datetime.datetime.now(datetime.UTC).strftime("%H%M%S") + '.txt'
>>>>>>> Stashed changes
    ErrorFile = os.path.join(WorkingDir,"Data","Errors",str(NowDate),"NetCDFPythonErrors_"+FileEnding)
    WarningFile = os.path.join(WorkingDir,"Data","Warnings",str(NowDate),"NetCDFPythonWarnings_"+FileEnding)
    # Processing files
    LocalOutputPath = os.path.join(WorkingDir,"Data","")
    if os.path.isdir(LocalOutputPath): # the first should be the directory where the Data folder is located.
        # Making sure the filepath is availible 
        NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
        SPF.ensure_dir(NetCDFPath)
        # Create timestamp so we know which files to load
        ThenTime = float(SPF.getFractionalHours(HoursBack))
        ThenDate = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=float(HoursBack))).strftime("%Y%m%d")
        # Making the netcdf child files
        makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,WorkingDir,NetCDFPath,'')
        # Copy NetCDF files to external drive
        print ("RSync files to backup drive ", datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S"))
        try:
            if RSync == '1':
                Response = ''
                for RSyncTargetDir in RSyncTargetDirs:
                    Response += DoRSync(os.getcwd(),RSyncTargetDir,WarningFile,ErrorFile)
                    Response += '\n'
            else:
                Response = 'No RSync Requested'
            print(Response)
        except:
            writeString = "WARNING: unable to RSync to external hard drive - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(WarningFile, writeString)        
    else:
        writeString = "ERROR: argument 1 (path to directory containing Data folder) - "+WorkingDir+" - is not a dir, looking for directory containing Data. - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)

    print ("End Processing: The date and time is - ", datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S"))

if __name__ == '__main__':
    try: 
        WorkingDir = sys.argv[1]
    except:
        WorkingDir = 'C:\\Users\\h2odial\\WVD-MCSupdate\\WVDNewArchitectureUpdate\\WVD_Architecture_Update'
    try: 
        RSyncTargetDirs = []
        for m in range(4,len(sys.argv)):
            RSyncTargetDirs.append(sys.argv[m])
    except:
        RSyncTargetDirs = ['D:\\MPDBackup']
    try:
        HoursBack = sys.argv[2] if is_number(sys.argv[2]) else 3
    except:
        HoursBack = 3
    try:
        RSync = sys.argv[3] if is_number(sys.argv[3]) else '0'
    except:
        RSync = '0'
           
    # Running main program
    main(WorkingDir,RSyncTargetDirs,HoursBack,RSync)

