
import os
from datetime import datetime
import matplotlib.pyplot as plt

def PacketWriteSpeed(FileList):
    # Determining the number of packets in each file (each packet has a 8 byte time
    # stamp, 1056 byte payload, and a 2 byte footer)
    PacketNums = [os.path.getsize(File)/(1056+8+2.) for File in FileList]
    # Determining the time each file was initiated 
    FileTimes = [datetime.strptime(File[-19:-4], '%Y%m%d_%H%M%S') for File in FileList]
    # Determining how long it took to write a file
#    FileWriteTimes = [(FileTimes[i+1] - FileTimes[i]).days for i in range(0,len(FileTimes)-1)]
    FileWriteTimes = [(FileTimes[i+1] - FileTimes[i]).seconds for i in range(0,len(FileTimes)-1)]
    
    # Determiing how many packets per second were written
    PPS = [PacketNum/FileWriteTime for [FileWriteTime,PacketNum] in zip(FileWriteTimes,PacketNums)]
    return(FileTimes,PPS)
    
def PlotLoadStats(FileList, Missing, PPS):
    FileTimes = [datetime.strptime(File[-19:-4], '%Y%m%d_%H%M%S') for File in FileList]
    # Plotting the number of missed packets from UDP
    fig,ax = plt.subplots()
    ax.plot(FileTimes,Missing, color="red", marker="o")
    ax.set_xlabel("File Time",fontsize=14)
    # set y-axis label
    ax.set_ylabel("Missing Packets",color="red",fontsize=14)
#    ax.set_yscale('log')
    # Plotting the packets per second of arrival 
    ax2=ax.twinx()
    ax2.plot(FileTimes[:-1], PPS,color="blue",marker="o")
    ax2.set_ylabel("Packets Per Second",color="blue",fontsize=14)
    
    fig.set_size_inches(8, 5)