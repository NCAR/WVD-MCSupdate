
import sys
from netCDF4 import Dataset

import os
import sys
import time
import csv
import datetime
import struct
import binascii
import math
import shutil
import numpy as np
from datetime import timedelta 
from netCDF4 import Dataset
from numpy import arange, dtype 
from copy import copy

def FillVar(dataset, varName):
    var = dataset.variables[varName][:]
    varFill = []
    i=0
    for entry in var:
        varFill.append(var[i])
        i=i+1
    return varFill
            

path = "/h/eol/brads/git/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/NetCDFOutput/20180515/Etalonsample184909.nc"

dataset = Dataset(path)

print (dataset.file_format)
print (dataset)
print (dataset.dimensions.keys())
print (dataset.dimensions['time'])
print (dataset.variables.keys()) 

print (path)
Datadataset = Dataset(path)
DataTimestamp = FillVar(Datadataset, "time")

checkFirstTime = DataTimestamp[0]
checkLastTime = DataTimestamp[len(DataTimestamp)-1]

print ("DataTimestamp=",DataTimestamp)
print ("checkFirstTime=",checkFirstTime)
print ("checkLastTime=",checkLastTime)
