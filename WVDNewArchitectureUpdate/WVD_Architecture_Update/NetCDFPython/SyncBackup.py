import subprocess
import SharedPythonFunctions as SPF

def DoRSync(syncFrom, syncTo,WarningFile,ErrorFile):
    process = subprocess.Popen(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", 
                                SPF.convertString2CWSyntax(syncFrom)+ '/Data/', 
                                SPF.convertString2CWSyntax(syncTo)],stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    return stdout.decode('utf-8')
