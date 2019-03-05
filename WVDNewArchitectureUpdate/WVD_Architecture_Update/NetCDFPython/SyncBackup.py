import subprocess
import SharedPythonFunctions as SPF

def DoRSync(syncFrom, syncTo,WarningFile,ErrorFile):
    #subprocess.call(["C:\\Users\\eol-lidar\\Desktop\\BaseSoftwareForGIT\\InstallPrograms\\Rsync\\OLD\\cwRsync_5.4.1_x86_Free\\rsync.exe", "-avz", "--compress-level=9", syncFrom, syncTo])
    # subprocess.call(["rsync", "-az", "--compress-level=9", syncFrom, syncTo])
    
    subprocess.call(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", 
                     SPF.convertString2CWSyntax(syncFrom)+ '/Data/', 
                     SPF.convertString2CWSyntax(syncTo)] )

