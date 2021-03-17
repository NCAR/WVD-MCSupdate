# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# This set of functions is used to call data rsyncing from labview. If the 
# program is not called directly, it assumes that the user just wants to backup
# all MPD data to the standard backup drive location. 

import subprocess, SharedPythonFunctions as SPF

def DoRSync(syncFrom, syncTo,WarningFile=None,ErrorFile=None):
    process = subprocess.Popen(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", 
                                SPF.convertString2CWSyntax(syncFrom)+ '/Data/', 
                                SPF.convertString2CWSyntax(syncTo)],stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    return stdout.decode('utf-8')


if __name__ == '__main__':
    # Default directories to rsync
    syncFrom = 'C:\\Users\\h2odial\\WVD-MCSupdate\\WVDNewArchitectureUpdate\\WVD_Architecture_Update\\Data'
    syncTo   = 'D:\\MPDBackup'
    # Performing the rsyncing with no logging
    Output = DoRSync(syncFrom, syncTo)
    print(Output)

