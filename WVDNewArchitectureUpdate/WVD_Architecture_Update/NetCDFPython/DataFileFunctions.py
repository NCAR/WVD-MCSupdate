# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# These functions are used to open, read, and write data files needed for the 
# MicroPulse DIAL lidar system. 
import os
from   netCDF4 import Dataset
import SharedPythonFunctions as SPF
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
    # Determining if the data type selected is recognized
    CellArray = []; 
    for m in range(len(Type)):
        DataType = 12
        if Type[m] == 'str':
            DataType = np.str
        elif (Type[m] == 'float' or Type[m] == 'float32' or Type[m] == 'f'):
            DataType = np.float
        elif (Type[m] == 'b'):
            DataType = np.bool
        elif (Type[m] == 'Pass'):
            DataType = 'Pass'
        # Converting cell as a particular type
        if DataType != 12:
            if DataType != 'Pass':
                CellArray.append(np.array(Collected[m]).astype(DataType))
            else:
                CellArray.append(ListData[m]) 
        else:
            CellArray.append([])  
            print('Data type in file not recognized')
    # returning cell array
    return CellArray    

#%%
# This function simply places the information needed for each variable within
# a netcdf file. 
def CreateAndPlaceNetCDFVariable(File,VarData,VarDescription,VarDimension,VarName,VarType,VarUnit):
    Data = File.createVariable(VarName,np.dtype(VarType).char,VarDimension)
    Data[:] = VarData
    Data.units = VarUnit
    Data.description = VarDescription
    
#%% 
# This function strips off the date and time from the files written by Labview
def FindFileDateAndTime(FileName,Print = False):
    FileDate = FileName[-19:-11]
    FileTime = FileName[-10:-4]
    if Print:
        print ('  File Date: ' + FileDate + ', File Time:' + FileTime)
    return (FileDate,FileTime)

#%%
# This function is used to write a netcdf file for the MPD systems. It takes 
# the description of that file as input and returns no output. 
def WriteNetCDFFile(LocalNetCDFOutputPath,Header,Transpose,
                    FileDate,FileDescription,FileDimensionNames,FileDimensionSize,FileTime,FileType, 
                    VarData, VarColumn, VarDescription, VarDimension, VarName, VarType, VarUnit):
    # Create a netcdf file and set its inital parameters
    SPF.ensure_dir(os.path.join(LocalNetCDFOutputPath,FileDate,''))
    DataFile = Dataset(os.path.join(LocalNetCDFOutputPath,FileDate,FileType+FileTime+'.nc'),'w')
    # Write a brief description of file
    DataFile.description = FileDescription
    # Load up header information for file

    # Creating dimensions
    for m in range(len(FileDimensionNames)):
        DataFile.createDimension(FileDimensionNames[m],FileDimensionSize[m])
    # Writing individual variables
    if (type(VarData) == list):      # File was an alpha-numeric file or contained complicated data
        for m in range(len(VarName)):
            if Transpose[m]:
                # transposing the data arrays 
                VarData[VarColumn[m]] = np.transpose(VarData[VarColumn[m]])
            CreateAndPlaceNetCDFVariable(DataFile, VarData[VarColumn[m]], VarDescription[m], 
                                         VarDimension[m], VarName[m], VarType[m], VarUnit[m])
    else:
        for m in range(len(VarName)):# File only contained numbers
            if Transpose[m]:
                # transposing the data arrays
                CreateAndPlaceNetCDFVariable(DataFile, np.transpose(VarData[:,VarColumn[m]]), VarDescription[m], 
                                         VarDimension[m], VarName[m], VarType[m], VarUnit[m])
            else:
                CreateAndPlaceNetCDFVariable(DataFile, VarData[:,VarColumn[m]], VarDescription[m], 
                                         VarDimension[m], VarName[m], VarType[m], VarUnit[m])
    # Close file
    DataFile.close()
   
#%%
# This function reads a given text file line by line and checks to make sure 
# all lines are the same length. If they are not, it pads the lines that are 
# shorter with bad values
def ReadAndPadTextFile(FileName):
    # Defining the original data array
    Data = []
    # Opening the file to be read
    with open(FileName,'r') as file:     # opening the file as read only
        for line in file:                # Looping over all lines in the file
            line = line.replace(' ','\t').strip('\r\n') # making sure the deliminator is consistent 
            if len(line.split('\t')) > 0: # Reading each non-zero length line
                Data.append(line.split('\t'))
    # Determining the needed size of the array
    Len = []
    for m in range(len(Data)): Len.append(len(Data[m]))
    ArrayWidth = max(Len)
    # Defining a padded data array
    Padded = []
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
