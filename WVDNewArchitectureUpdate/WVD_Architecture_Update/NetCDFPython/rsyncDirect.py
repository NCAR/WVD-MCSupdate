# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# This set of functions is used to call data rsyncing from labview. It just allows
# the user to see the rsync output directly and doesn't have to wait until process
# return. 

import subprocess

syncFrom = '/cygdrive/c/Users/h2odial/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/'
syncTo   = '/cygdrive/d/MPDBackup/'

subprocess.call(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-av", syncFrom, syncTo])