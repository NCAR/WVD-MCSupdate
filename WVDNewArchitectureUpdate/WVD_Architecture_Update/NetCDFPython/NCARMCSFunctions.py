# Written By: Robert Stillwell
# Written For: National Center for Atmospheric Research
# The following functions are used to open and read the binary files the 
# labview code writes for the MicroPulse DIAL. Some data checks are run and if
# there is a recognized error, a string describing it will be returned; if no
# error is recognized, then data arrays containing all of the file information 
# are returned. 

import math, os, struct, DefineFileElements as Define

#%%
def ParseMCSCountsHeader(Header,ChannelAssign):
    # Bytes 0 - 7 -> Timestamp
    Timestamp = struct.unpack('>d',Header[0:8])[0]
    # Bytes 8-10 -> null, Byte 11 -> Start of Text, Byte 12 -> CR, Byte 13 -> 
    # LF, Bytes 14-16 -> null, and Byte 17 -> "0", Bytes 18-27 -> "OnlineH2O " 
    OnlineH2OCh = ord(Header[29:30])-48 
    if ord(Header[28:29]) == 49: # a two digit channel assignment so add 10 
        OnlineH2OCh = OnlineH2OCh + 10  
    # Bytes 30-40 -> "OfflineH2O "
    OfflineH2OCh = ord(Header[42:43])-48
    if ord(Header[41:42]) == 49: 
        OfflineH2OCh = OfflineH2OCh + 10 
    # Bytes 43-55 -> "CombinedHSRL "
    CombinedHSRLCh = ord(Header[57:58])-48
    if ord(Header[56:57]) == 49: 
        CombinedHSRLCh = CombinedHSRLCh + 10  
    # Bytes 58-71 -> "MolecularHSRL "
    MolecularHSRLCh = ord(Header[73:74])-48
    if ord(Header[72:73]) == 49: 
        MolecularHSRLCh = MolecularHSRLCh + 10  
    # Bytes 74-82 -> "OnlineO2 "
    OnlineO2Ch = ord(Header[84:85])-48
    if ord(Header[83:84]) == 49: 
        OnlineO2Ch = OnlineO2Ch + 10 
    # Bytes 85-94 -> "OfflineO2 "
    OfflineO2Ch = ord(Header[96:97])-48
    if ord(Header[95:96]) == 49: 
        OfflineO2Ch = OfflineO2Ch + 10
    # Bytes 97-99 -> null, Byte 100 -> Start of text, Byte 101 -> CR, Byte  
    # 102 -> LF, Bytes 103-104 -> null, Bytes 105-106 -> ??????????
    # Bytes 107-110 -> Histogram Data Frame Header Word 
    # Checking that the header word is there and equal to 0x4D430000
    if ''.join('{:08b}'.format(ord(Header[i:i+1])) for i in range(107,111)) != \
       ''.join('{:08b}'.format(ord(x))             for x in '\x00\x00\x43\x4D'):
        print(''.join('{:08b}'.format(ord(Header[i:i+1])) for i in range(107,111)))
        print(''.join('{:08b}'.format(ord(x))             for x in '\x00\x00\x43\x4D'))
        ErrorResponse = 'The MCS data frame header word does not match the expected value. ~RS'
        print(ErrorResponse)
        return ([],[],[],[],[],[],[],[],[],ErrorResponse)
    # Bytes 111-112 -> Profiles per histogram
    ProfPerHist = ord(Header[112:113])*2**8 + ord(Header[111:112])
    # Bytes 113 -> null (from Josh)
    # Bytes 114 -> Sync and Channel
    Sync     = ord(Header[114:115])%16
    Channel  = (ord(Header[114:115])-Sync)/16
    # Bytes 115-116 -> Counts per bin * 5ns per count
    NsPerBin = (ord(Header[116:117])*2**8 + ord(Header[115:116]))*5
    # Bytes 117-118 -> Number of bins
    NBins    = ord(Header[118:119])*2**8 + ord(Header[117:118])
    # Bytes 119-121 - Relative time counter
    RTime    = ord(Header[121:122])*2**16 + ord(Header[120:121])*2**8 + ord(Header[119:120])
    # Bytes 122 -> Frame counter
    FCount   = ord(Header[122:123])
    # Bytes 123-126 = null
    # Saving 
    ChannelAssign[OnlineH2OCh] = str("WVOnline")
    ChannelAssign[OfflineH2OCh] = str("WVOffline")
    ChannelAssign[CombinedHSRLCh] = str("HSRLCombined")
    ChannelAssign[MolecularHSRLCh] = str("HSRLMolecular")
    ChannelAssign[OnlineO2Ch] = str("O2Online")
    ChannelAssign[OfflineO2Ch] = str("O2Offline")
    return(Channel,FCount,NBins,NsPerBin,ProfPerHist,RTime,Sync,Timestamp,ChannelAssign,'')

def ParseMCSCountsHeaderV2(Header,ChannelAssign):
    # Reading the data time stamp
    Timestamp = struct.unpack('>d',Header[0:8])[0]
    # Reading the number of channels and the MPD Number
#            MPDNum    = ord(Header[8:9])
    ChannelMap = Define.MCSPhotonCountMapV2(ord(Header[9:10]))
    # Checking that the header word is there and equal to 0x4D430000
    if ''.join('{:08b}'.format(ord(Header[i:i+1])) for i in range(10,14)) != \
       ''.join('{:08b}'.format(ord(x))             for x in '\x00\x00\x43\x4D'):
        ErrorResponse = 'The MCS data frame header word does not match the expected value. ~RS'
        print(ErrorResponse)
        return ([],[],[],[],[],[],[],[],[],ErrorResponse)
    # Bytes 14-15 -> Profiles per histogram
    ProfPerHist = ord(Header[15:16])*2**8 + ord(Header[14:15])
    # Byte 17 -> Sync and Channel
    Sync     = ord(Header[17:18])%16
    Channel  = (ord(Header[17:18])-Sync)//16
    # Bytes 18-19 -> Counts per bin * 5ns per count
    NsPerBin = (ord(Header[19:20])*2**8 + ord(Header[18:19]))*5
    # Bytes 20-21 -> Number of bins
    NBins    = ord(Header[21:22])*2**8 + ord(Header[20:21])
    # Bytes 22-24 - Relative time counter
    RTime    = ord(Header[24:25])*2**16 + ord(Header[23:24])*2**8 + ord(Header[22:23])
    # Bytes 25 -> Frame counter
    FCount   = ord(Header[25:26])
    # 
    ChannelAssign[Channel] = ChannelMap
    return(Channel,FCount,NBins,NsPerBin,ProfPerHist,RTime,Sync,Timestamp,ChannelAssign,'')

#%%
def ReadMCSCounts(Bins,File,ReadIndex,ExpectedChannel):
    # Reading the data from the MCS
    DataArray = []
    for v in range(0, Bins):
        data = File.read(4)
        ReadIndex = ReadIndex+4          
        if ord(data[3:4])/16 != ExpectedChannel:
            # Warning that header & data body don't have same channel number
            ReadError = 'The MCS count channel and header channel do not match. ~RS'
            print(ReadError)
            return([],[],ReadError)
        # Reading photon counting data
        DataArray.append(ord(data[2:3])*2**16 + ord(data[1:2])*2**8 + ord(data[0:1]))
    return (DataArray,ReadIndex,'')

#%%
def ReadMCSPhotonCountFile(MCSFile, Channels=12, headerBytes=127):
    # Constants
    ReadIndex = 0
    # Pre-allocating data arrays 
    Timestamp = []; ProfPerHist = []; Channel = []; DataArray = []; Sync = []
    CntsPerBin = []; NBins = []; RTime = []; FrameCtr = []; ChannelAssign = []
    # Pre-allocating Channel asignment array
    for i in range(Channels): ChannelAssign.append("Unassigned")
    # Opening the file and reading its data contents
    with open(MCSFile , 'rb') as file:
        file_length=len(file.read())
        file.seek(0)
        # Looping over the availible bytes
        while ReadIndex+headerBytes < file_length:
            # Reading and saving header information and photon counting information  
            (Ch,FC,Bins,NPB,PPH,TRel,sync,TStamp,ChannelAssign,HeaderError) = ParseMCSCountsHeader(file.read(headerBytes),ChannelAssign)
            ReadIndex = ReadIndex+headerBytes
            if HeaderError == '':
                (DataReturn,ReadIndex,ReadError) = ReadMCSCounts(Bins,file,ReadIndex,Ch)
                if ReadError == '':
                    Channel.append(Ch); del Ch
                    CntsPerBin.append(NPB); del NPB
                    DataArray.append(DataReturn); del DataReturn
                    FrameCtr.append(FC); del FC
                    NBins.append(Bins); del Bins
                    ProfPerHist.append(PPH); del PPH
                    RTime.append(TRel); del TRel
                    Sync.append(sync); del sync
                    Timestamp.append(TStamp); del TStamp 
                    # Confirming footer word was where it is expected and that it is what 
                    # it is expected to be (0xFFFFFFFF)
                    Footer = file.read(4)
                    if ''.join('{:08b}'.format(ord(Footer[i:i+1])) for i in range(0,4)) != \
                       ''.join('{:08b}'.format(ord(x))           for x in '\xff\xff\xff\xff'):
                        #Write warning that footer is not equal to what it should be
                        FooterError = 'The MCS data frame footer word does not match the expected value. ~RS'
                        print(FooterError)
                        return([],[],[],[],[],[],[],[],[],[],FooterError)
                else:
                    return([],[],[],[],[],[],[],[],[],[],ReadError)
                # Seeking forward 8 bytes from current location (throwing away 
                # extra bits on end of data frame so next is alligned)
                file.seek(8,1)
                ReadIndex = ReadIndex+12
            else:
                return([],HeaderError)
    # If there are no observed errors, return the data as a tuple
    return(Channel, ChannelAssign, CntsPerBin, DataArray, FrameCtr, NBins, ProfPerHist, RTime, Sync, Timestamp, '')

def ReadMCSPhotonCountFileV2(MCSFile, Channels=12, headerBytes=30):
    # Constants
    ReadIndex = 0
    # Pre-allocating data arrays 
    Timestamp = []; ProfPerHist = []; Channel = []; DataArray = []; Sync = []
    CntsPerBin = []; NBins = []; RTime = []; FrameCtr = []; ChannelAssign = []
    # Pre-allocating Channel asignment array
    for i in range(Channels):
        ChannelAssign.append("Unassigned")
    del i
    # Opening the file and reading its data contents
    with open(MCSFile , 'rb') as file:
        file_length=len(file.read())
        file.seek(0)
        # Looping over the availible bytes
        while ReadIndex+headerBytes < file_length:
            # Reading and saving header information and photon counting information  
            (Ch,FC,Bins,NPB,PPH,TRel,sync,TStamp,ChannelAssign,HeaderError) = ParseMCSCountsHeaderV2(file.read(headerBytes),ChannelAssign)
            ReadIndex+=headerBytes
            if HeaderError == '':
                (DataReturn,ReadIndex,ReadError) = ReadMCSCounts(Bins,file,ReadIndex,Ch)
                if ReadError == '':
                    Channel.append(Ch); del Ch
                    CntsPerBin.append(NPB); del NPB
                    DataArray.append(DataReturn); del DataReturn
                    FrameCtr.append(FC); del FC
                    NBins.append(Bins); del Bins
                    ProfPerHist.append(PPH); del PPH
                    RTime.append(TRel); del TRel
                    Sync.append(sync); del sync
                    Timestamp.append(TStamp); del TStamp  
                    # Confirming footer word was where it is expected and that it is what 
                    # it is expected to be (0xFFFFFFFF)
                    Footer = file.read(4)
                    if ''.join('{:08b}'.format(ord(Footer[i:i+1])) for i in range(0,4)) != \
                       ''.join('{:08b}'.format(ord(x))           for x in '\xff\xff\xff\xff'):
                        #Write warning that footer is not equal to what it should be
                        FooterError = 'The MCS data frame footer word does not match the expected value. ~RS'
                        print(FooterError)
                        return([],[],[],[],[],[],[],[],[],[],FooterError)
                    ReadIndex += 4
                    # Checking that the data chunk ends with a carriage return and line feed
                    if (ord(file.read(1)) != 13) or (ord(file.read(1)) != 10):
                        FootError = 'The data write footer word does not match the expected value. ~RS'
                        print(FootError)
                        return([],[],[],[],[],[],FootError)
                    ReadIndex += 2
                else:
                    return([],[],[],[],[],[],[],[],[],[],ReadError)
            else:
                return([],HeaderError)
    # If there are no observed errors, return the data as a tuple
    return(Channel, ChannelAssign, CntsPerBin, DataArray, FrameCtr, NBins, ProfPerHist, RTime, Sync, Timestamp, '')

#%%
def ReadMCSPowerFile(Powerfile, Channels=12):
    # Processing constants
    MeasurementBytes = 146 # this is the number of bytes per power measurement
    StartByte        = 78  # this is the location of the first byte in the 
                           # power monitoring data frame (see Josh's document
                           # for details about this data frame)               
    ChannelAssign = []
    for index in range(Channels): ChannelAssign.append("Unassigned")
    # Pre-allocating data arrays
    AccumExp  = []; Demux = []; PowerCh = []; RTime = [];Timestamp = [];
    HSRLPowCh = []; OnlineH2OCh = []; OfflineH2OCh = []; OnlineO2Ch = []; OfflineO2Ch = [];
    # Opening the file as a binary file and looping over availible data bytes
    with open(Powerfile, "rb") as file:
        file.seek(0)  # Go to beginning of the file
        for k in range(int(os.path.getsize(Powerfile)/MeasurementBytes)):
            # Reading next chunk of data
            Data = file.read(MeasurementBytes)
            # Reading the data time stamp
            Timestamp.append(struct.unpack('>d',Data[0:8])[0])
            # For reference the next several bytes are: 8-10 (null), 11 (Start of Text),
            # 12 (Carrage Return), 13 (Line feed), 14-16 (null), 17 (2)
            # Reading the channel numbers
            # For reference now...Bytes 18-22 are the word "HSRL "
            HSRLPowCh.append(ord(Data[23:24])-48)
            # For reference now...Bytes 24-33 are the word "OnlineH2O "
            OnlineH2OCh.append(ord(Data[34:35])-48) 
            # For reference now...Bytes 35-45 are the word "OfflineH2O "
            OfflineH2OCh.append(ord(Data[46:47])-48)
            # For reference now...Bytes 47-55 are the word "OnlineO2 "
            OnlineO2Ch.append(ord(Data[56:57])-48)
            # For reference now...Bytes 57-66 are the word "OfflineO2 "
            OfflineO2Ch.append(ord(Data[67:68])-48)
            # Temp variable to match the current output
            ChannelAssign[ord(Data[23:24])-48] = str("HSRL")
            ChannelAssign[ord(Data[34:35])-48] = str("OnlineH2O")
            ChannelAssign[ord(Data[46:47])-48] = str("OfflineH2O")
            ChannelAssign[ord(Data[56:57])-48] = str("OnlineO2")
            ChannelAssign[ord(Data[67:68])-48] = str("OfflineO2")
            # For reference the next several bytes are: 68-70 (null), 71 (Start of Text),
            # 72 (Carrage Return), 73 (Line feed), 74-76 (null), 77 (<)
            # Checking that the header word is there and equal to 0x4D430000
            if ''.join('{:08b}'.format(ord(Data[i:i+1])) for i in range(StartByte,StartByte+4)) != \
               ''.join('{:08b}'.format(ord(x))           for x in '\x00\x00\x50\x4D'):
                   HeaderError = 'The MCS power frame header word does not match the expected value. ~RS'
                   print(HeaderError)
                   return([],[],[],[],[],[],HeaderError)
            # Pulling out the relative time counter
            RTime.append(ord(Data[StartByte+4:StartByte+5])+
                         ord(Data[StartByte+5:StartByte+6])*2**8+ 
                         ord(Data[StartByte+6:StartByte+7])*2**16)
            # byte (StartByte + 7) is empty
            # Looping over all the channels to pull out channel specific data
            for m in range(Channels):
                # Pre-allocating the power channel list, accumulation exponent
                # list and the demux select list
                if k==0:PowerCh.append([]);AccumExp.append([]);Demux.append([])
                # Pulling power channel data out of the file
                PowerCh[m].append(ord(Data[4*m+StartByte+8:4*m+StartByte+9]) + 
                                  ord(Data[4*m+StartByte+9:4*m+StartByte+10])*2**8 + 
                                  ord(Data[4*m+StartByte+10:4*m+StartByte+11])*2**16)
                # Pulling the accumulation exponent out of the file
                AccumExp[m].append(ord(Data[4*m+StartByte+11:4*m+StartByte+12])%2**4)
                # Pulling the demux selection out of the file
                Demux[m].append(ord(Data[4*m+StartByte+11:4*m+StartByte+12])//2**4)
            # Checking that the footer word is there and equal to 0xFFFFFFFF
            # For reference bytes 134-137 should be the footer word
            if ''.join('{:08b}'.format(ord(Data[4*m+StartByte+12+i:4*m+StartByte+13+i])) for i in range(0,4)) != \
               ''.join('{:08b}'.format(ord(x))                        for x in '\xFF\xFF\xFF\xFF'):
                   FooterError = 'The MCS power frame footer word does not match the expected value. ~RS'
                   print(FooterError)
                   return([],[],[],[],[],[],FooterError)
            # For reference the end of each measurement is as follows:
            # Bytes 138-140 (null), 141 (End of transmission), 142 (Carriage 
            # return), 143 (Line Feed), 144 (Carriage return), 145 (Line Feed)
    # Return the data arrays read from the file
#    return(AccumExp,Demux,PowerCh,RTime,Timestamp,ChannelAssign,'')
    return(Timestamp,PowerCh,AccumExp,Demux,RTime,ChannelAssign,'')

def ReadMCSPowerFileV2(Powerfile):            
    # Variables for running the loop
    ReadIndex = 0; FirstTime = True; Count = 0
    # Pre-allocating data arrays
    AccumExp  = []; Demux = []; Power = []; RTime = [];Timestamp = [];
    # Opening the file as a binary file and looping over availible data bytes
    with open(Powerfile, "rb") as file:
        file_length=len(file.read())
        file.seek(0) # Go to beginning of the file
        while ReadIndex < file_length:
#            # Getting rid of the start of text bytes from labview
#            file.seek(4,1); ReadIndex += 4                
            # Reading next chunk of data
            Data = file.read(10); ReadIndex += 10;             
            # Reading the data time stamp
            Timestamp.append(struct.unpack('>d',Data[0:8])[0])
            # Reading the number of channels and the MPD Number
#            MPDNum    = ord(Data[8:9])
            NChannels = ord(Data[9:10])
            # Reading the channel map
            ChannelMap = []  
            for m in range(NChannels): 
                ChannelMap.append(Define.MCSPowerMapV2(ord(file.read(1))))
            ReadIndex += NChannels
            # Checking that the header word is there and equal to 0x4D430000
            if ''.join('{:08b}'.format(ord(file.read(1))) for i in range(0,4)) != \
               ''.join('{:08b}'.format(ord(x))            for x in '\x00\x00\x50\x4D'):  
                   HeaderError = 'The MCS power frame header word does not match the expected value. ~RS'
                   print(HeaderError)
                   return([],[],[],[],[],[],HeaderError)
            ReadIndex += 4
            # Reading the relative time counter
            Data = file.read(4); ReadIndex += 4;
            RTime.append(ord(Data[0:1])+ord(Data[1:2])*2**8+ord(Data[2:3])*2**16)
            # Reading the power information
            for m in range(NChannels):
                # Reading data from the file
                Data = file.read(4); ReadIndex += 4;
                # Pre-allocating 2d-power list, accumulation exponent list, and demux list
                if FirstTime:Power.append([]);AccumExp.append([]);Demux.append([])
                # Pulling power channel data out of the file
                Power[m].append(ord(Data[0:1])+ord(Data[1:2])*2**8+ord(Data[2:3])*2**16)
                # Pulling the accumulation exponent out of the file
                AccumExp[m].append(ord(Data[3:4])%2**4)
                # Pulling the demux selection out of the file
                Demux[m].append(ord(Data[3:4])//2**4)
            # Checking that the footer word is there and equal to 0xFFFFFFFF
            if ''.join('{:08b}'.format(ord(file.read(1))) for i in range(0,4)) != \
               ''.join('{:08b}'.format(ord(x))            for x in '\xFF\xFF\xFF\xFF'):  
                   FooterError = 'The MCS power frame footer word does not match the expected value. ~RS'
                   print(FooterError)
                   return([],[],[],[],[],[],FooterError)
            ReadIndex += 4
            # Checking that the data chunk ends with a carriage return and line feed
            if (ord(file.read(1)) != 13) or (ord(file.read(1)) != 10):
                FootError = 'The data write footer word does not match the expected value. ~RS'
                print(FootError)
                return([],[],[],[],[],[],FootError)
            ReadIndex += 2
            # Updating the counter describing the number of power measurements
            FirstTime = False
            Count += 1
    # Return the data arrays read from the file
#    return(AccumExp,Demux,Power,RTime,Timestamp,ChannelMap,'')
    return(Timestamp,Power,AccumExp,Demux,RTime,ChannelMap,'')
    
    
    
    
#%%
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
