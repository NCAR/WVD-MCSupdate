# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# These functions are used to convert raw data from the MicroPulse DIAL systems
# to netcdf data. The information should be identical except for the following 
# cases:
#       1) Files where the data are jagged arrays instead of full are filled 
#          with a bad data marker (-1000000000) to make all rows the same size
#       2) Thermocouple & Current data files have the location of the elements 
#          in the raw file name but as a variable in the netcdf file
#%% Importing needed modules
import datetime, os, sys, pdb
import numpy                 as np
import DataFileFunctions     as DFF
import DefineFileElements    as Define
import SharedPythonFunctions as SPF

#%%################################# General ##################################
def processGeneral(FolderType,FileType,FileName,NetCDFOutputPath,Header):
    # Print what is going on
    print("Making ",FileType," data file:", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    # Find file date and time
    (FileDate,FileTime,MPDNum) = DFF.FindFileDateAndTime(FileName,True)
    # Reading data file 
    VarData = DFF.ReadFileGeneral(FileName,FolderType,FileType)
    # Filling data arrays needed to define file attributes
    ArrayData=None; List1d=None; List2d=None; ListOther=None
    if isinstance(VarData,np.ndarray):
        ArrayData = VarData; 
    elif isinstance(VarData,list):
        if FileType in ['MCS','MCSV2','MCSScanV2']:
            List2d = VarData;
        elif FileType in ['TCSPC']:
            ListOther = VarData;
        else:
            List1d = VarData;
    # Defining file attributes and variable attributes
    Attributes = Define.DefineNetCDFFileAttributes(ArrayData,List1d,List2d,ListOther)
    # Writing the netcdf file 
    DFF.WriteNetCDFFileV2(NetCDFOutputPath,Header,Attributes[FileType],FileDate,FileTime,MPDNum,VarData)
    
#%%
def makeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,WarningFile,ErrorFile,WorkingDir,NetCDFPath,Header):
    # Defining the files to be written (File base name, file extension, local file type tag))
    FileTypes2Process = {'Container':      [['ContainerLogging','.txt','Container']],
                         'Current':        [['Current','.txt','Current']],
                         'Housekeeping':   [['HousekeepingV2','.txt','HKV2']],
                         'HumiditySensor': [['Humidity','.txt','Humidity']],
                         'HyperfineScan':  [['BalancedDetector','.txt','BDetector'],
                                            ['Wavemeter','.txt','Wavemeter'],
                                            ['LaserCurrentScan','.txt','CurrentScan']],
                         'LaserLocking':   [['LaserLocking','.txt','LL'],
                                            ['Etalon',      '.txt','Etalon']],
                         'MCS':            [['MCSDataV2','.bin','MCSV2'],
                                            ['MCSPowerV2','.bin','PowerV2']],
                         'QuantumComposer':[['QuantumComposerOps','.txt','Clock']],
                         'ReceiverScan':   [['MCSDataV2','.bin','MCSScanV2'],
                                            ['Wavemeter','.txt','Wavemeter'],
                                            ['LaserScanData','.txt','LaserScan'],
                                            ['EtalonScanData','.txt','EtalonScan']],
                         'TCSPC':          [['TCSPCFastData','.bin','TCSPC']],
                         'UPS':            [['UPS','.txt','UPS']],
                         'WeatherStation': [['WeatherStation','.txt','WStation']]}
#    FileTypes2Process = {'TCSPC':          [['TCSPC','.bin','TCSPC']]}
    # Looping over all possible file types and looking for files matching that
    for FolderType in FileTypes2Process:
        for FileBase, FileExt, FileType in FileTypes2Process[FolderType]:
            # Defining the file base path expected
            Where2FindData = os.path.join(WorkingDir,'Data',FolderType)           
            if os.path.isdir(Where2FindData):
                # Looking for files and looping over them
                FileList = SPF.getFiles(Where2FindData , FileBase, FileExt, ThenDate, ThenTime)
                for File in FileList:
                    try:
                        processGeneral(FolderType,FileType,File,NetCDFPath,Header) 
                    except:
                        writeString = 'WARNING: Failure to process ' + FolderType + ' data - ' + FolderType +\
                                      ' file = ' + str(File) + ' - ' + '\n' + str(sys.exc_info()[0]) + '\n\n'
                        print(writeString)
                        