import os
import sys
import datetime
from datetime import timedelta
from netCDF4 import Dataset
from copy import copy

import numpy as np
from numpy import arange, dtype
import decimal
decimal.getcontext().rounding = decimal.ROUND_DOWN

import SharedPythonFunctions as SPF

def FillVar(dataset, varName):
    var = dataset.variables[varName][:]
    varFill = []
    i=0
    for entry in var:
        varFill.append(var[i])
        i=i+1
    return varFill

def Fill2DVar(dataset, varName):
    var = dataset.variables[varName][:]
    localvar = []
    for array in var:
        localvar.append([])
        localvar[int(len(localvar)-1)]=array
    localvar = np.array(localvar).T.tolist()
    return localvar

def toSec(fracHour):
    return (float(fracHour) - int(fracHour))*3600 



#=========== called by various merging functions to interpolate sparse data onto
# a timeseries that is determined by MCS data if available, or to a 1/2 Hz timeseries
# if data is unavailable ===========
def interpolate(ArrayIn,MasterIn, VarTimestamp, MasterTimestamp):
        
    LocalArrayIn = copy(ArrayIn)
    LocalMasterIn = copy(MasterIn)
    LocalVarTimestamp = copy(VarTimestamp)
    LocalMasterTimestamp = copy(MasterTimestamp)
    ArrayOut = LocalMasterIn
    
    timedeltaSum = 0
    timecounter = 0
    for i in range(0,len(LocalMasterTimestamp)-1):
        timecounter = timecounter + 1
        timedeltaSum = timedeltaSum + (LocalMasterTimestamp[i+1] - LocalMasterTimestamp[i])
    if len(LocalMasterTimestamp) == 1:
        ArrayOut = ma.array([float('NaN')])
        return ArrayOut
    if len(LocalMasterTimestamp) == 0:
        ArrayOut = ma.array([])
        return ArrayOut
        
    AveTimeDelta = timedeltaSum/timecounter
    
    placeOututArray = 0 # this hold where in the output array we want

    if len(LocalVarTimestamp) > 0:
        for localTime in LocalMasterTimestamp:
            if toSec(LocalVarTimestamp[0]) > localTime - AveTimeDelta:
                placeOututArray = placeOututArray + 1
            else:
                while len(LocalVarTimestamp) > 1 and toSec(LocalVarTimestamp[1]) < localTime:
                    LocalVarTimestamp.pop(0)
                    LocalArrayIn.pop(0)
                if len(LocalVarTimestamp) > 1:    
                    deltaT = toSec(LocalVarTimestamp[1]) - toSec(LocalVarTimestamp[0])
                    deltaTau = localTime - toSec(LocalVarTimestamp[0])
                    fracT = deltaTau/deltaT 
                    deltaVal = LocalArrayIn[1] - LocalArrayIn[0]
                    newVal = LocalArrayIn[0] + (fracT * deltaVal)
                    ArrayOut[placeOututArray]=newVal
                placeOututArray = placeOututArray + 1
    return ArrayOut


    
#=========== called by power merging function to appfileTimely frequent data onto
# a timeseries that is determined by MCS data if available, or to a 1/2 Hz timeseries
# if data is unavailable ===========
def assign(ArrayIn,MasterIn,VarTimestamp,MasterTimestamp):
    LocalArrayIn = copy(ArrayIn)
    LocalMasterIn = copy(MasterIn)
    LocalVarTimestamp = copy(VarTimestamp)
    LocalMasterTimestamp = copy(MasterTimestamp)

    ArrayOut = LocalMasterIn

    timedeltaSum = 0
    timecounter = 0
    for i in range(0,len(LocalMasterTimestamp)-1):
        timecounter = timecounter + 1
        timedeltaSum = timedeltaSum + (LocalMasterTimestamp[i+1] - LocalMasterTimestamp[i])
    if len(LocalMasterTimestamp) == 1:
        ArrayOut = ma.array([float('NaN')])
        return ArrayOut
    if len(LocalMasterTimestamp) == 0:
        ArrayOut = ma.array([])
        return ArrayOut
    
    AveTimeDelta = timedeltaSum/timecounter

    placeOututArray = 0 # this hold where in the output array we want

    if len(LocalVarTimestamp) > 0:
        for localTime in LocalMasterTimestamp:
            if toSec(LocalVarTimestamp[0]) > localTime - AveTimeDelta:
                placeOututArray = placeOututArray + 1
            else:
                tempsum = 0
                tempcount = 0
                while len(LocalVarTimestamp) > 1 and len(LocalArrayIn) > 1 and toSec(LocalVarTimestamp[0]) < localTime:
                    if toSec(LocalVarTimestamp[0]) > (localTime - AveTimeDelta) :
                        tempsum = tempsum + LocalArrayIn[0]
                        tempcount = tempcount + 1
                    LocalVarTimestamp.pop(0)
                    LocalArrayIn.pop(0)
                if tempcount > 0:
                    ArrayOut[placeOututArray] = (tempsum/tempcount)
                placeOututArray = placeOututArray + 1

    return ArrayOut



#=========== called by merging function to conform to CFRadial standards ===========
def CFRadify(MergedFile,CFRadPath,header):
    print ("formatting merged file into CFRadial", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = MergedFile[-29:-21]
    fileTime = MergedFile[-9:-3]
    print (fileDate)
    print (fileTime) 
    
    Mergedncfile = Dataset(MergedFile,'a')
        
    # brief description of file
    Mergedncfile.description = "Water Vapor Dial data file"
        
    # load up header information for file global attributes
    for entry in header:
        if len(entry)>0:
            Mergedncfile.setncattr(entry[0],entry[len(entry)-1])
        
    # these two dimensions should already exist
    # Mergedncfile.createDimension('time',len(MasterTimestamp))
    # Mergedncfile.createDimension('range',MasterNBins[0])

    # these dimentions are being added here
    try:
        Mergedncfile.createDimension('sweep',1)
        Mergedncfile.createDimension('string_length',20)
        Mergedncfile.createDimension('string_length_DataType',5)
    except:
        pass
    
    # thse are the coordinate variables - time is already built, range is not. 
    TimestampData = Mergedncfile['time']

    try:
        RangeData = Mergedncfile.createVariable('range',dtype('float').char,('range'))
        RangeData.standard_name = 'projection_range_coordinate'
        RangeData.long_name = 'range_to_measurement_volume'           
        RangeData.units = "meters"
        RangeData.spacing_is_constant = 'true'
        RangeData.meters_to_center_of_first_gate = 0
        RangeData.axis = "radial_range_coordinate"
        RangeData.description = "The range variable for collected data as distance from DIAL unit"
    except:
        RangeData = Mergedncfile.variables["range"][:]
    
    # global variables
    try:
        VolNumData = Mergedncfile.createVariable('volume_number',dtype('float').char,())
        InstTypeData = Mergedncfile.createVariable('instrument_type','S1','string_length_DataType')
    except:
        InstTypeData = Mergedncfile.variables["instrument_type"][:]

    InstTypeData[:] = list("lidar")

    try:
        TimeStartData = Mergedncfile.createVariable('time_coverage_start','S1','string_length')
        TimeEndData = Mergedncfile.createVariable('time_coverage_end','S1','string_length')
    except:
        TimeStartData = Mergedncfile.variables["time_coverage_start"][:]
        TimeEndData = Mergedncfile.variables["time_coverage_end"][:]
        
    year = int(int(fileDate)/10000)
    month = int((int(fileDate) - year*10000)/100)
    day = int((int(fileDate) - year*10000 - month*100))
    hour = int(int(fileTime)/10000)
    minute = int((int(fileTime) - hour*10000)/100)
    sec = int(int(fileTime) - hour*10000 - minute*100)
    TimeStart = format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')+"T"+format(hour,'02d')+":"+format(minute,'02d')+":"+format(sec,'02d')+"Z"
    TimeStartData[:] = list(TimeStart)
    lastTime = TimestampData[len(TimestampData)-1]
    hour = int(int(fileTime)/10000)
    minute = int(float(lastTime)/60)
    sec = int(float(lastTime)%60)
    TimeEnd = format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')+"T"+format(hour,'02d')+":"+format(minute,'02d')+":"+format(sec,'02d')+"Z"

    TimeEndData[:] = list(TimeEnd)

    # set attributes for time 
    TimestampData.standard_name = 'time'
    TimestampData.long_name = 'time_in_seconds_since_volume_start'           
    TimestampData.units = "seconds since " + TimeStart
    TimestampData.description = "The time of collected data in UTC hours from the start of the day"

    # ------------------------- Checking for variables existing. -----------------------------
    # Each section here tries to make variables, that will fail if the variable exists and it will move on to the except
    # which will load the variable. Then we try to set its units and descriptions for each system.
    try: #create the variable if you can, fill it with nans
        nSensors = 1
        Mergedncfile.createDimension('nInternalThermalSensors',nSensors)
        HKeepTemperatureData = Mergedncfile.createVariable("HKeepTemperature",dtype('float').char,('nInternalThermalSensors','time'))
        HKeepTemperatureData.append([])
        for i in range (0,len(TimestampData)-1):
            HKeepTemperatureData[i].append(float('nan'))
    except:
        HKeepTemperatureData = Mergedncfile.variables["HKeepTemperature"][:]
    HKeepTemperatureData.units = "Celcius"
    HKeepTemperatureData.description = "Temperature measured inside the container by nInternalThermalSensors"


    try: #create the variable if you can, fill it with nans
        UPSTemperatureData = Mergedncfile.createVariable("UPSTemperature",dtype('float').char,('time'))
        UPSHoursOnBatteryData = Mergedncfile.createVariable("UPSHoursOnBattery",dtype('float').char,('time'))
        for time in MasterTimestamp:
            UPSTemperatureDataData.append(float('nan'))
            UPSHoursOnBatteryData.append(float('nan'))
    except:
        UPSTemperatureData = Mergedncfile.variables["UPSTemperature"][:]
        UPSHoursOnBatteryData = Mergedncfile.variables["UPSHoursOnBattery"][:]
    UPSTemperatureData.units = "Celcius"
    UPSHoursOnBatteryData.units = "hours"
    UPSTemperatureData.description = "Temperature of the UPS"
    UPSHoursOnBatteryData.description = "Hours operating on UPS Battery"


    try: #create the variable if you can, fill it with nans
        WSTemperatureData = Mergedncfile.createVariable("WSTemperature",dtype('float').char,('time'))
        WSRelHumData = Mergedncfile.createVariable("WSRelHum",dtype('float').char,('time'))
        WSPressureData = Mergedncfile.createVariable("WSPressure",dtype('float').char,('time'))
        WSAbsHumData = Mergedncfile.createVariable("WSAbsHum",dtype('float').char,('time'))
        for time in MasterTimestamp:
            WSTemperatureData.append(float('nan'))
            WSRelHumData.append(float('nan'))
            WSPressureData.append(float('nan'))
            WSAbsHumData.append(float('nan'))
    except:
        WSTemperatureData = Mergedncfile.variables["WSTemperature"][:]
        WSRelHumData = Mergedncfile.variables["WSRelHum"][:]
        WSPressureData = Mergedncfile.variables["WSPressure"][:]
        WSAbsHumData = Mergedncfile.variables["WSAbsHum"][:]
    WSTemperatureData.units = "Celcius"
    WSRelHumData.units = "%"
    WSPressureData.units = "Millibar"
    WSAbsHumData.units = "g/m^3"
    WSTemperatureData.description = "Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)"
    WSRelHumData.description = "Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"
    WSPressureData.description = "Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)"
    WSAbsHumData.description = "Atmospheric absolute humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"


    Channels = ["WVEtalon", "HSRLEtalon"]
    ChanTempData = []
    ChanTempDiffData = []
    for i in range (0,len(Channels)):
        ChanTempData.append([])
        ChanTempDiffData.append([])
    for i in range (0,len(Channels)):
        tempstr = Channels[i]+"Temperature"
        tempDiffstr = Channels[i]+"TempDiff"
        try: # create the variable if you can, fill it with nans until the mergeing
            ChanTempData[i] =  Mergedncfile.createVariable(tempstr,dtype('float').char,('time'))
            for time in MasterTimestamp:
                ChanTempData[i].append(float('nan'))
        except:
            ChanTempData[i] = Mergedncfile.variables[tempstr][:]
        try: # create the variable if you can, fill it with nans until the mergeing
            ChanTempDiffData[i] =  Mergedncfile.createVariable(tempDiffstr,dtype('float').char,('time'))
            for time in MasterTimestamp:
                ChanTempDiffData[i].append(float('nan'))
        except:
            ChanTempDiffData[i] = Mergedncfile.variables[tempDiffstr][:]
    for i in range (0,len(Channels)):
        ChanTempData[i].units = "Celcius"
        ChanTempDiffData[i].units = "Celcius"
        ChanTempData[i].description = "Measured temperature of the etalon from the Thor 8000 thermo-electric cooler for " + Channels[i]
        ChanTempDiffData[i].description = "Temperature difference of etalon measured Minus desired setpoint for " + Channels[i]


    ChanAssign = ["WVOnline","WVOffline","HSRL"]
    Variables = ["Wavelength", "WaveDiff", "TempDesired", "TempMeas", "Current"]
    VarUnits = ["nm","nm","Celcius","Celcius","Amp"]
    VarDescr = ["Wavelength of the seed laser measured by the wavemeter (reference to vacuum)","Wavelength of the seed laser measured by the wavemeter (reference to vacuum) Minus Desired wavelenth (reference to vacuum)","Laser temperature setpoint","Measured laser temperature from the Thor 8000 diode thermo-electric cooler","Measured laser current from the Thor 8000 diode laser controller"]
    ChanVarData = []
    for i in range (0,len(Variables)):
        ChanVarData.append([])
        for j in range (0,len(ChanAssign)):
            ChanVarData[i].append([])
    i=0
    for var in Variables:
        j=0
        for chan in ChanAssign:
            thing = chan+"Laser"+var
            try: # create the variable if you can, fill it with nans until the mergeing
                ChanVarData[i][j] = Mergedncfile.createVariable(thing ,dtype('float').char,('time'))
                for time in MasterTimestamp:
                    ChanVarData[i][j].append(float('nan'))
            except:
                ChanVarData[i][j] = Mergedncfile.variables[thing][:]
            j=j+1
        i=i+1
    # add variable units and descriptions
    for i in range (0,len(Variables)):
        for j in range (0,len(ChanAssign)):
            ChanVarData[i][j].units = VarUnits[i]
            ChanVarData[i][j].description = VarDescr[i] + " for " + ChanAssign[j]


    ChannelsIn = ["OnlineH2O", "OfflineH2O", "HSRL"]
    ChannelsOut = ["WVOnline", "WVOffline", "HSRL"]
    PowChanData = []
    for i in range (0,len(ChannelsIn)):
        PowChanData.append([])
    for i in range (0,len(ChannelsIn)):
        powthing = ChannelsOut[i]+"Power"
        try: # create the variable if you can, fill it with nans until the mergeing
            PowChanData[i] = Mergedncfile.createVariable(powthing,dtype('float').char,('time'))
            for time in MasterTimestamp:
                PowChanData[i].append(float('nan'))
        except: # variable already existed\
            PowChanData[i] = Mergedncfile.variables[powthing][:]
    for i in range (0,len(ChannelsIn)):
        PowChanData[i].units = "PIN count"
        PowChanData[i].description = "Raw pin count from the MCS analog detectors (must be converted to power using ???)"


    # setting value of range variable
    MasterRange = []
    try:
        NBinsData = dataset.variables['NBins'][:]
        for i in range (0,int(NBinsData[0])):
            MasterRange.append(i*37.5)
            # hard coded 37.5 for now which is conversion 
            # from bin number to actual range in meters     
    except:
        for i in range (0,560):
            MasterRange.append(i*37.5) 
            # hard coded for fixed number of bins in case there was no MCS data
            # also hard coded for range bins. 
    RangeData[:] = MasterRange

    # Location Variables
    try:
        LatitudeData = Mergedncfile.createVariable('latitude',dtype('double').char,())
        LongitudeData = Mergedncfile.createVariable('longitude',dtype('double').char,())
        AltitudeData = Mergedncfile.createVariable('altitude',dtype('double').char,())
        for entry in header:
            if len(entry) >0:
                if entry[0] == "latitude":
                    LatitudeData[:] = entry[len(entry)-1]
                if entry[0] == "longitude":
                    LongitudeData[:] = entry[len(entry)-1]
                if entry[0] == "altitude":
                    AltitudeData[:] = entry[len(entry)-1]            
        LatitudeData.units = "degrees_north"
        LongitudeData.units = "degrees_east"
        AltitudeData.units = "meters"
    except:
        pass
    
    # sweep variables
    try:
        SweepNumData = Mergedncfile.createVariable('sweep_number',dtype('int').char,('sweep'))
        SweepModeData = Mergedncfile.createVariable('sweep_mode','S1',('sweep','string_length'))
        FixedAngleData = Mergedncfile.createVariable('fixed_angle',dtype('float').char,('sweep'))
        SweepStartData = Mergedncfile.createVariable('sweep_start_ray_index',dtype('int').char,('sweep'))
        SweepEndData = Mergedncfile.createVariable('sweep_end_ray_index',dtype('int').char,('sweep'))
        FixedAngleData.units = "degrees"
    except:
        pass
    
    # sensor pointing variables
    try:
        AzimuthData = Mergedncfile.createVariable('azimuth',dtype('float').char,('time'))
        ElevationData = Mergedncfile.createVariable('elevation',dtype('float').char,('time'))

        # set attributes for Azimuth & Elevation
        AzimuthData.standard_name = "ray_azimuth_angle"
        AzimuthData.long_name = "azimuth_angle_from_true_north"
        AzimuthData.units = "degrees"
        AzimuthData.axis = "radial_azimuth_coordinate"
        ElevationData.standard_name = "ray_elevation_angle"
        ElevationData.long_name = "elevation_angle_from_horizontal_plane"
        ElevationData.units = "degrees"
        ElevationData.axis = "radial_elevation_coordinate"
    except:
        pass
    
    
    
    # moving platform geo-reference variables
    try:
        HeadingData = Mergedncfile.createVariable('heading',dtype('float').char,('time'))
        RollData = Mergedncfile.createVariable('roll',dtype('float').char,('time'))
        PitchData = Mergedncfile.createVariable('pitch',dtype('float').char,('time'))
        DriftData = Mergedncfile.createVariable('drift',dtype('float').char,('time'))
        RotationData = Mergedncfile.createVariable('rotation',dtype('float').char,('time'))
        TiltData = Mergedncfile.createVariable('tilt',dtype('float').char,('time'))
    
        HeadingData.units = "degrees"
        RollData.units = "degrees"
        PitchData.units = "degrees"
        DriftData.units = "degrees"
        RotationData.units = "degrees"
        TiltData.units = "degrees"
    except:
        pass
    
    
    # giving attributes to any present data fields
    try:
        WVOnlineData = dataset.variables['WVOnline'][:]
        WVOnlineData.long_name = "Water Vapor Online"
        WVOnlineData.standard_name = "WVOnline"
        WVOnlineData.units = "Photons"
        WVOnlineData._FillValue = ""
        WVOnlineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        WVOfflineData = dataset.variables['WVOffline'][:]
        WVOfflineData.long_name = "Water Vapor Offline"
        WVOfflineData.standard_name = "WVOffline"
        WVOfflineData.units = "Photons"
        WVOfflineData._FillValue = ""
        WVOfflineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        HSRLCombinedData = dataset.variables['HSRLCombined'][:]
        HSRLCombinedData.long_name = "HSRL Combined"
        HSRLCombinedData.standard_name = "HSRLCombined"
        HSRLCombinedData.units = "Photons"
        HSRLCombinedData._FillValue = ""
        HSRLCombinedData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        HSRLMolecularData = dataset.variables['HSRLMolecular'][:]
        HSRLMolecularData.long_name = "HSRL Molecular"
        HSRLMolecularData.standard_name = "HSRLMolecular"
        HSRLMolecularData.units = "Photons"
        HSRLMolecularData._FillValue = ""
        HSRLMolecularData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        O2OnlineData = dataset.variables['O2Online'][:]
        O2OnlineData.long_name = "Oxygen Online"
        O2OnlineData.standard_name = "O2Online"
        O2OnlineData.units = "Photons"
        O2OnlineData._FillValue = ""
        O2OnlineData.coordinates = "elevation azimuth range"            
    except:
        pass
        
    try:
        O2OfflineData = dataset.variables['O2Offline'][:]
        O2OfflineData.long_name = "Oxygen Offline"
        O2OfflineData.standard_name = "O2Offline"
        O2OfflineData.units = "Photons"
        O2OfflineData._FillValue = ""
        O2OfflineData.coordinates = "elevation azimuth range"            
    except:
        pass
        


# ==========called by mergeNetCDF to process MCS photon counting data============
def mergeData(Datafile, CFRadPath,nameList):
    print ("Merging MCS Data", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Datafile[-27:-19]
    fileTime = Datafile[-9:-3]
    
    print (fileDate)
    print (fileTime)
    
    DataTimestamp = []
    DataChannelAssign = []
    DataProfPerHist = []
    DataChannel = []
    DataCntsPerBin = []
    DataNBins = []
    DataDataArray = []
    
    Datadataset = Dataset(Datafile)
    
    DataTimestamp = FillVar(Datadataset, "time")
    DataProfPerHist = FillVar(Datadataset, "ProfilesPerHist")
    DataChannel = FillVar(Datadataset, "Channel")
    DataCntsPerBin = FillVar(Datadataset, "CntsPerBin")
    DataNBins = FillVar(Datadataset, "NBins")
    DataDataArray = Fill2DVar(Datadataset, "Data")
    DataChannelAssign = FillVar(Datadataset, "ChannelAssignment")
    
    #print ("hey")
    #print (len(DataTimestamp))
    #print (len(DataProfPerHist))
    #print (len(DataChannel))
    #print (len(DataCntsPerBin))
    #print (len(DataNBins))
    #print (len(DataDataArray))
    #print (len(DataChannelAssign))
    #print ("listen")

    firstChan=-1
    i=0
    for entry in DataChannelAssign:
        if firstChan < 0:
            if entry != "Unnassigned":
                firstChan = i
        i=i+1
                
    #print ("firstChan = " , firstChan)
    
    MasterTimestamp = []
    MasterWVOnline = []
    MasterWVOffline = []
    MasterHSRLCombined = []
    MasterHSRLMolecular = []
    MasterO2Online = []
    MasterO2Offline = []
    MasterProfPerHist = []
    MasterCntsPerBin = []
    MasterNBins = []
    
    NaNArray = []
    for x in range(0,int(DataNBins[0])):
        NaNArray.append(float('nan'))
        
    i=0
    for time in DataTimestamp:
        if DataChannel[i] == firstChan:
            # the following ifs are needed if a timestamp got added but data did not
            # this is likely due to the file beginning between reported channels
            # the first three should realistically never be hit. 
            if len(MasterTimestamp) > len(MasterProfPerHist):
                MasterProfPerHist.append(float('nan'))
            if len(MasterTimestamp) > len(MasterCntsPerBin):
                MasterCntsPerBin.append(float('nan'))
            if len(MasterTimestamp) > len(MasterNBins):
                MasterNBins.append(float('nan'))
            if len(MasterTimestamp) > len(MasterWVOnline):
                MasterWVOnline.append(NaNArray)
            if len(MasterTimestamp) > len(MasterWVOffline):
                MasterWVOffline.append(NaNArray)
            if len(MasterTimestamp) > len(MasterHSRLCombined):
                MasterHSRLCombined.append(NaNArray)
            if len(MasterTimestamp) > len(MasterHSRLMolecular):
                MasterHSRLMolecular.append(NaNArray)
            if len(MasterTimestamp) > len(MasterO2Online):
                MasterO2Online.append(NaNArray)
            if len(MasterTimestamp) > len(MasterO2Offline):
                MasterO2Offline.append(NaNArray)
                
            if len(MasterTimestamp) != len(MasterProfPerHist):
                print ("MasterProfPerHist length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterProfPerHist))
            if len(MasterTimestamp) != len(MasterCntsPerBin):
                print ("MasterCntsPerBin length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterCntsPerBin))
            if len(MasterTimestamp) != len(MasterNBins):
                print ("MasterNBins length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterNBins))
            if len(MasterTimestamp) != len(MasterWVOnline):
                print ("MasterWVOnline length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterWVOnline))
            if len(MasterTimestamp) != len(MasterWVOffline):
                print ("MasterWVOffline length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterWVOffline))
            if len(MasterTimestamp) != len(MasterHSRLCombined):
                print ("MasterHSRLCombined length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterHSRLCombined))
            if len(MasterTimestamp) != len(MasterHSRLMolecular):
                print ("MasterHSRLMolecular length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterHSRLMolecular))
            if len(MasterTimestamp) != len(MasterO2Online):
                print ("MasterO2Online length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterO2Online))
            if len(MasterTimestamp) != len(MasterO2Offline):
                print ("MasterO2Offline length discrepency")
                print (len(MasterTimestamp))
                print (len(MasterO2Offline))
            
            MasterTimestamp.append(time)
            MasterProfPerHist.append(DataProfPerHist[i])
            MasterCntsPerBin.append(DataCntsPerBin[i])
            MasterNBins.append(DataNBins[i])

        if DataChannelAssign[int(DataChannel[i])] == "WVOnline":
            # the next if statement is needed if we start in the middle of transmitting 
            # data and don't get the first few channels. 
            # The timestamp should be one longer at this point because we haven't 
            # yet added the data for this channel yet, but should have added the timestamp. 
            if len(MasterTimestamp) == len(MasterWVOnline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterWVOnline.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "WVOffline":
            if len(MasterTimestamp) == len(MasterWVOffline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterWVOffline.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "HSRLCombined":
            if len(MasterTimestamp) == len(MasterHSRLCombined):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterHSRLCombined.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "HSRLMolecular":
            if len(MasterTimestamp) == len(MasterHSRLMolecular):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterHSRLMolecular.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "O2Online":
            if len(MasterTimestamp) == len(MasterO2Online):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterO2Online.append(DataDataArray[i])
        if DataChannelAssign[int(DataChannel[i])] == "O2Offline":
            if len(MasterTimestamp) == len(MasterO2Offline):
                MasterTimestamp.append(time)
                MasterProfPerHist.append(DataProfPerHist[i])
                MasterCntsPerBin.append(DataCntsPerBin[i])
                MasterNBins.append(DataNBins[i])
            MasterO2Offline.append(DataDataArray[i])
        i=i+1

    # check if last entry is missing
    # this is needed if the end of file cuts off between channels
    # and is used to give one last entry to channels which are turned off
    if len(MasterTimestamp) == len(MasterProfPerHist)+1:
        MasterProfPerHist.append(float('nan'))
    if len(MasterTimestamp) == len(MasterCntsPerBin)+1:
        MasterCntsPerBin.append(float('nan'))
    if len(MasterTimestamp) == len(MasterNBins)+1:
        MasterNBins.append(float('nan'))
    if len(MasterTimestamp) == len(MasterWVOnline)+1:
        MasterWVOnline.append(NaNArray)
    if len(MasterTimestamp) == len(MasterWVOffline)+1:
        MasterWVOffline.append(NaNArray)
    if len(MasterTimestamp) == len(MasterHSRLCombined)+1:
        MasterHSRLCombined.append(NaNArray)
    if len(MasterTimestamp) == len(MasterHSRLMolecular)+1:
        MasterHSRLMolecular.append(NaNArray)
    if len(MasterTimestamp) == len(MasterO2Online)+1:
        MasterO2Online.append(NaNArray)
    if len(MasterTimestamp) == len(MasterO2Offline)+1:
        MasterO2Offline.append(NaNArray)
        
    # make sure output path exists
    SPF.ensure_dir(os.path.join(CFRadPath,fileDate,""))
    
    place = os.path.join(CFRadPath,fileDate,"MergedFiles"+fileTime+".nc")
    Mergedncfile = Dataset(place,'w')
    # timestamp defines the dimentions of variables
    Mergedncfile.createDimension('time',len(MasterTimestamp))
    Mergedncfile.createDimension('range',MasterNBins[0])
    
    # creates variables
    TimestampData = Mergedncfile.createVariable('time',dtype('float').char,('time'))

    EmptyArray = []
    for entry in MasterTimestamp:
        EmptyArray.append(float('nan'))
    Empty2DArray = []
    for entry in MasterTimestamp:
        for x in range(0,int(MasterNBins[0])):
            Empty2DArray.append(float('nan'))

    # converting from fractional hours to fractional seconds for CFRadial compliance
    for i in range(0,len(MasterTimestamp)):
        MasterTimestamp[i] = (MasterTimestamp[i] - int(MasterTimestamp[i])) *3600

    TimestampData[:] = MasterTimestamp

    ProfPerHistData = Mergedncfile.createVariable('ProfPerHist',dtype('float').char,('time'))
    CntsPerBinData = Mergedncfile.createVariable('CntsPerBin',dtype('float').char,('time'))
    NBinsData = Mergedncfile.createVariable('NBins',dtype('float').char,('time'))
    if len(MasterTimestamp) == len(MasterProfPerHist):
        ProfPerHistData[:] = MasterProfPerHist
    else:
        writeString = "ERROR: - ProfPerHistData is full Empty2DArray" + " - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)
        ProfPerHistData[:] = EmptyArray
    if len(MasterTimestamp) == len(MasterCntsPerBin):
        CntsPerBinData[:] = MasterCntsPerBin
    else:
        writeString = "ERROR: - CntsPerBinData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)
        CntsPerBinData[:] = EmptyArray
    if len(MasterTimestamp) == len(MasterNBins):
        NBinsData[:] = MasterNBins
    else:
        writeString = "ERROR: - NBinsData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(ErrorFile, writeString)
        NBinsData[:] = EmptyArray

    ProfPerHistData.units = "Number of shots"
    CntsPerBinData.units = "Unitless"
    NBinsData.units = "Unitless"

    ProfPerHistData.description = "Number of laser shots summed to create a single vertical histogram"
    CntsPerBinData.description = "The number of 5 ns clock counts that defines the width of each altitude bin. To convert to range take the value here and multiply by 5 ns then convert to range with half the speed of light"
    NBinsData.description = "Number of sequential altitude bins measured for each histogram profile"

    if 'WVOnline' in nameList:
        WVOnlineData = Mergedncfile.createVariable('WVOnline',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterWVOnline):
            WVOnlineData[:] = MasterWVOnline
        else:
            writeString = "ERROR: - WVOnlineData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            WVOnlineData[:] = Empty2DArray
        WVOnlineData.units = "Photons"
        WVOnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Water Vapor"

    if 'WVOffline' in nameList:
        WVOfflineData = Mergedncfile.createVariable('WVOffline',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterWVOffline):
            WVOfflineData[:] = MasterWVOffline
        else:
            writeString = "ERROR: - WVOfflineData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            WVOfflineData[:] = Empty2DArray
        WVOfflineData.units = "Photons"
        WVOfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

    if 'HSRLCombined' in nameList:
        HSRLCombinedData = Mergedncfile.createVariable('HSRLCombined',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterHSRLCombined):
            HSRLCombinedData[:] = MasterHSRLCombined
        else:
            writeString = "ERROR: - HSRLCombinedData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            HSRLCombinedData[:] = Empty2DArray
        HSRLCombinedData.units = "Photons"
        HSRLCombinedData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for HSRL Combined"

    if 'HSRLMolecular' in nameList:
        HSRLMolecularData = Mergedncfile.createVariable('HSRLMolecular',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterHSRLMolecular):
            HSRLMolecularData[:] = MasterHSRLMolecular
        else:
            writeString = "ERROR: - HSRLMolecularData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            HSRLMolecularData[:] = Empty2DArray
        HSRLMolecularData.units= "Photons"
        HSRLMolecularData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for HSRL Molecular"

    if 'O2Online' in nameList:
        O2OnlineData = Mergedncfile.createVariable('O2Online',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterO2Online):
            O2OnlineData[:] = MasterO2Online
        else:
            writeString = "ERROR: - O2OnlineData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            O2OnlineData[:] = Empty2DArray
        O2OnlineData.units = "Photons"
        O2OnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Oxygen"


    if 'O2Offline' in nameList:
        O2OfflineData = Mergedncfile.createVariable('O2Offline',dtype('float').char,('time','range'))
        if len(MasterTimestamp) == len(MasterO2Offline):
            O2OfflineData[:] = MasterO2Offline
        else:
            writeString = "ERROR: - O2OfflineData is full Empty2DArray - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
            SPF.Write2ErrorFile(ErrorFile, writeString)
            O2OfflineData[:] = Empty2DArray
        O2OfflineData.units = "Photons"
        O2OfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Oxygen"

    Mergedncfile.close()



# ==========called to create files for periods where there is no photon counting data============
def createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,fromTime,toTime,AveTimeDelta,nameList):
    print ("Making Merged File Without Data", datetime.datetime.utcnow().strftime("%H:%M:%S"))

    fileTime = decimal.Decimal(fromTime*10000) # decimal.Decimal is used to round down
    fileTime = str(round(fileTime,0)).zfill(6)# append extra 0s so the file names are of constant width.

    print (fileDate)
    print (fileTime)

    CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
    NetCDFPath = os.path.join(LocalOutputPath, "NetCDFOutput", "")

    SPF.ensure_dir(CFRadPath)
    SPF.ensure_dir(NetCDFPath)

    path = os.path.join(CFRadPath,fileDate,"MergedFiles"+fileTime+".nc")

    if os.path.isfile(path):
       pass
    else:
        MCSPowerFileList = SPF.getFiles(NetCDFPath, "Powsample", ".nc", ThenDate, ThenTime)
        LLFileList = SPF.getFiles(NetCDFPath, "LLsample", ".nc", ThenDate, ThenTime)
        EtalonFileList = SPF.getFiles(NetCDFPath, "Etalonsample", ".nc", ThenDate, ThenTime)
        WSFileList = SPF.getFiles(NetCDFPath, "WSsample", ".nc", ThenDate, ThenTime)

        MCSPowerFileList.sort()
        LLFileList.sort()
        EtalonFileList.sort()
        WSFileList.sort()

        needToMake = False

        for PowerFile in MCSPowerFileList:
            if needToMake == False:
                powFileDate = PowerFile[-27:-19]
                if powFileDate == fileDate:
                    MyDataset = Dataset(PowerFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for LLFile in LLFileList:
            if needToMake == False:
                LLFileDate = LLFile[-26:-18]
                if LLFileDate == fileDate:
                    MyDataset = Dataset(LLFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for EtalonFile in EtalonFileList:
            if needToMake == False:
                EtalonFileDate = EtalonFile[-30:-22]
                if EtalonFileDate == fileDate:
                    MyDataset = Dataset(EtalonFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True

        for WSFile in WSFileList:
            if needToMake == False:
                WSFileDate = WSFile[-26:-18]
                if WSFileDate == fileDate:
                    MyDataset = Dataset(WSFile)
                    TS = FillVar(MyDataset, "time")
                    firstTime = TS[0]
                    lastTime = TS[len(TS)-1]
                    if firstTime > fromTime and firstTime < toTime:
                        needToMake = True
                    if lastTime > fromTime and lastTime < toTime:
                        needToMake = True
                        needToMake = True

        # int ("needToMake = ",needToMake)
            # if needToMake:
        if True: # if i fix this if statement i get a segfault for reasons i do not understand.
            SPF.ensure_dir(path)
            Mergedncfile = Dataset(path,'w')
            # master timestamp is filled as 1/2 Hz if no file available
            MasterTimestamp = []
            time = (float(fromTime) - int(fromTime))*3600
            while time < (float(toTime) - int(fromTime))*3600:
                MasterTimestamp.append(time)
                time = time + AveTimeDelta*3600
            Mergedncfile.createDimension('time',len(MasterTimestamp))
            Mergedncfile.createDimension('range',0)
            TimestampData = Mergedncfile.createVariable('time',dtype('float').char,('time'))
            TimestampData[:] = MasterTimestamp

            emptyArray = []
            for i in range(0,len(TimestampData)):
                emptyArray.append([])
                for j in range(0,560):
                    emptyArray[i].append(float('NaN'))

            if 'WVOnline' in nameList:
                WVOnlineData = Mergedncfile.createVariable('WVOnline',dtype('float').char,('time','range'))
                WVOnlineData[:] = emptyArray
                WVOnlineData.units = "Photons"
                WVOnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Online Water Vapor"

            if 'WVOffline' in nameList:
                WVOfflineData = Mergedncfile.createVariable('WVOffline',dtype('float').char,('time','range'))
                WVOfflineData[:] = emptyArray
                WVOfflineData.units = "Photons"
                WVOfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            if 'HSRLCombined' in nameList:
                HSRLCombinedData = Mergedncfile.createVariable('HSRLCombined',dtype('float').char,('time','range'))
                HSRLCombinedData[:] = emptyArray
                HSRLCombinedData.units = "Photons"
                HSRLCombinedData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            if 'HSRLMolecular' in nameList:
                HSRLMolecularData = Mergedncfile.createVariable('HSRLMolecular',dtype('float').char,('time','range'))
                HSRLMolecularData[:] = emptyArray
                HSRLMolecularData.units = "Photons"
                HSRLMolecularData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            if 'O2Online' in nameList:
                O2OnlineData = Mergedncfile.createVariable('O2Online',dtype('float').char,('time','range'))
                O2OnlineData[:] = emptyArray
                O2OnlineData.units = "Photons"
                O2OnlineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            if 'O2Offline' in nameList:
                O2OfflineData = Mergedncfile.createVariable('O2Offline',dtype('float').char,('time','range'))
                O2OfflineData[:] = emptyArray
                O2OfflineData.units = "Photons"
                O2OfflineData.description = "A profile containing the number of photons returned in each of the sequential altitude bins for Offline Water Vapor"

            EmptyArray = []
            for entry in MasterTimestamp:
                EmptyArray.append(float('nan'))

            ProfPerHistData = Mergedncfile.createVariable('ProfPerHist',dtype('float').char,('time'))
            CntsPerBinData = Mergedncfile.createVariable('CntsPerBin',dtype('float').char,('time'))
            NBinsData = Mergedncfile.createVariable('NBins',dtype('float').char,('time'))

            ProfPerHistData[:] = EmptyArray
            CntsPerBinData[:] = EmptyArray
            NBinsData[:] = EmptyArray

            ProfPerHistData.units = "Number of shots"
            CntsPerBinData.units = "Unitless"
            NBinsData.units = "Unitless"

            ProfPerHistData.description = "Number of laser shots summed to create a single vertical histogram"
            CntsPerBinData.description = "The number of 5 ns clock counts that defines the width of each altitude bin. To convert to range take the value here and multiply by 5 ns then convert to range with half the speed of light"
            NBinsData.description = "Number of sequential altitude bins measured for each histogram profile"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Power data============
def mergePower(Powerfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Power", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Powerfile[-27:-19]
    fileTime = Powerfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    PowTimestamp = []
    PowData = []
    PowChannelAssign = []
    
    Powerdataset = Dataset(Powerfile)
    
    PowTimestamp = FillVar(Powerdataset, "time")
    PowData = FillVar(Powerdataset, "Power")
    PowChannelAssign = FillVar(Powerdataset, "ChannelAssignment")
    
    # ChannelsIn and ChannelsOut need to be the same length, 
    # In is used to read from the device file while 
    # Out is used to name the variables in the merged file 
    #ChannelsIn = ["OnlineH2O", "OfflineH2O", "HSRL", "OnlineO2", "OfflineO2"]
    #ChannelsOut = ["WVOnline", "WVOffline", "HSRL", "O2Online", "O2Offline"]
    ChannelsIn = ["OnlineH2O", "OfflineH2O", "HSRL"]
    ChannelsOut = ["WVOnline", "WVOffline", "HSRL"]
  
    PowChan = []
    for i in range (0,len(ChannelsIn)):
        PowChan.append([])
        
    for i in range(0,len(ChannelsIn)):
        for j in range(0,len(PowChannelAssign)):
            if ChannelsIn[i] == PowChannelAssign[j]:
                PowChan[i]= PowData[j].tolist()

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        PowerHour = Powerfile[-9:-7]
        if MergedHour == PowerHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstPowTime = PowTimestamp[0]
            LastPowTime = PowTimestamp[len(PowTimestamp)-1]

            if FirstPowTime < LastMergedTime or LastPowTime > FirstMergedTime:
                PowChanData = []

                for i in range (0,len(ChannelsIn)):
                    PowChanData.append([])

                for i in range (0,len(ChannelsIn)):
                    powthing = ChannelsOut[i]+"Power"
                    try: # create the variable if you can, fill it with nans until the mergeing
                        PowChanData[i] = Mergedncfile.createVariable(powthing,dtype('float').char,('time'))
                        for time in MasterTimestamp:
                            PowChanData[i].append(float('nan'))
                    except: # variable already existed
                        PowChanData[i] = Mergedncfile.variables[powthing][:]

                    # do the merging
                    PowChanData[i][:] = assign(PowChan[i],PowChanData[i],PowTimestamp,MasterTimestamp)

            for i in range (0,len(ChannelsIn)):
                PowChanData[i].units = "PIN count"
                PowChanData[i].description = "Raw pin count from the MCS analog detectors (must be converted to power using ???)"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Laser data============
def mergeLaser(LLfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Lasers", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = LLfile[-26:-18]
    fileTime = LLfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    
    #ChanAssign = ["WVOnline","WVOffline","HSRL","O2Online","O2Offline"]
    ChanAssign = ["WVOnline","WVOffline","HSRL"]
    Variables = ["Wavelength", "WaveDiff", "TempDesired", "TempMeas", "Current"]
    VarUnits = ["nm","nm","Celcius","Celcius","Amp"]
    VarDescr = ["Wavelength of the seed laser measured by the wavemeter (reference to vacuum)","Wavelength of the seed laser measured by the wavemeter (reference to vacuum) Minus Desired wavelenth (reference to vacuum)","Laser temperature setpoint","Measured laser temperature from the Thor 8000 diode thermo-electric cooler","Measured laser current from the Thor 8000 diode laser controller"]
    
    LLTimestamp = []
    LLLaserName = []
    
    LLBlockData = [] # has dimentions Variables, Timestamp
    for entry in Variables:
        LLBlockData.append([])
        
    Laserdataset = Dataset(LLfile)
    
    LLTimestamp = FillVar(Laserdataset, "time")
    LLLaserName = FillVar(Laserdataset, "LaserName")
    
    i=0
    for entry in Variables:
        LLBlockData[i] = FillVar(Laserdataset, entry)
        i=i+1
        
    ArrayTimestamp = []
    LLArrayBlockData = [] #dimentions are Variables, ChanAssign, timestamp
    
    for i in range (0,len(Variables)):
        LLArrayBlockData.append([])
        for j in range(0,len(ChanAssign)):
            LLArrayBlockData[i].append([])
            
    for i in range(0,len(ChanAssign)):
        ArrayTimestamp.append([])
        
    for i in range (0,len(LLTimestamp)):
        for j in range (0,len(ChanAssign)):
            if LLLaserName[i] == ChanAssign[j]: 
                ArrayTimestamp[j].append(LLTimestamp[i])
                for k in range(0,len(Variables)):
                    LLArrayBlockData[k][j].append(LLBlockData[k][i])

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        LLHour = LLfile[-9:-7]
        if MergedHour == LLHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstLLTime = LLTimestamp[0]
            LastLLTime = LLTimestamp[len(LLTimestamp)-1]

            if FirstLLTime < LastMergedTime or LastLLTime > FirstMergedTime:
                ChanVarData = []

                for i in range (0,len(Variables)):
                    ChanVarData.append([])
                    for j in range (0,len(ChanAssign)):
                        ChanVarData[i].append([])

                i=0
                for var in Variables:
                    j=0
                    for chan in ChanAssign:
                        thing = chan+"Laser"+var
                        try: # create the variable if you can, fill it with nans until the mergeing
                            ChanVarData[i][j] = Mergedncfile.createVariable(thing ,dtype('float').char,('time'))
                            for time in MasterTimestamp:
                                ChanVarData[i][j].append(float('nan'))
                        except:
                            ChanVarData[i][j] = Mergedncfile.variables[thing][:]
                        j=j+1
                    i=i+1

                # do the merging
                for k in range (0,len(Variables)):
                    for l in range (0,len(ChanAssign)):
                        ChanVarData[k][l] = interpolate(LLArrayBlockData[k][l],ChanVarData[k][l], ArrayTimestamp[l], MasterTimestamp)
            # add variable units and descriptions
            for i in range (0,len(Variables)):
                for j in range (0,len(ChanAssign)):
                    ChanVarData[i][j].units = VarUnits[i]
                    ChanVarData[i][j].description = VarDescr[i] + " for " + ChanAssign[j]

            Mergedncfile.close()
      


# ==========called by mergeNetCDF to process Etalon data============
def mergeEtalon(Etalonfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Etalons", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = Etalonfile[-30:-22]
    fileTime = Etalonfile[-9:-3]
    print (fileDate)
    print (fileTime)
    EtalonTimestamp = []
    EtalonNum = []
    EtalonTemp = []
    EtalonTempDiff = []
    
    #Channels = ["WVEtalon", "HSRLEtalon", "O2Etalon"]
    Channels = ["WVEtalon", "HSRLEtalon"]
    
    Etalondataset = Dataset(Etalonfile)
    
    EtalonTimestamp = FillVar(Etalondataset, "time")
    EtalonNum = FillVar(Etalondataset, "EtalonNum")
    EtalonTemp = FillVar(Etalondataset, "Temperature")
    EtalonTempDiff = FillVar(Etalondataset, "TempDiff")
    
    EtalonTimestampBlock = [] # has dimentions Channel, Timestamp
    EtalonTemperatureBlock = [] # has dimentions Channel, Timestamp
    EtalonTempDiffBlock = [] # has dimentions Channel, Timestamp
    
    for entry in Channels:
        EtalonTimestampBlock.append([])
        EtalonTemperatureBlock.append([])
        EtalonTempDiffBlock.append([])
        
    for i in range(0,len(EtalonTimestamp)):
        for j in range(0,len(Channels)):
            if EtalonNum[i] == Channels[j]:
                EtalonTimestampBlock[j].append(EtalonTimestamp[i])
                EtalonTemperatureBlock[j].append(EtalonTemp[i])
                EtalonTempDiffBlock[j].append(EtalonTempDiff[i])

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        EtalonHour = Etalonfile[-9:-7]
        if MergedHour == EtalonHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstEtalonTime = EtalonTimestamp[0]
            LastEtalonTime = EtalonTimestamp[len(EtalonTimestamp)-1]

            if FirstEtalonTime < LastMergedTime or LastEtalonTime > FirstMergedTime:
                ChanTempData = []
                ChanTempDiffData = []

                for i in range (0,len(Channels)):
                    ChanTempData.append([])
                    ChanTempDiffData.append([])

                for i in range (0,len(Channels)):
                    tempstr = Channels[i]+"Temperature"
                    tempDiffstr = Channels[i]+"TempDiff"
                    try: # create the variable if you can, fill it with nans until the mergeing
                        ChanTempData[i] =  Mergedncfile.createVariable(tempstr,dtype('float').char,('time'))
                        ChanTempDiffData[i] =  Mergedncfile.createVariable(tempDiffstr,dtype('float').char,('time'))
                        for time in MasterTimestamp:
                            ChanTempData[i].append(float('nan'))
                            ChanTempDiffData[i].append(float('nan'))
                    except:
                        ChanTempData[i] = Mergedncfile.variables[tempstr][:]
                        ChanTempDiffData[i] = Mergedncfile.variables[tempDiffstr][:]

                # do the merging
                for i in range (0,len(Channels)):
                     ChanTempData[i] = interpolate(EtalonTemperatureBlock[i], ChanTempData[i], EtalonTimestampBlock[i], MasterTimestamp)
                     ChanTempDiffData[i] = interpolate(EtalonTempDiffBlock[i], ChanTempDiffData[i], EtalonTimestampBlock[i], MasterTimestamp)

            for i in range (0,len(Channels)):
                ChanTempData[i].units = "Celcius"
                ChanTempDiffData[i].units = "Celcius"
                ChanTempData[i].description = "Measured temperature of the etalon from the Thor 8000 thermo-electric cooler for " + Channels[i]
                ChanTempDiffData[i].description = "Temperature difference of etalon measured Minus desired setpoint for " + Channels[i]

            Mergedncfile.close()



# ==========called by mergeNetCDF to process WeatherStation data============
def mergeWS(WSfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging WeatherStation", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = WSfile[-26:-18]
    fileTime = WSfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    WSTimestamp = []
    WSTemperature = []
    WSRelHum = []
    WSPressure = []
    WSAbsHum = []
    
    WSdataset = Dataset(WSfile)
    
    WSTimestamp = FillVar(WSdataset, "time")
    WSTemperature = FillVar(WSdataset, "Temperature")
    WSRelHum = FillVar(WSdataset, "RelHum")
    WSPressure = FillVar(WSdataset, "Pressure")
    WSAbsHum = FillVar(WSdataset, "AbsHum")

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        WSHour = WSfile[-9:-7]
        if MergedHour == WSHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstWSTime = WSTimestamp[0]
            LastWSTime = WSTimestamp[len(WSTimestamp)-1]

            if FirstWSTime < LastMergedTime or LastWSTime > FirstMergedTime:

                try: #create the variable if you can, fill it with nans until the mergeing
                    WSTemperatureData = Mergedncfile.createVariable("WSTemperature",dtype('float').char,('time'))
                    WSRelHumData = Mergedncfile.createVariable("WSRelHum",dtype('float').char,('time'))
                    WSPressureData = Mergedncfile.createVariable("WSPressure",dtype('float').char,('time'))
                    WSAbsHumData = Mergedncfile.createVariable("WSAbsHum",dtype('float').char,('time'))
                    for time in MasterTimestamp:
                        WSTemperatureData.append(float('nan'))
                        WSRelHumData.append(float('nan'))
                        WSPressureData.append(float('nan'))
                        WSAbsHumData.append(float('nan'))
                except:
                    WSTemperatureData = Mergedncfile.variables["WSTemperature"][:]
                    WSRelHumData = Mergedncfile.variables["WSRelHum"][:]
                    WSPressureData = Mergedncfile.variables["WSPressure"][:]
                    WSAbsHumData = Mergedncfile.variables["WSAbsHum"][:]

                WSTemperatureData = interpolate(WSTemperature, WSTemperatureData, WSTimestamp, MasterTimestamp)
                WSRelHumData = interpolate(WSRelHum, WSRelHumData, WSTimestamp, MasterTimestamp)
                WSPressureData = interpolate(WSPressure, WSPressureData, WSTimestamp, MasterTimestamp)
                WSAbsHumData = interpolate(WSAbsHum, WSAbsHumData, WSTimestamp, MasterTimestamp)

            WSTemperatureData.units = "Celcius"
            WSRelHumData.units = "%"
            WSPressureData.units = "Millibar"
            WSAbsHumData.units = "g/m^3"

            WSTemperatureData.description = "Atmospheric temperature measured by the weather station at the ground (actual height is 2 meters at the top of the container)"
            WSRelHumData.description = "Atmospheric relative humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"
            WSPressureData.description = "Atmospheric pressure mesaured by the weather station at ground level (actual height is 2 meters at the top of the container)"
            WSAbsHumData.description = "Atmospheric absolute humidity measured by the weather station at ground level (actual height is 2 meters at the top of the container)"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process Housekeeping data============
def mergeHKeep(HKeepfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging Housekeeping", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = HKeepfile[-29:-21]
    fileTime = HKeepfile[-9:-3]
    print (fileDate)
    print (fileTime)

    HKeepTimestamp = []
    HKeepTemperature = []
    
    HKeepdataset = Dataset(HKeepfile)
    
    HKeepTimestamp = FillVar(HKeepdataset, "time")
    HKeepTemperature = FillVar(HKeepdataset, "Temperature")

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        HKeepHour = HKeepfile[-9:-7]
        if MergedHour == HKeepHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstHKeepTime = HKeepTimestamp[0]
            LastHKeepTime = HKeepTimestamp[len(HKeepTimestamp)-1]

            if FirstHKeepTime < LastMergedTime or LastHKeepTime > FirstMergedTime:
                try: #create the variable if you can, fill it with nans until the mergeing
                    nSensors = len(HKeepTemperature)
                    Mergedncfile.createDimension('nInternalThermalSensors',nSensors)
                    HKeepTemperatureData = Mergedncfile.createVariable("HKeepTemperature",dtype('float').char,('nInternalThermalSensors','time'))
                except:
                    HKeepTemperatureData = Mergedncfile.variables["HKeepTemperature"][:]

                for i in range(0,len(HKeepTemperature)-1):
                    HKeepTemperatureData[i] = interpolate(list(HKeepTemperature[i]), HKeepTemperatureData[i], HKeepTimestamp, MasterTimestamp)

            HKeepTemperatureData.units = "Celcius"

            HKeepTemperatureData.description = "Temperature measured inside the container by nInternalThermalSensors"

            Mergedncfile.close()



# ==========called by mergeNetCDF to process UPS data============
def mergeUPS(UPSfile, CFRadPath, ThenDate, ThenTime):
    print ("Merging UPS", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    fileDate = UPSfile[-27:-19]
    fileTime = UPSfile[-9:-3]
    print (fileDate)
    print (fileTime) 
    UPSTimestamp = []
    UPSTemperature = []
    UPSHoursOnBattery = []
    
    UPSdataset = Dataset(UPSfile)

    UPSTimestamp = FillVar(UPSdataset, "time")
    UPSTemperature = FillVar(UPSdataset, "UPSTemperature")
    UPSHoursOnBattery = FillVar(UPSdataset, "HoursOnBattery")

    MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
    MergedFileList.sort()
    for Mergedfile in MergedFileList:
        MergedHour = Mergedfile[-9:-7]
        UPSHour = UPSfile[-9:-7]
        if MergedHour == UPSHour:
            Mergedncfile = Dataset(Mergedfile,'a')
            MasterTimestamp = Mergedncfile.variables['time'][:]
            FirstMergedTime = MasterTimestamp[0]
            LastMergedTime = MasterTimestamp[len(MasterTimestamp)-1]
            FirstUPSTime = UPSTimestamp[0]
            LastUPSTime = UPSTimestamp[len(UPSTimestamp)-1]

            if FirstUPSTime < LastMergedTime or LastUPSTime > FirstMergedTime:

                try: #create the variable if you can, fill it with nans until the mergeing
                    UPSTemperatureData = Mergedncfile.createVariable("UPSTemperature",dtype('float').char,('time'))
                    UPSHoursOnBatteryData = Mergedncfile.createVariable("UPSHoursOnBattery",dtype('float').char,('time'))
                    for time in MasterTimestamp:
                        UPSTemperatureDataData.append(float('nan'))
                        UPSHoursOnBatteryData.append(float('nan'))
                except:
                    UPSTemperatureData = Mergedncfile.variables["UPSTemperature"][:]
                    UPSHoursOnBatteryData = Mergedncfile.variables["UPSHoursOnBattery"][:]

                UPSTemperatureData = interpolate(UPSTemperature, UPSTemperatureData, UPSTimestamp, MasterTimestamp)
                UPSHoursOnBatteryData = interpolate(list(UPSHoursOnBattery), UPSHoursOnBatteryData, UPSTimestamp, MasterTimestamp)

            UPSTemperatureData.units = "Celcius"
            UPSHoursOnBatteryData.units = "hours"

            UPSTemperatureData.description = "Temperature of the UPS"
            UPSHoursOnBatteryData.description = "Hours operating on UPS Battery"

            Mergedncfile.close()



# ------------------------------merged files ------------------------------
# read in raw NetCDF files and merge them into one file. 
def mergeNetCDF(ThenDate,ThenTime,NowDate,NowTime,LastTime,LocalOutputPath,header,WarningFile,ErrorFile):
    print ("Creating Merged files", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    SPF.ensure_dir(LocalOutputPath)
    NetCDFPath = os.path.join(LocalOutputPath,"NetCDFOutput","")
    SPF.ensure_dir(NetCDFPath)
    CFRadPath = os.path.join(LocalOutputPath, "CFRadialOutput", "")
    SPF.ensure_dir(CFRadPath)
    if os.path.isdir(NetCDFPath):
        MCSDataFileList = SPF.getFiles(NetCDFPath, "MCSsample", ".nc", ThenDate, ThenTime)
        MCSPowerFileList = SPF.getFiles(NetCDFPath, "Powsample", ".nc", ThenDate, ThenTime)
        LLFileList = SPF.getFiles(NetCDFPath, "LLsample", ".nc", ThenDate, ThenTime)
        EtalonFileList = SPF.getFiles(NetCDFPath, "Etalonsample", ".nc", ThenDate, ThenTime)
        WSFileList = SPF.getFiles(NetCDFPath, "WSsample", ".nc", ThenDate, ThenTime)
        HKeepFileList = SPF.getFiles(NetCDFPath, "HKeepsample", ".nc", ThenDate, ThenTime)
        UPSFileList = SPF.getFiles(NetCDFPath, "UPSsample", ".nc", ThenDate, ThenTime)

        MCSDataFileList.sort()
        MCSPowerFileList.sort()
        LLFileList.sort()
        EtalonFileList.sort()
        WSFileList.sort()

        # ==========creates merged files and processes data==========

        firstTime = -1
        lastTime = -1

        for Datafile in MCSDataFileList:
            fileDate = Datafile[-27:-19]
            fileTime = Datafile[-9:-3]

            # begin with checking for gaps in data files and create placeholder files for missing data
            Datadataset = Dataset(Datafile)
            DataTimestamp = FillVar(Datadataset, "time")
            DataChannelAssign = FillVar(Datadataset, "ChannelAssignment")
            DataChannel = FillVar(Datadataset, "Channel")

            firstTime = DataTimestamp[0]

            timedeltaSum = 0
            timecounter = 0
            timeCheck=0
            name = ""
            nameList = []
            for i in range(0,len(DataTimestamp)-1):
                if i==0:
                    name = DataChannelAssign[int(DataChannel[i])]
                    timeCheck = DataTimestamp[i]
                elif DataChannelAssign[int(DataChannel[i])] == name:
                    timecounter = timecounter + 1
                    timedeltaSum = timedeltaSum + (DataTimestamp[i] - timeCheck)
                    timeCheck = DataTimestamp[i]
                if not DataChannelAssign[int(DataChannel[i])] in nameList:
                    nameList.append(DataChannelAssign[int(DataChannel[i])])

            if timecounter > 0:
                AveTimeDelta = timedeltaSum/timecounter
            else:
                AveTimeDelta = 2
                
            nTimeDeltasGap = 3

            #print ("FT=",firstTime)
            #print ("LT=",lastTime)
            #print ("ATD=",AveTimeDelta)
            #print ("Diff=",firstTime - lastTime)

            if lastTime < 0:  # this case covers the beginning of the running period

                okDate = 0  # I'm limiting how long it will make files before the beginning of data taking
                # once createEmptyDataFile is fixed and no longer segfaulting okDate will not be needed.
                if int(ThenDate) < (int(fileDate) - 1):
                    okDate = int(fileDate)
                else:
                    okDate = ThenDate

                # for date in range (int(ThenDate),int(fileDate)+1):
                for date in range(int(okDate), int(fileDate) + 1):
                    # print ("date=",date)
                    startTime = 0
                    endTime = 0

                    if date == int(fileDate) and date != int(ThenDate):
                        startTime = 0
                        endTime = int(int(fileTime) / 10)
                    elif date == int(fileDate) and date == int(ThenDate):
                        startTime = int(ThenTime+1)*1000
                        endTime = int(int(fileTime) / 10)
                    elif date != int(fileDate) and date != int(ThenDate):
                        startTime = 0
                        endTime = 24000
                    elif date != int(fileDate) and date == int(ThenDate):
                        startTime = int(ThenTime+1)*1000
                        endTime = 24000

                    for time in range(int(startTime / 1000), int(endTime / 1000)):
                        createEmptyDataFile(LocalOutputPath, str(date), ThenDate, ThenTime, int(time), int(time + 1), AveTimeDelta,nameList)

                if firstTime - int(firstTime) > nTimeDeltasGap * AveTimeDelta:  # covers the fractional hour potentially missed at beginning of data collection
                    createEmptyDataFile(LocalOutputPath, fileDate, ThenDate, ThenTime, int(firstTime), firstTime, AveTimeDelta,nameList)

            else: # if this is not our first time through
                if firstTime - lastTime > nTimeDeltasGap*AveTimeDelta:
                    intDiff = int(firstTime)-int(lastTime)
                    if intDiff > 0: # we crossed at least one hour boundry
                        for i in range(0,intDiff+1): # number of files needed to account for crossing hour boundries without data
                            if i ==0: # first partial hour missed
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta,nameList)
                            elif i == intDiff: # last partial hour potentially missed
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,int(firstTime),firstTime,AveTimeDelta,nameList)
                            else: # any full hours that were missed in the middle
                                createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,int(lastTime)+i,int(lastTime)+i+1,AveTimeDelta,nameList)
                    else:# the gap is contained within one hour
                        createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,firstTime,AveTimeDelta,nameList)

            try:
                mergeData(Datafile, CFRadPath,nameList)
            except:
                writeString = "ERROR: unable to merge MCSData into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(ErrorFile, writeString)

            lastTime = DataTimestamp[len(DataTimestamp)-1]

            if Datafile == MCSDataFileList[len(MCSDataFileList)-1]: # this case covers the end of the running period
                if fileDate != NowDate:
                    if int(lastTime) + 1 - lastTime > nTimeDeltasGap*AveTimeDelta:# covers last fractional hour at end of list
                        createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta,nameList)
                else:
                    if int(lastTime) + 1 < NowTime:
                        if int(lastTime) + 1 - lastTime > nTimeDeltasGap*AveTimeDelta:# covers last fractional hour at end of list
                            createEmptyDataFile(LocalOutputPath,fileDate,ThenDate,ThenTime,lastTime,int(lastTime)+1,AveTimeDelta,nameList)

                # I'm limiting how long it will make files past the end of data taking
                # when createEmptyDataFile is fixed i can replace the for loop
                #for date in range (int(fileDate),int(NowDate)+1):
                for date in range (int(fileDate),int(fileDate) +1):
                    #print ("date=",date)
                    startTime = 0
                    endTime = 0
                    if date == int(fileDate) and date != int(NowDate):
                        startTime = int(int(fileTime)/10+1000)
                        endTime = 24000
                    elif date == int(fileDate) and date == int(NowDate):
                        startTime = int(int(fileTime)/10+1000)
                        endTime = int((int(NowTime))*1000)
                    elif date != int(fileDate) and date != int(NowDate):
                        startTime = 0
                        endTime = 24000
                    elif date != int(fileDate) and date == int(NowDate):
                        startTime = 0
                        endTime = int((int(NowTime))*1000)

                    for time in range (int(startTime/1000),int(endTime/1000)):
                        createEmptyDataFile(LocalOutputPath,str(date),ThenDate,ThenTime,int(time),int(time+1),AveTimeDelta,nameList)

        for Powerfile in MCSPowerFileList:
            try:
                mergePower(Powerfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "WARNING: unable to merge MCSPower into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

        for LLfile in LLFileList:
            try:
                mergeLaser(LLfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "ERROR: unable to merge LaserLocking into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(ErrorFile, writeString)

        for Etalonfile in EtalonFileList:
            try:
                mergeEtalon(Etalonfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "WARNING: unable to merge Etalons into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

        for WSfile in WSFileList:
            try:
                mergeWS(WSfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "WARNING: unable to merge WeatherStation into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

        for HKeepfile in HKeepFileList:
            try:
                mergeHKeep(HKeepfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "WARNING: unable to merge Housekeeping into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

        for UPSfile in UPSFileList:
            try:
                mergeUPS(UPSfile, CFRadPath, ThenDate, ThenTime)
            except:
                writeString = "WARNING: unable to merge WeatherStation into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

        MergedFileList = SPF.getFiles(CFRadPath, "Merged", ".nc", ThenDate, ThenTime)
        MergedFileList.sort()
        for Mergedfile in MergedFileList:
            try:
                CFRadify(Mergedfile,CFRadPath,header)
            except:
                writeString = "WARNING: unable to put CFRadial formatting into CFRadial file - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
                SPF.Write2ErrorFile(WarningFile, writeString)

