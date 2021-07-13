
import struct, math, itertools, glob
import numpy as np

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
    BitString = CreateRString(D,4,0)[::-1]
    # Defining the types of time stamps possible
    BitStringTypes = {'00':0,'01':1,'10':2,'11':3}
    # Unpacking payload information
    Sync   = int(BitString[30:32][::-1],2)
    Type   = BitStringTypes[BitString[28:30][::-1]]
    Status = int(BitString[24:28][::-1])
    TDiff  = int(BitString[0:16][::-1],2)
    if Type == 2:
        Channel_RTime = int(math.log2(int(BitString[16:24][::-1],2)))
    elif Type == 1:
        Channel_RTime = int(BitString[16:24][::-1],2)
    else:
        Channel_RTime = -1
        
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
    # Unpacking time stamps and the meta-data therewith
    for Index in range(0,int(PayloadSize/4)):
        A = list(UnpackPulseFrame(Payload[32+(Index*4):32+((Index+1)*4)]))
        for SubIndex in range(0,len(A)):
            Data[SubIndex+6].append(A[SubIndex])
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
    # Reading file 
    FullData = ReadTCSPCTimeTags(FileName)
    # Unpacking packet counter for initial check of data flow
    TimeStamp = np.array(FullData[0])
    TimeStamp = (TimeStamp - TimeStamp[0])*60*60
    Packets   = np.array(list(itertools.chain(*FullData[6])))
    PStart = Packets[0]
    PEnd   = Packets[-1]
    # Making packet counter monotonically increase
    A = np.where(np.diff(Packets) < 0)
    for index in range(0,len(A[0])):
        Packets[A[0][index]+1:] = Packets[A[0][index]+1:] + 65536
    # Last number minus first number divided by the number of entries
    RecordedFraction = (len(Packets)-1)/(Packets[-1] - Packets[0])
    if RecordedFraction<1:
        print(FileName)
        print([(len(Packets)-1),(Packets[-1] - Packets[0])])
    # Return loaded information
    return(PStart,PEnd,RecordedFraction,Packets[0],Packets[-1],FullData)


if __name__ == '__main__':
    Counter = 0
    Start   = []; End = []; Frac = []; Total = []
    for file in glob.glob("*.bin"):
        # Reading data file and storing data as lists
        S, E, F, T1, T2, Data = ReadTestFile(file)
        Start.append(S)
        End.append(E)
        Frac.append(F)
        Total.append(T2-T1)
        # Removing temporary data
        del S, E, F, T1, T2
        # Checking if user requests early exit
        if Counter >= 0:
            break
        Counter += 1

    del Counter, file    
      
    print(Frac)
    print(np.array(Start[1:])-np.array(End[0:-1]))
    print(sum(np.array(Total)))
    
    V00_PacketTimeStamps = np.array(Data[0][:])  # Header: Size ->(# of packets x 1)
    V01_RTimeStamps      = np.array(Data[1][:])  # Header: Size ->(# of packets x 1)
    V02_chPulseCounter   = np.array(Data[2][:])  # Header: Size ->(# of packets x 1)
    V03_syncPulseCounter = np.array(Data[3][:])  # Header: Size ->(# of packets x 1)
    V04_PacketStatus     = np.array(Data[4][:])  # Header: Size ->(# of packets x 1)
    V05_PayloadSize      = np.array(Data[5][:])  # Header: Size ->(# of packets x 1)
    V06_PacketCounter    = np.array(Data[6][:])  # Header: Size ->(# of packets x 1) 
    V07_Type             = np.array(Data[7][:])  # Body:   Size ->(# of packets x 256)
    V08_SyncNum          = np.array(Data[8][:])  # Body:   Size ->(# of packets x 256)
    V09_ChannelNum_RTime = np.array(Data[9][:])  # Body:   Size ->(# of packets x 256)
    V10_TimeTag          = np.array(Data[10][:]) # Body:   Size ->(# of packets x 256)
    V11_Status           = np.array(Data[11][:])
