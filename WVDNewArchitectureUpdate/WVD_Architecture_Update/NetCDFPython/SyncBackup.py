import subprocess
import datetime
import os
import shutil
import SharedPythonFunctions as SPF

def DoRSync(syncFrom, syncTo,WarningFile,ErrorFile):
    #subprocess.call(["C:\\Users\\eol-lidar\\Desktop\\BaseSoftwareForGIT\\InstallPrograms\\Rsync\\OLD\\cwRsync_5.4.1_x86_Free\\rsync.exe", "-avz", "--compress-level=9", syncFrom, syncTo])
    subprocess.call(["rsync", "-avz", "--compress-level=9", syncFrom, syncTo])
