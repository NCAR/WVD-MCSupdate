# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# These functions are used to open, read, and write data files needed for the 
# MicroPulse DIAL lidar system. 
#%% Importing needed modules
import os, pdb
from   netCDF4     import Dataset
from   collections import defaultdict
import DefineFileElements    as Define
import SharedPythonFunctions as SPF
import NCARMCSFunctions      as NMF
import numpy                 as np
#%% 
# This function takes a list of data (rows are individual measurments) and 
# reshapes it into a list of data (rows are each measurement type) with each 
# row being an array of all the same type 
def ConvertAlphaNumericFile(ListData,Type,Transpose=True):
    # Collecting all the columns of the data for individual conversion
    if Transpose:
        Collected = []
        for n in range(len(ListData[0])):
            Collected.append([])
            for m in range(len(ListData)):
                Collected[n].append(ListData[m][n])
    else:
        Collected = ListData
    # Defining a dictonary to convert data types
    DataTypeMap = defaultdict(lambda:'NotRecognized',getattr(Define,'DefineDataTypeMap')())
    # Determining if the data type selected is recognized
    CellArray = []; 
    for m in range(len(Type)):
        DataType = DataTypeMap[Type[m]]
        # Converting cell as a particular type
        if DataType == 'Pass':
             CellArray.append(ListData[m])
        elif DataType == 'NotRecognized':
             CellArray.append([])  
             print('Data type in file not recognized')
        else:
             CellArray.append(np.array(Collected[m]).astype(DataType))
    # returning cell array
    return CellArray    

#%%
# This function takes a filename with a combined location string, splits that 
# location string into its component bits, and then calls the defined map for 
# that bit map to return a list of string locations
def ConvertLocationNumber2Strings(FileName,BPL,MaxLoc,Type):
    # Converting the filename number to a string of bits with the right length
    BitString = ''.join(['{:',str(MaxLoc*BPL),'b}']).format(int(FileName.split('_')[-4])).replace(' ','0')
    # Looping over the bits in chunks of BPL to extrac location numbers
    Types = [int(BitString[I*BPL:I*BPL+BPL],2) for I in range(MaxLoc)]
    # Defining a dictonary with a default value
    MapDictonary = defaultdict(lambda:"Unassigned",getattr(Define,'Define'+Type+'Map')())
    # Parsing the Location bits using the BitsPerLocation  
    return(np.array([MapDictonary[Type] for Type in reversed(Types)]).astype(np.str))
    
#%%
# This function simply places the information needed for each variable within
# a netcdf file. 
def CreateAndPlaceNetCDFVariable(File,VarData,VarDescription,VarDimension,VarName,VarType,VarUnit):
    Data = File.createVariable(VarName,np.dtype(VarType).char,VarDimension)
    Data[:] = VarData                  # Setting variable value
    Data.units = VarUnit               # Setting variable units
    Data.description = VarDescription  # Setting variable description
    
#%% 
# This function strips off the date and time from the files written by Labview
def FindFileDateAndTime(FileName,Print=False):
    FileDate = FileName[-19:-11]
    FileTime = FileName[-10:-4]
    MPDNum   = FileName[-22:-20]
    if Print: print ('  File date: ' + FileDate + ', File time:' + FileTime)
    return (FileDate,FileTime,MPDNum)

#%%
# This function is used to write a netcdf file for the MPD systems. It takes 
# the description of that file as input and returns no output. 
def WriteNetCDFFileV2(LocalNetCDFOutputPath,Header,Attr,FileDate,FileTime,MPDUnit,VarData):
    # Create a netcdf file and set its inital parameters
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,FileDate,''))
    FileNameFinal = Attr['FType'] + '_' + MPDUnit + '_' + FileDate + '_' + FileTime + '.nc'
    DataFile = Dataset(os.path.join(LocalNetCDFOutputPath,FileDate,FileNameFinal),'w')
    # Write a brief description of file
    DataFile.description = Attr['FDescription']
    # Load up header information for file

    # Creating dimensions
    for m in range(len(Attr['FDimNames'])):
        DataFile.createDimension(Attr['FDimNames'][m],Attr['FDimSize'][m])
    # Writing individual variables
    for m in range(len(Attr['VarName'])):# File only contained numbers
        # Determining if the data to write should be transposed or not
        if (type(VarData) == list): 
            Data2Write = np.transpose(VarData[Attr['VarCol'][m]]) if Attr['Transpose'][m] else VarData[Attr['VarCol'][m]]
        else:
            Data2Write = np.transpose(VarData[:,Attr['VarCol'][m]]) if Attr['Transpose'][m] else VarData[:,Attr['VarCol'][m]]
        # Placing the variables in the netcdf file
        CreateAndPlaceNetCDFVariable(DataFile, Data2Write, Attr['VarDescrip'][m],Attr['VarDim'][m],
                                     Attr['VarName'][m],Attr['VarType'][m],Attr['VarUnit'][m])
    # Close file
    DataFile.close()
   
#%%
# This function reads a given text file line by line and checks to make sure 
# all lines are the same length. If they are not, it pads the lines that are 
# shorter with bad values
def ReadAndPadTextFile(FileName):
    # Defining the data lists 
    Data = []; Len = []; Padded = []
    # Opening the file to be read
    with open(FileName,'r') as file:     # opening the file as read only
        for line in file:                # Looping over all lines in the file
            line = line.replace(' ','\t').strip('\r\n') # making sure the deliminator is consistent 
            if len(line.split('\t')) > 0: # Reading each non-zero length line
                Data.append(line.split('\t'))
    # Determining the needed size of the array
    for m in range(len(Data)): Len.append(len(Data[m]))
    ArrayWidth = max(Len)
    # Looping over all lines in the data array
    for m in range(len(Data)):
        # Checking if the data is the correct size or too small
        if (len(Data[m]) ==  ArrayWidth):    # Just add the data as is
            Padded.append(Data[m])
        else:                                # Data needs to be padded
            PaddingNeeded = ArrayWidth - len(Data[m])
            Padded.append(Data[m] + PaddingNeeded*['-1000000000'])  
    # Returning a padded data array
    return Padded
#%%
def ReadFileGeneral(FileName, FolderType, FileType):
    VarData = []
    # Read file based on its type 
    if FileType in {'BDetector','Current','HKV2','Humidity','UPS','Wavemeter','WStation'}:
        # File contains only numbers so read simply
        VarData = np.array(ReadAndPadTextFile(FileName)).astype(np.float)  
        # Parse out location information for files containing such info
        if FileType in {'Current','HKV2'}:
            ProcessMap={'Current':'Current','HKV2':'Thermocouple' }
            Locations = len(VarData[1,:])-1
            VarData = [VarData[:,0],np.transpose(VarData[:,list(np.asarray(range(Locations))+1)]),
                       ConvertLocationNumber2Strings(FileName,4,Locations,ProcessMap[FileType])]        
    elif FileType in {'Container','Etalon','LL','LaserScan','EtalonScan','MCSV2','PowerV2','MCSScanV2','TCSPC'}:  
        # Determing the file structure 
        DataType = Define.DefineFileStructure(FileType)       
        # Defining which function to call
        MapDictonary = {'MCS':'ReadMCSPhotonCountFile','MCSV2':'ReadMCSPhotonCountFileV2',
                        'Power':'ReadMCSPowerFile','PowerV2':'ReadMCSPowerFileV2', 
                        'MCSScanV2':'ReadMCSPhotonCountFileV2', 'TCSPC': 'ReadTCSPCTimeTags'}
        MapDictonary = defaultdict(lambda:"NotMCS",MapDictonary)
        # Converting file
        if MapDictonary[FileType]=="NotMCS":            
            VarData = ConvertAlphaNumericFile(ReadAndPadTextFile(FileName),DataType)
        else:
            VarData = ConvertAlphaNumericFile(list(getattr(NMF,MapDictonary[FileType])(FileName)),DataType,False)
    elif FileType == 'Clock':
        # Reading data file and returning a padded array as needed 
        FileData = [' '.join(Line).split() for Line in ReadAndPadTextFile(FileName)]
        VarData = np.array(FileData).astype(np.float) 
    return(VarData)