# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# This set of functions is used to call data rsyncing from labview. It just allows
# the user to see the rsync output directly and doesn't have to wait until process
# return. 

import os, subprocess, time

def RunProcess(syncFrom,syncTo):
    try:
        process = subprocess.run(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-av", syncFrom, syncTo],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return(process.stdout.decode("utf-8"),process.stderr.decode("utf-8"))
    except:
        return('FAILED\n','Failed to run rsync from python\n')
    
if __name__ == '__main__':
    # Defining paths to the write data logs to
    LogPath =  os.path.join(os.path.split(os.getcwd())[0],'Data','RSync')
    DailyFolder = time.strftime("%Y%m%d",time.gmtime())
    FileName = "RsyncLog_" + time.strftime("%Y%m%d_%H%M%S",time.gmtime()) + ".txt"
    ParentDir = os.path.join(LogPath,DailyFolder)
    
    # Definign the file paths to rsync
    syncFrom = '/cygdrive/c/Users/h2odial/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/'
    syncToA   = '/cygdrive/d/MPDBackup/'
    syncToB   = '/cygdrive/e/MPDBackup/'
    
    # Defining the text to help the user understand the data file 
    Header = "========================Calling Rsyncing========================\n" + \
             " Started at: " + time.strftime("%Y%m%d_%H:%M:%S",time.gmtime()) + "\n\n"
             
    # Perform rsync to data drive A
    OutA,ErrA = RunProcess(syncFrom,syncToA)
    # Perform rsync to data drive B
    OutB,ErrB = RunProcess(syncFrom,syncToB)
    
    time.sleep(5)
    
    # Defining the text to help the user understand the data file 
    Footer = "\n=========================Ending Rsyncing========================\n" + \
             " Ended at: " + time.strftime("%Y%m%d_%H:%M:%S",time.gmtime()) + "\n"
    
    # Writting data file
    try:
        if not os.path.exists(ParentDir):
            os.makedirs(ParentDir)
        with open(os.path.join(ParentDir,FileName),"w") as textfile:
            textfile.write(Header+OutA+ErrA+OutB+ErrB+Footer)
    except:
        pass