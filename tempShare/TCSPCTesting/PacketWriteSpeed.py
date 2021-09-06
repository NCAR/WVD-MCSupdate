

import glob, os
from datetime import datetime
import matplotlib.pyplot as plt
# Finging the  file list
#FileList = glob.glob('C:\\Users\\h2odial\\Desktop\\20210714\\' + 'TCSPC_*.bin')
FileList = glob.glob('D:\\20210714\\Evening\\' + 'TCSPC_*.bin')
# Determining the number of packets in each file (each packet has a 8 byte time
# stamp, 1056 byte payload, and a 2 byte footer)
PacketNums = [os.path.getsize(File)/(1056+8+2.) for File in FileList]
# Determining the time each file was initiated 
FileTimes = [datetime.strptime(File[-19:-4], '%Y%m%d_%H%M%S') for File in FileList]
# Determining how long it took to write a file
FileWriteTimes = [(FileTimes[i+1] - FileTimes[i]).seconds for i in range(0,len(FileTimes)-1)]
# Determiing how many packets per second were written
PPS = [PacketNum/FileWriteTime for [FileWriteTime,PacketNum] in zip(FileWriteTimes,PacketNums)]

plt.plot(PPS)