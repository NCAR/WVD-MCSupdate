
import struct, math, itertools, glob
import numpy as np
import TCSPCPacketInfo as TTInfo

# This function is used to convert a 4 byte word into a 32 bit number. The word
# contained in the sub-list D.
def Read4ByteWord(D):
    return(ord(D[3:4])*2**24+ord(D[2:3])*2**16+ord(D[1:2])*2**8+ord(D[0:1]))
# This function creates a string of bits. The words are contained in an array D
# with the start and end indices of the desired string of the array given. 
def CreateString(D,Start,End):
    return(''.join('{:08b}'.format(ord(D[i:i+1])) for i in range(Start,End)))   
def CreateRString(D,Start,End):
    return(''.join('{:08b}'.format(ord(D[i-1:i])) for i in range(Start,End,-1))) 
# This function is used to check if a data chunk is equal to an expected value. 
# It creates a bit string from both the known Check word and a Data array using
# Start and End indices given. 
def CheckHeaderFooter(Data,Start,End,Check):
    if CreateString(Data,Start,End) != ''.join('{:08b}'.format(ord(x)) for x in Check):
        print('The TCSPC header/footer word does not match the expected value. ~RS')
        return(True)
    else:
        return(False)
# This function uses the pre-defined TCSPC bulk data sub-frame structure and  
# parses known elements from it. It retuns a tuple of data contained within a  
# single frame of data.    
def UnpackPulseFrame(D):
    # Converting byte literal into a string and reversing so that its indices 
    # match Josh's documentation
    Bits = CreateRString(D,4,0)[::-1]
    # Defining the types of time stamps possible
    BitStringTypes = {'00':0,'01':1,'10':2,'11':3}
    # Unpacking payload information
    TDiff  = int(Bits[0:16][::-1],2)
    Status = int(Bits[24:28][::-1])
    Sync   = int(Bits[30:32][::-1],2)
    Type   = BitStringTypes[Bits[28:30][::-1]]
    if Type == 2:
        Channel_RTime = int(math.log2(int(Bits[16:24][::-1],2)))
    elif Type == 1:
        Channel_RTime = int(Bits[16:24][::-1],2)
    else:
        Channel_RTime = -1
    # Return data from the payload
    return(Type,Sync,Channel_RTime,TDiff,Status)

# This function uses the pre-defined TCSPC bulk data frame structure and parses
# known elements from it. It returns a list of data contained within a single 
# data packet. 
def ReadTimeTagPayload(Payload):
    # Checking known packet structure matches data read
    Error = [CheckHeaderFooter(Payload, 0, 4,'\x00\x00\x46\x54'), \
             CheckHeaderFooter(Payload, 4 ,8,'\x00\x00\x00\x00'), \
             CheckHeaderFooter(Payload,28,32,'\x00\x00\x00\x00')]   
    # Pre-allocating data list
    Data = [[] for i in range(11)]
    # Word03: relTime, Word04: chPulseCnt, Word05: syncPulseCnt, Word06: statusPulseFrame
    for Bytes in range(3,7):
        Data[Bytes-3].append(Read4ByteWord(Payload[(4*Bytes):(4*(Bytes+1))]))         
    # Payload size from Word02
    PayloadSize = ord(Payload[9:10])*2**8 + ord(Payload[8:9])
    Data[4].append(PayloadSize)
    # Packet Counter from Word02
    Data[5].append(ord(Payload[11:12])*2**8 + ord(Payload[10:11])) 
#    # Unpacking time stamps and the meta-data therewith
#    for Index in range(0,int(PayloadSize/4)):
#        A = list(UnpackPulseFrame(Payload[32+(Index*4):32+((Index+1)*4)]))
#        for SubIndex in range(0,len(A)):
#            Data[SubIndex+6].append(A[SubIndex])
    # If there are no observed errors, return the data as a tuple    
    if any(Error):
        return([],True)
    else:
        return(Data, False)               
# This function is used to read a full TCSPC bulk data file. It loops over the 
# contents of the file and parses it. Assuming all data is written correctly, 
# it returns a list of data. If the check values are not recognized, it returns
# and empty list.
def ReadTCSPCTimeTags(FileName):
    # Setting up data reading
    Variables = 12; HeaderLength = 8; PayloadLength = 1056; ReadIndex = 0
    # Preallocating data arrays
    FullData = [[] for i in range(Variables)]; Error = False;
    # Reading file
    with open(FileName , 'rb') as file:
        # Initializing file
        file_length=len(file.read())
        file.seek(0)
        # Looping over the availible bytes
        while ReadIndex+HeaderLength < file_length and not(Error):
            # Reading data
            Header  = file.read(HeaderLength)
            Payload = file.read(PayloadLength)
            file.seek(2,1)
            # Parsing Header Data
            FullData[0].append(struct.unpack('>d',Header[0:8])[0])
            # Parsing payload data
            Data,Error = ReadTimeTagPayload(Payload)
            for Index in range(len(Data)):
                FullData[Index+1].append(Data[Index])
            # Updating reading index
            ReadIndex += (HeaderLength + PayloadLength + 2)
    # Returning data
    if Error:
        return([[] for i in range(Variables)])
    else:
        return(FullData)


def ReadTestFile(FileName):
    print('Checking: ' + FileName)
    # Reading file 
    FullData = ReadTCSPCTimeTags(FileName)
    # Unpacking packet counter for initial check of data flow
    Packets = np.array(list(itertools.chain(*FullData[6])))
    # Finding where the packet counter does not monotonically increase
    A = np.where(np.diff(Packets) < 0)    
    # Total number of packets divided by the difference from the first to the 
    # last packet. Note that the 
    PStart  = Packets[0]; PEnd = Packets[-1]; PEndMono = Packets[-1] + 65536*(len(A[0]))
    RecordedFraction = (len(Packets)-1)/(PEndMono - PStart) 
    Missing = (PEndMono - PStart) - (len(Packets)-1)
    if RecordedFraction<1:
        print('------File With Dropped Packets------')
        print([(len(Packets)-1),(PEndMono - PStart), Missing])
        print('-------------------------------------')
    # Return loaded information
    return(PStart,PEnd,PEndMono,Missing,RecordedFraction)


if __name__ == '__main__':
    # Determinging the names of all the possible files
    FileList = glob.glob('E:\\TCSPC\\20210819\\' + 'TCSPC_*.bin')
    FileList.sort()
    # Running the file reader for all files 
    Start,End,EndMono,Missing,Frac = zip(*[ReadTestFile(FileList[F]) for F in range(0,len(FileList))])


#    # Saving data as a list of numpy arrays    
#    FinalData = [np.array(Data[Index][:]) for Index in range(len(Data)-1)]

    # Determinging
    FileTimes, PPS = TTInfo.PacketWriteSpeed(FileList)
    #  Plotting loading stats
    TTInfo.PlotLoadStats(FileList, Missing, PPS)
    # Outputting the percent of packets received
    print(sum(Missing))
    print(sum((np.array(EndMono)-np.array(Start))))
    print((sum((np.array(EndMono)-np.array(Start)))-sum(Missing))/sum((np.array(EndMono)-np.array(Start)))*100)
    