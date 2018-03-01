#NetCDF writer for NCAR WVD system
#Brad Schoenrock
#Feb. 2018
# useage:
# python MyScript.py [working directory containing Data folder] [how many hours back in time to process]

import os
import sys
import time
import datetime
from netCDF4 import Dataset
from numpy import arange, dtype # array module from http://numpy.scipy.org

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

# --------------------------------main------------------------------------
def main():
    print ("hello world")
    print (time.ctime())
    print ("These are the arguments I passed in to my test script:")
    for i in range(0,len(sys.argv)-1):
        print (sys.argv[i+1])
    
    print (" ")
    print (" ")
    
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            if is_number(sys.argv[2]):
                print ("go back",sys.argv[2],"hours")
                #Do stuff here !!!!!!

                #check for children data dirs

                #grab last sys.argv[2] hours of data

                #check if NetCDF child directory exists & create if needed

                #write files
                
                #process into NetCDF files
                
            else:
                print (sys.argv[1],"is a dir, but",sys.argv[2],"is not a number")
        else:
            print (sys.argv[1],"is not a dir, looking for directory containing Data")


    # ------------ trash below here once done ----------------------- 
    # the output array to write will be nx x ny
    nx = 6; ny = 12
    # open a new netCDF file for writing.
    ncfile = Dataset('simple_xy.nc','w') 
    # create the output data.
    data_out = arange(nx*ny) # 1d array
    data_out.shape = (nx,ny) # reshape to 2d array
    # create the x and y dimensions.
    ncfile.createDimension('x',nx)
    ncfile.createDimension('y',ny)
    # create the variable (4 byte integer in this case)
    # first argument is name of variable, second is datatype, third is
    # a tuple with the names of dimensions.
    data = ncfile.createVariable('data',dtype('int32').char,('x','y'))
    # write data to variable.
    data[:] = data_out
    # close the file.
    ncfile.close()
    print ('*** SUCCESS writing example file simple_xy.nc!')

if __name__ == '__main__':
    main()

