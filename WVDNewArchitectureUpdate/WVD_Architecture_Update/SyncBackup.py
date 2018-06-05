import subprocess

def DoRSync(syncFrom, syncTo):
    subprocess.call(["rsync", "-az", syncFrom, syncTo])

