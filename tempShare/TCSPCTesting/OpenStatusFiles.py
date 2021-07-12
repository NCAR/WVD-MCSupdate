
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
# This function uses the pre-defined TCSPC status frame structure and parses 
# known elements from it. It retuns a list of data contained within a single 
# frame of data.
def ReadStatusPayload(Payload):
    # Checking that the header/footer are correct and in the right place
    Error = [CheckHeaderFooter(Payload,0,4,'\x00\x00\x48\x54'), \
              CheckHeaderFooter(Payload,36,40,'\xff\xff\xff\xff')]               
    # Unpacking payload of the MCS TCSPC payload
    Data = []
    for Bytes in range(1,5):
        Data.append(CreateString(Payload, 4*Bytes, 4*(Bytes+1)))
    for Bytes in range(5,8):
        Data.append(Read4ByteWord(Payload[(4*Bytes):(4*(Bytes+1))]))  
    # If there are no observed errors, return the data as a tuple    
    if any(Error):
        return([],True)
    else:
        return(Data, False)               
# This function is used to read a full TCSPC Heartbeat file. It loops over the 
# contents of the file and parses it. Assuming all data is written correctly, 
# it returns a list of data. If the check values are not recognized, it returns
# and empty list.
def ReadTCSPCHeartBeat(FileName):
    # Setting up data reading
    Variables = 9; HeaderLength = 9; PayloadLength = 40; ReadIndex = 0
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
            Data,Error = ReadStatusPayload(Payload)
            for Index in range(0,len(Data)):
                FullData[Index+2].append(Data[Index])
            # Updating reading index
            ReadIndex += (HeaderLength + PayloadLength + 2)
    # Returning data
    if Error:
        return([[] for i in range(Variables)])
    else:
        return(FullData)


if __name__ == '__main__':
    FileName = 'TCSPCHeartbeat_01_20210707_230000.bin'
    Data = ReadTCSPCHeartBeat(FileName)