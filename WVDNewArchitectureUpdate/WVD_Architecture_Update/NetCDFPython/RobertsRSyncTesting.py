

import subprocess

syncFrom = '/cygdrive/c/Users/h2odial/WVD-MCSupdate/WVDNewArchitectureUpdate/WVD_Architecture_Update/Data/'
syncTo   = '/cygdrive/d/MPDBackup/'

subprocess.call(["C:\\Program Files (x86)\\ICW\\bin\\rsync.exe", "-avz", "--compress-level=9", syncFrom, syncTo])
