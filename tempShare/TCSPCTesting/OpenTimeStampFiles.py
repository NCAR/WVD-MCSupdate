
import struct

# This function is used to convert a 4 byte word into a 32 bit number. The word
# contained in the sub-list D.
def Read4ByteWord(D):
    return(ord(D[3:4])*2**24+ord(D[2:3])*2**16+ord(D[1:2])*2**8+ord(D[0:1]))
# This function creates a string of bits. The words are contained in an array D
# with the start and end indices of the desired string of the array given. 
def CreateString(D,Start,End):
    return(''.join('{:08b}'.format(ord(D[i:i+1])) for i in range(Start,End)))
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
    # Unpack the Pulse Data Frame Payload (should be exactly 8 bytes)
    TDiff      = ord(D[1:2])*2**8+ord(D[0:1])
    Channel    = ord(D[2:3])
    StatusChan = ord(D[3:4])%16
    Sync       = ((ord(D[3:4])-StatusChan)//16-2)//4   
    SyncCnt    = ord(D[5:6])*2**8+ord(D[4:5])
    RTime      = ord(D[6:7])
    StatusSync = ord(D[7:8])%16
    # Sync2       = ((ord(D[7:8])-StatusSync)//16-2)//4   # Seems redundant???
    return(TDiff,Channel,StatusChan,Sync,SyncCnt,RTime,StatusSync)
# This function uses the pre-defined TCSPC bulk data frame structure and parses
# known elements from it. It returns a list of data contained within a single 
# data packet. 
def ReadTimeTagPayload(Payload):
    Error = [CheckHeaderFooter(Payload,0,4,'\x00\x00\x46\x54'), \
             CheckHeaderFooter(Payload,4,8,'\xff\xff\xff\xff')]
    # Pre-allocating data list
    Data = []
    # Word03: relTime, Word04: chPulseCnt, Word05: syncPulseCnt, Word06: statusPulseFrame
    for Bytes in range(3,7):
        Data.append(Read4ByteWord(Payload[(4*Bytes):(4*(Bytes+1))]))         
    # Payload size from Word02
    Data.append(ord(Payload[9:10])*2**8 + ord(Payload[8:9]))
    # Packet Counter from Word02
    Data.append(ord(Payload[11:12])*2**8 + ord(Payload[10:11]))
    # Unpacking time stamps and the meta-data therewith
    for Index in range(0,128):
        A = list(UnpackPulseFrame(Payload[32+(Index*8):32+((Index+1)*8)]))
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
    Variables =15; HeaderLength = 9; PayloadLength = 1056; ReadIndex = 0
    # Preallocating data arrays
    FullData = [[] for i in range(9)]; Error = False;
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
            FullData[1].append(ord(Header[8:9]))
            # Parsing payload data
            Data,Error = ReadTimeTagPayload(Payload)
            for Index in range(len(Data)):
                FullData[Index+2].append(Data[Index])
            # Updating reading index
            ReadIndex += (HeaderLength + PayloadLength + 2)
    # Returning data
    if Error:
        return([[] for i in range(Variables)])
    else:
        return(FullData)


if __name__ == '__main__':
    print('No files yet known for testing. ~RS')
#    FileName = ''
#    Data = ReadTCSPCTimeTags(FileName)
