

import subprocess

syncFrom = '/cygdrive/c/Users/h2odial/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/'
syncTo   = '/cygdrive/d/MPDBackup/'

#process = subprocess.Popen(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", syncFrom, syncTo], stdout=subprocess.PIPE)
#stdout = process.communicate()[0]
#print(stdout.decode('utf-8'))

subprocess.call(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", syncFrom, syncTo])
