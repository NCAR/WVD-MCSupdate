#-------------------------------------------------------------------------------
# Name:        WV-DIAL MCS TEst Script
# Purpose:     Intended to verify the MCS build and all connections
#              Not intended to verify all FW functionality
# Author:      J.Carnes
# FW Version   Beta, ~12/2017
#
# Created:     12/7/2017
# Copyright:   (c) J 2017
#-------------------------------------------------------------------------------

# TEST 1
# - Use test patterns, check all data output channels
# - Basic LAN Connectivity
# - Write/Read Registers via LAN
# - Read Serial Number
# - Verify Histogram and Power Monitor Frames
# - View results over COM terminal
# - Check Relative Time Counter
# - No signal generator stimulus needed

# TEST 2
# - Stimulate DINx with pulse generator to verify inputs
# - Uses SYNC test pattern
# - Requires 1MHz (50%), 0/2V Pulse from generator

# TEST 3
# - Stimulate DEMUXx with pulse generator to verify inputs
# - Uses SYNC and DIN test pattern
# - Requires 1MHz (50%), 0/2V Pulse from generator

# TEST 4
# - Stimulate SYNCx with pulse generator to verify inputs
# - Uses DIN test pattern
# - Requires 6.3kHz (1us), 0/2V Pulse from generator

# TEST 5
# - Stimulate PINx with pulse generator to verify inputs, 3 pnt amplitude test
# - Automatically verifies vth_ref
# - Requires 6.3kHz (1us), Pulse from generator with 3 different pulse amplitudes [0.5,1.0,2.0]V

import socket
import sys
import binascii
import datetime
import time

RUN_TEST1 = True
RUN_TEST2 = False
RUN_TEST3 = False
RUN_TEST4 = False
RUN_TEST5 = False

CLIENT_IP = '192.168.000.199'  # MicroZed
HOST_IP   = '192.168.000.116'  # PC
HOST_IP_INT = int(HOST_IP[0:3])*pow(2,24) + int(HOST_IP[4:7])*pow(2,16) + int(HOST_IP[8:11])*pow(2,8) + int(HOST_IP[12:15])
UDP_PORT = 24599
RX_BUFF_LEN = 131072
READBACK_TIMEOUT = 5         # Time before readbck timeout [seconds]

HIST_FRAME_SIZE = 12024      # histogram, includes header, data, and footer [Bytes], "MC"
HIST_HEADER_SIZE = 5*4       # Histogram Frame header Size [Bytes]
HIST_FOOTER_SIZE = 1*4       # Histogram Frame Footer Size [Bytes]
PMON_FRAME_SIZE  = 15*4      # Power Monitor Frame Total Size [Bytes], "MP"
PMON_HEADER_SIZE = 2*4       # Power Monitor Frame Header Size [Bytes]
PMON_FOOTER_SIZE = 1*4       # Power Monitor Frame Footer Size [Bytes]
BULK_READ_FRAME_SIZE = 23*4  # User Reg Map Bulk Read Frame Size, "MR"
SINGLE_READ_FRAME_SIZE = 3*4 # Single Register Read Frame size
DEBUG_BULK_READ_FRAME_SIZE = 100*4


### --- Read/Write Register Utilities -----------------------------------------------------------------

def writeUserReg(addr, data):
    if (addr > 255) | (data > pow(2,32)-1):   # Do not allow invalid address or data
        return -1
    try:
        sock.sendto("w%s%s"%('{:02x}'.format(addr,'x'), '{:08x}'.format(data,'x')), (CLIENT_IP, UDP_PORT))
    except:
        return -1
    return 0

def readUserReg(addr):
    regValue = None
    try:
        sock.sendto("s%s00000000"%('{:02x}'.format(addr,'x')), (CLIENT_IP, UDP_PORT))
        while True:
            data, address = sock.recvfrom(RX_BUFF_LEN)

            packet_len = len(data)
            if (packet_len == SINGLE_READ_FRAME_SIZE) & (getPacketType(data[0:4]) == PACKET_ONERD):  # Check for a single read packet
                regValue = int(binascii.hexlify(data[1*4+3:1*4-1:-1]),16)
                break

    except:
        return (-1,None)
    return (0,regValue)

def readBulkUserRegMap(addr):
    pass

def readBulkDebugRegMap(addr):
    pass

def updateDestinationIp(ip_addr):
    writeUserReg(0x40, ip_addr)


### --- Configuration Related Stuff -----------------------------------------------------------------

def readSerialNumber():
    return readUserReg(0x11)

def resetHarvester():
    reg_01 = 0x00010FFF  # Reset Harvester and Channels
    reg_01_c = 0x00000000  # Clear Reset

    reg_addr_set = [0x01, 0x01]
    reg_data_set = [reg_01, reg_01_c]
    for i in range(0,len(reg_addr_set)):
        writeUserReg(reg_addr_set[i], reg_data_set[i])
    return 0

def disableData():
    reg_00 = 0x00000000  # Turn off all CH
    reg_01 = 0x00010FFF  # Reset Harvester and Channels
    reg_09 = 0x00000000  # Turn off all PMON
    reg_addr_set = [0x00, 0x01, 0x09]
    reg_data_set = [reg_00, reg_01, reg_09]
    for i in range(0,len(reg_set)):
        writeUserReg(reg_addr_set[i], reg_data_set[i])
    return 0

def resetConfig():
    updateDestinationIp(HOST_IP_INT)

    reg_00 = 0x00000000
    reg_01 = 0x00000000
    reg_02 = 0x0000000A  # cntsPerBin = 10
    reg_03 = 0x00000200  # numBins = 512
    reg_04 = 0x00000400  # profPerHist = 1024
    reg_05 = 0x00000000
    reg_06 = 0x00000000  # Normal Mode, no test modes
    reg_07 = 0x01312D00  # rTimeStep = 100ms
    reg_08 = 0x00000000
    reg_09 = 0x00000000
    reg_0A = 0x00000000
    reg_0B = 0x00000000
    reg_0C = 0x00000000
    reg_0D = 0x00000000
    reg_0E = 0x00000000
    reg_0F = 0x00000000
    #reg_10 = 0x00000000 (read only)
    reg_30 = 0x000051E0  # vth_ref = 0.8V
    reg_31 = 0x00006660  # demux_ref = 1.0V
    reg_32 = 0x00006660  # din_ref   = 1.0V
    reg_33 = 0x00006660  # sync_ref  = 1.0V

#    reg_addr_set = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, \
#                    0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, \
#                    0x30, 0x31, 0x32, 0x33]
#    reg_data_set = [reg_00, reg_01, reg_02, reg_03, reg_04, reg_05, reg_06, reg_07, \
#                    reg_08, reg_09, reg_0A, reg_0B, reg_0C, reg_0D, reg_0E, reg_0F, \
#                    reg_30, reg_31, reg_32, reg_33]
    reg_addr_set = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, \
                    0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
    reg_data_set = [reg_00, reg_01, reg_02, reg_03, reg_04, reg_05, reg_06, reg_07, \
                    reg_08, reg_09, reg_0A, reg_0B, reg_0C, reg_0D, reg_0E, reg_0F]
    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1
    return 0


TEST1_RUNTIME = 86000                      # seconds
TEST1_NUMBINS = 3000                       # bins (see config)
TEST1_HIST_FRAME_SIZE = (5 + TEST1_NUMBINS + 1)*4   # Bytes
TEST1_HIST_BINVAL = 512                    # Hits
TEST1_HIST_DATARATE_NOM = 1017             # kB/s: (5+3000+1)*4*8/0.0944
TEST1_HIST_DATARATE_MAXERR = 50            # kB/s
TEST1_PMON_FRAME_SIZE = (2 + 12 + 1)*4     # Bytes
TEST1_PMON_DATARATE_NOM = 600              # B/s
TEST1_PMON_DATARATE_MAXERR = 20            # B/s

def configTest1():
    resetConfig()
    reg_01 = 0x00010FFF  # hold in reset
    reg_02 = 0x0000000A  # cntsPerBin = 10
    reg_03 = 0x00000BB8  # numBins = 3000
    reg_04 = 0x00000200  # profPerHist = 512
    reg_06 = 0x1F090900  # Test Modes: Sync 6.3kHz, DIN Pulse inputs (1 per bin)
    reg_09 = 0x00010FFF  # Test Modes: PMON pulses at 5us width, 82us period
    reg_00 = 0x000100FF  # Enable Sync0, All CHx
    reg_01_2 = 0x00000000  # release reset

    reg_addr_set = [0x01, 0x02, 0x03, 0x04, 0x06, 0x09, 0x00, 0x01]
    reg_data_set = [reg_01, reg_02, reg_03, reg_04, reg_06, reg_09, reg_00, reg_01_2]

    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1

    return 0

TEST2_RUNTIME = 5                         # seconds
TEST2_SIGNAL = '1MHz 50% 0/2V pulse'
TEST2_NUMBINS = 256                       # Bins (see config)
TEST2_HIST_FRAME_SIZE = (5 + TEST2_NUMBINS + 1)*4   # Bytes
TEST2_HIST_BINVALUE = 437                 # 0x1B5, Hits (see config)
TEST2_HIST_BINVALUE_MAXERR = 20           # Hits (see config)

def configTest2():
    resetConfig()
    reg_01 = 0x00010FFF  # hold in reset
    reg_02 = 0x0000000A  # cntsPerBin = 10
    reg_03 = 0x00000100  # numBins = 256
    reg_04 = 0x00002222  # profPerHist = 8738 (0x2222), results in histogram every ~1.4s
    reg_06 = 0x1F000800  # Test Modes: Sync 6.3kHz
    reg_00 = 0x00010000  # Enable Sync0. DIN will be enabled in script
    reg_01_2 = 0x00000000  # release reset
    #Note: Should result in ~437 hits/bin = 1e6*10/200e6*8738

    reg_addr_set = [0x01, 0x02, 0x03, 0x04, 0x06, 0x00, 0x01]
    reg_data_set = [reg_01, reg_02, reg_03, reg_04, reg_06, reg_00, reg_01_2]

    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1
    return 0

TEST3_RUNTIME = 6                         # seconds
TEST3_SIGNAL = '1MHz 50% 0/2V pulse'
TEST3_NUMBINS = 256                       # Bins (see config)
TEST3_HIST_FRAME_SIZE = (5 + TEST3_NUMBINS + 1)*4   # Bytes
TEST3_HIST_BINVALUE = 4369                # Hits (see config)
TEST3_HIST_BINVALUE_MAXERR = 100          # Hits (see config)

def configTest3():
    resetConfig()
    reg_01 = 0x00010FFF  # hold in reset
    reg_02 = 0x0000000A  # cntsPerBin = 10
    reg_03 = 0x00000100  # numBins = 256
    reg_04 = 0x00002222  # profPerHist = 8738 (0x2222), results in histogram every ~1.4s
    reg_06 = 0x1F090900  # Test Modes: Sync 6.3kHz, DIN pulse 1/10 cnts
    reg_00 = 0x0F010000  # Enable Sync0, All DEMUX. DIN will be enabled in script
    reg_01_2 = 0x00000000  # release reset
    # Note: Should result in ~8738/2= 4369 (0x1111) in each histogram, though not exact

    reg_addr_set = [0x01, 0x02, 0x03, 0x04, 0x06, 0x00, 0x01]
    reg_data_set = [reg_01, reg_02, reg_03, reg_04, reg_06, reg_00, reg_01_2]

    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1
    return 0

TEST4_RUNTIME = 6                         # seconds
TEST4_SIGNAL = '6.3kHz (1us pulse width) 0/2V pulse'
TEST4_NUMBINS = 256                       # Bins (see config)
TEST4_HIST_FRAME_SIZE = (5 + TEST4_NUMBINS + 1)*4   # Bytes
TEST4_HIST_BINVALUE = 8738                # Hits (see config)
TEST4_HIST_BINVALUE_MAXERR = 0            # Hits (see config)

def configTest4():
    resetConfig()
    reg_01 = 0x00010FFF  # hold in reset
    reg_02 = 0x0000000A  # cntsPerBin = 10
    reg_03 = 0x00000100  # numBins = 256
    reg_04 = 0x00002222  # profPerHist = 8738 (0x2222), results in histogram every ~1.4s
    reg_05 = 0x00000000  # Select SYNC0 for DIN0. WIll be updated in the script
    reg_06 = 0x00090100  # Test Modes: DIN pulses, 1 per 10 cnts
    reg_00 = 0x00070001  # Enable All SYNCx, Only CH0
    reg_01_2 = 0x00000000  # release reset
    # Note: Should result in exactly 8738 (0x2222) in each histogram

    reg_addr_set = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x00, 0x01]
    reg_data_set = [reg_01, reg_02, reg_03, reg_04, reg_05, reg_06, reg_00, reg_01_2]

    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1
    return 0

TEST5_RUNTIME = 5                       # seconds
TEST5_SIGNAL1 = ' 0/1V pulse, 6.3kHz (1us pulse width)'
TEST5_SIGNAL2 = ' 0/0.5V pulse, 6.3kHz (1us pulse width)'
TEST5_SIGNAL3 = ' 0/2V pulse, 6.3kHz (1us pulse width)'
TEST5_PMON_VALUE1 = 256*844             # Hits (see config), 1.0V->850 hits
TEST5_PMON_VALUE2 = 256*130             # Hits (see config), 0.5V->140 hits
TEST5_PMON_VALUE3 = 256*1478            # Hits (see config)  2.0V->1470 hits
TEST5_PMON_VALUE_MAXERR1 = 256*50       # Hits (see config)
TEST5_PMON_VALUE_MAXERR2 = 256*85       # Hits (see config)
TEST5_PMON_VALUE_MAXERR3 = 256*40       # Hits (see config)
# Note: Count errors translate to smaller voltage error at smaller Vo

def configTest5():
    resetConfig()
    reg_09 = 0x00000FFF  # Enable all power monitor channels
    reg_0A = 0x00888888  # Average 2^8 pulses
#    reg_0A = 0x00000000  # Average 2^0=1 pulse

    reg_addr_set = [0x0A, 0x09]
    reg_data_set = [reg_0A, reg_09]

    for i in range(0,len(reg_addr_set)):
        rtn = writeUserReg(reg_addr_set[i], reg_data_set[i])
        if (rtn != 0): return -1
        (rtn,regValue) = readUserReg(reg_addr_set[i])
        if (rtn != 0) | (regValue != reg_data_set[i]): return -1
    return 0


### --- Data Verification Utilities -----------------------------------------------------------------

PACKET_NONE = 0
PACKET_HIST = 1
PACKET_PMON = 2
PACKET_BULKRD = 3
PACKET_ONERD = 4

def getPacketType(data):
    # Determine packet type
    ptype = binascii.hexlify(data[0:4])
    if ( ptype == '0000434d'): # typical histogram packet "MC"
        return PACKET_HIST
    elif (ptype == '0000504d'): # typical power monitor packet "MP"
        return PACKET_PMON
    elif (ptype == '0000524d'): # typical bulk read packet "MR"
        return PACKET_BULKRD
    elif (ptype == '0000534d'): # typical single read packet "MS"
        return PACKET_ONERD
    else:
        return PACKET_NONE      # not a recognized packet

oldFrameCounterValue = '00'
oldChannelValue = '0'
def verifyFrameCounter(data):
    # Verify frame counter order
    global oldFrameCounterValue
    global oldChannelValue

    newChannelValue = int(binascii.hexlify(data[7]),16)/16
    newFrameCounterValue = binascii.hexlify(data[15])
    if ( newFrameCounterValue == '00') & ( oldFrameCounterValue == 'ff'):
        pass
    elif ( int(newFrameCounterValue,16) == int(oldFrameCounterValue,16) + 1 ):
        pass
    else:
        printAndLog('WARNING: Missing frame(s), jumped from 0x%s (ch.%s) to 0x%s (ch.%s), %s' % (oldFrameCounterValue, oldChannelValue, newFrameCounterValue, newChannelValue, datetime.datetime.now()))
        oldFrameCounterValue = newFrameCounterValue[:]
        oldChannelValue = newChannelValue
        return -1

    oldFrameCounterValue = newFrameCounterValue[:]
    oldChannelValue = newChannelValue
    return 0


def verifyHistBinValue(data,binIndex,maxVal,minVal):
    value = int(binascii.hexlify(data[(5+binIndex)*4+2:(5+binIndex)*4-1:-1]),16)
    if (value > maxVal) | (value < minVal):
        printAndLog('ERROR: Bad Bin Value %s at bin %d' % (hex(value),binIndex+1))
        return -1
    return 0

def verifyAllHistBinValues(data,numbins,maxVal,minVal):
    for i in range(0,numbins):
        value = int(binascii.hexlify(data[(5+i)*4+2:(5+i)*4-1:-1]),16)
        if (value > maxVal) | (value < minVal):
            printAndLog('ERROR: Bad Bin Value %s at bin %d' % (hex(value),i+1))
            return -1
        return 0

def verifyPmonValue(data,channel,maxVal,minVal):
    value = int(binascii.hexlify(data[(2+channel)*4+2:(2+channel)*4-1:-1]),16)
    if (value > maxVal) | (value < minVal):
        printAndLog('ERROR: Bad Value %s on channel %d' % (hex(value),channel))
        return -1
    return 0

### --- Log Related Stuff -----------------------------------------------------------------
fid_log = None
fid_result = None
logFileName = None
resultFileName = None

def startNewLog(tagStr):
    global fid_log
    global fid_result
    global logFileName
    global resultFileName

    timenow_raw = datetime.datetime.now()
    timenow_str = timenow_raw.strftime('%Y%m%d%H%M%S')

    logFileName = tagStr+'_'+timenow_str+'_log.txt'
    resultFileName = tagStr+'_'+timenow_str+'_results.txt'
    try:
        fid_log = open(logFileName, 'w')
        fid_result = open(resultFileName, 'w')
    except:
        print('ERROR opening log files')
        return -1

    return 0

def writeToLog(str):
    fid_log.write(str+'\n')
    return 0

def writeToResults(str):
    fid_result.write(str+'\n')
    return 0

def stopLog():
    fid_log.close()
    fid_result.close()
    return 0

def printAndLog(str):
    print(str)
    writeToLog(str)
    return 0

def printAndLogTime():
    nowtime = datetime.datetime.now()
    print(nowtime)
    writeToLog(str(nowtime))
    return 0

def printResultsFile():
    try:
        fid = open(resultFileName, 'r')
        for line in fid:
            print(lines)
    except:
        pass
    return

### --- Socket Related Stuff -----------------------------------------------------------------
sock = None
def openSocket():
    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RX_BUFF_LEN) # Set Rx buffer to accomodate pack of 12 histograms (144kB)
        sock.settimeout(READBACK_TIMEOUT)  # set timeout
        printAndLog('Socket Rx Buffer: %s Bytes' % str(sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)))

        server_address = (HOST_IP, UDP_PORT)
        printAndLog('Starting Socket on %s port %s' % server_address)
        sock.bind(server_address)
        return 0
    except:
        return -1

def closeSocket():
    sock.close()

### --- Test Runs -----------------------------------------------------------------

def runTest1():
    result = 0
    printAndLog("-------- Test 1 --------")
    printAndLogTime()

    printAndLog("Opening Socket ...")
    rtn = openSocket()
    if (rtn != 0):
        writeToResults('[FAIL] Test 1')
        return -1
    printAndLog("Socket Successfully opened")

    printAndLog("Configuring Unit ...")
    rtn = configTest1()
    if (rtn != 0):
        printAndLog("ERROR during configuration")
        writeToResults('[FAIL] Test 1')
        return -1
    printAndLog("Configuration Complete")

    rtn, serialNumDevice = readSerialNumber()
    if (rtn != 0):
        printAndLog("Error reading Serial Number, ABORTED")
        return

    serialNumUsr = int(raw_input("What is expected Serial Number of device?"))
    if (serialNumDevice == serialNumUsr):
        printAndLog("[STATUS] Serial Number Confirmed, %d"%(serialNumDevice))
    else:
        printAndLog("[ERROR] Detected Serial Number %d, Expected Serial Number: %d"%(serialNumDevice,serialNumUsr))

    time0 = datetime.datetime.now()
    accumHistDataSize = 0
    accumPmonDataSize = 0
    ignoreFrameCounter = 1              # Ignore the error on the first frame counter observation
    ignoreFirstPacket = 1

    printAndLog("Starting Data Collection, running for - %d - [s] " % TEST1_RUNTIME)
    while True:
        try:
            data, address = sock.recvfrom(RX_BUFF_LEN)
        except:
            printAndLog("ERROR: No Data Received")
            return -1

        if (ignoreFirstPacket == 1):
            ignoreFirstPacket = 0
            continue

        packet_len = len(data)

        time1 = datetime.datetime.now()
        if (time1 - time0 > datetime.timedelta(0,TEST1_RUNTIME,0)):
            break

        if (getPacketType(data[0:4]) == PACKET_HIST):
            if(packet_len != TEST1_HIST_FRAME_SIZE):                         # Check packet length
                printAndLog("ERROR: Bad HIST Frame Size, %d" % packet_len)
                result = -1

            rtn = verifyFrameCounter(data[0:20])                             # Check frame counter
            if ((rtn != 0) & (ignoreFrameCounter == 1)):                     #  Ignore the error on the first received frame
                printAndLog("Note: Ignoring first observed Frame Counter Value")
                ignoreFrameCounter == 0
            elif ((rtn != 0) & (ignoreFrameCounter == 0)):
                result = -1
            else:
                pass

            for i in [0,TEST1_NUMBINS/2,TEST1_NUMBINS-1]:                                          # Check histogram value at a few different bins, including bounds
                rtn = verifyHistBinValue(data,i,TEST1_HIST_BINVAL,TEST1_HIST_BINVAL)
                if (rtn != 0):
                    result = -1

            accumHistDataSize = accumHistDataSize + packet_len               # Accumulate Data Received [Bytes]

        if (getPacketType(data[0:4]) == PACKET_PMON):
            if(packet_len != TEST1_PMON_FRAME_SIZE):                         # Check packet length
                printAndLog("ERROR: Bad PMON Frame Size, %d" % packet_len)
                result = -1

            accumPmonDataSize = accumPmonDataSize + packet_len               # Accumulate Data Received [Bytes]

    # Disable channels
    reg_00 = 0x00000000
    writeUserReg(0x00, reg_00)
    reg_09 = 0x00000000
    writeUserReg(0x09, reg_09)
    time.sleep(1)

    try:
        data, address = sock.recvfrom(RX_BUFF_LEN)  # Receive (and ignore) any last data from buffer
    except: pass
    printAndLog("Closing Socket ...")
    closeSocket()
    dataRateHist = round(accumHistDataSize/TEST1_RUNTIME/1e3)                # Check Data Rate [kB/s]
    printAndLog("Histogram Data Rate = %d kB/s" % (dataRateHist))
    if (dataRateHist > TEST1_HIST_DATARATE_NOM + TEST1_HIST_DATARATE_MAXERR) | (dataRateHist < TEST1_HIST_DATARATE_NOM - TEST1_HIST_DATARATE_MAXERR):
        printAndLog("ERROR: Bad HIST Data Rate")
        result = -1

    dataRatePmon = round(accumPmonDataSize/TEST1_RUNTIME)                    # Check Data Rate [B/s]
    printAndLog("Power Monitor Data Rate = %d B/s" % (dataRatePmon))
    if (dataRatePmon > TEST1_PMON_DATARATE_NOM + TEST1_PMON_DATARATE_MAXERR) | (dataRatePmon < TEST1_PMON_DATARATE_NOM - TEST1_PMON_DATARATE_MAXERR):
        printAndLog("ERROR: Bad PMON Data Rate")
        result = -1

    printAndLog("-------- Test 1 FINISHED --------")

    if (result != 0):
        writeToResults('[FAIL] Test 1')
    else:
        writeToResults('[SUCCESS] Test 1')

    return 0

def runTest2():
    result = 0
    printAndLog("-------- Test 2 --------")
    printAndLogTime()

    printAndLog("Opening Socket ...")
    rtn = openSocket()
    if (rtn != 0):
        writeToResults('[FAIL] Test 2')
        return -1
    printAndLog("Socket Successfully opened")

    printAndLog("Configuring Unit ...")
    rtn = configTest2()
    if (rtn != 0):
        printAndLog("ERROR during configuration")
        writeToResults('[FAIL] Test 2')
        return -1
    printAndLog("Configuration Complete")

    printAndLog("Closing Socket ...")
    closeSocket()

    for din_index in range(0,8):                                                # Loop over all DINx Inputs
        raw_input("Apply a "+TEST2_SIGNAL+" signal to DIN-%d-, then press ENTER" % (din_index))

        printAndLog("Opening Socket ...")
        rtn = openSocket()
        if (rtn != 0):
            writeToResults('[FAIL] Test 2')
            return -1
        printAndLog("Socket Successfully opened")

        # Enable the appropriate histogram channel
        reg_00 = 0x00010000 + pow(2,din_index)
        writeUserReg(0x00, reg_00)
        resetHarvester()

        time0 = datetime.datetime.now()
        ignoreFirstPacket = 1
        properPacketArrived = 0

        printAndLog("Starting Data Collection, running for - %d - [s] " % TEST2_RUNTIME)
        while True:
            try:
                data, address = sock.recvfrom(RX_BUFF_LEN)
            except:
                printAndLog("ERROR: No Data Received")
                return -1

            time1 = datetime.datetime.now()
            if (time1 - time0 > datetime.timedelta(0,TEST2_RUNTIME,0)):
                break

            if (ignoreFirstPacket == 1):
                ignoreFirstPacket = 0
                continue

            packet_len = len(data)

            if (getPacketType(data[0:4]) == PACKET_HIST):                        # Check a single histogram packet when it arrives
                properPacketArrived = 1
                if(packet_len != TEST2_HIST_FRAME_SIZE):                         # Check packet length
                    printAndLog("ERROR: Bad HIST Frame Size, %d" % packet_len)
                    result = -1
                    break
                rtn = verifyAllHistBinValues(data,TEST2_NUMBINS,TEST2_HIST_BINVALUE+TEST2_HIST_BINVALUE_MAXERR,TEST2_HIST_BINVALUE-TEST2_HIST_BINVALUE_MAXERR)  # Check all histogram bin values
                if (rtn != 0):
                    printAndLog("ERROR: Failed Histogram Bin Value")
                    result = -1
                    break

        # Verify that a proper packet even arrived
        if (properPacketArrived != 1):
            printAndLog("ERROR: Proper Packet was never received")
            result = -1

        # Disable the channel
        reg_00 = 0x00000000
        writeUserReg(0x00, reg_00)
        time.sleep(1)

        #try:  # No need to clear out buffer because data is so slow
        #    data, address = sock.recvfrom(RX_BUFF_LEN)  # Receive (and ignore) any last data from buffer
        #except: pass
        printAndLog("Closing Socket ...")
        closeSocket()
        printAndLog("Finished testing DIN-%d-"%(din_index))



    printAndLog("-------- Test 2 FINISHED --------")

    if (result != 0):
        writeToResults('[FAIL] Test 2')
    else:
        writeToResults('[SUCCESS] Test 2')

    return 0

def runTest3():
    result = 0
    printAndLog("-------- Test 3 --------")
    printAndLogTime()

    printAndLog("Opening Socket ...")
    rtn = openSocket()
    if (rtn != 0):
        writeToResults('[FAIL] Test 3')
        return -1
    printAndLog("Socket Successfully opened")

    printAndLog("Configuring Unit ...")
    rtn = configTest3()
    if (rtn != 0):
        printAndLog("ERROR during configuration")
        return -1
    printAndLog("Configuration Complete")

    printAndLog("Closing Socket ...")
    closeSocket()


    for demux_index in range(0,4):                                                # Loop over all DEMUXx Inputs
        raw_input("Apply a "+TEST3_SIGNAL+" signal to DEMUX-%d-, then press ENTER" % (demux_index))

        printAndLog("Opening Socket ...")
        rtn = openSocket()
        if (rtn != 0):
            writeToResults('[FAIL] Test 3')
            return -1
        printAndLog("Socket Successfully opened")

        time0 = datetime.datetime.now()
        ignoreFirstPacket = 1
        properPacketArrived = 0

        # Enable the appropriate histogram channels (low and high)
        reg_01 = 0x00010FFF
        writeUserReg(0x01, reg_01)
        reg_00 = 0x0F010000 + pow(2,demux_index) + pow(2,demux_index+8)
        writeUserReg(0x00, reg_00)
        resetHarvester()

        printAndLog("Starting Data Collection, running for - %d - [s] " % TEST3_RUNTIME)
        while True:
            try:
                data, address = sock.recvfrom(RX_BUFF_LEN)
            except:
                printAndLog("ERROR: No Data Received")
                writeToResults('[FAIL] Test 3')
                return -1

            if (ignoreFirstPacket == 1):
                ignoreFirstPacket = 0
                continue

            packet_len = len(data)

            if (getPacketType(data[0:4]) == PACKET_HIST):                        # Check histogram packet when it arrives, will look at paired low and high channels
                properPacketArrived = 1
                if(packet_len != TEST3_HIST_FRAME_SIZE):                         # Check packet length
                    printAndLog("ERROR: Bad HIST Frame Size, %d" % packet_len)
                    result = -1
                    break

                rtn = verifyAllHistBinValues(data,TEST3_NUMBINS,TEST3_HIST_BINVALUE+TEST3_HIST_BINVALUE_MAXERR,TEST3_HIST_BINVALUE-TEST3_HIST_BINVALUE_MAXERR)  # Check all histogram bin values
                if (rtn != 0):
                    result = -1
                    break

            time1 = datetime.datetime.now()
            if (time1 - time0 > datetime.timedelta(0,TEST3_RUNTIME,0)):
                break

        # Verify that a proper packet even arrived
        if (properPacketArrived != 1):
            printAndLog("ERROR: Proper Packet was never received")
            result = -1

        # Disable the channel
        reg_00 = 0x00000000
        writeUserReg(0x00, reg_00)
        time.sleep(1)

        try:
            data, address = sock.recvfrom(RX_BUFF_LEN)  # Receive (and ignore) any last data from buffer
        except: pass
        printAndLog("Closing Socket ...")
        closeSocket()
        printAndLog("Finished testing DEMUX-%d-"%(demux_index))

    printAndLog("-------- Test 3 FINISHED --------")

    if (result != 0):
        writeToResults('[FAIL] Test 3')
    else:
        writeToResults('[SUCCESS] Test 3')

    return 0


def runTest4():
    result = 0
    printAndLog("-------- Test 4 --------")
    printAndLogTime()

    printAndLog("Opening Socket ...")
    rtn = openSocket()
    if (rtn != 0):
        writeToResults('[FAIL] Test 4')
        return -1
    printAndLog("Socket Successfully opened")

    printAndLog("Configuring Unit ...")
    rtn = configTest4()
    if (rtn != 0):
        printAndLog("ERROR during configuration")
        return -1
    printAndLog("Configuration Complete")

    printAndLog("Closing Socket ...")
    closeSocket()

    for sync_index in range(0,3):                                                # Loop over all SYNCx Inputs
        raw_input("Apply a "+TEST4_SIGNAL+" signal to SYNC-%d-, then press ENTER" % (sync_index))

        printAndLog("Opening Socket ...")
        rtn = openSocket()
        if (rtn != 0):
            writeToResults('[FAIL] Test 4')
            return -1
        printAndLog("Socket Successfully opened")

        time0 = datetime.datetime.now()
        ignoreFirstPacket = 1
        properPacketArrived = 0

        # Link the appropriate SYNCx input to CH0
        reg_05 = 0x00000000 + sync_index    # Cycle through SYNCx
        writeUserReg(0x05, reg_05)
        reg_00 = 0x00070001                 # Use CH0
        writeUserReg(0x00, reg_00)
        resetHarvester()

        printAndLog("Starting Data Collection, running for - %d - [s] " % TEST4_RUNTIME)
        while True:
            try:
                data, address = sock.recvfrom(RX_BUFF_LEN)
            except:
                printAndLog("ERROR: No Data Received")
                writeToResults('[FAIL] Test 4')
                return -1

            if (ignoreFirstPacket == 1):
                ignoreFirstPacket = 0
                continue

            packet_len = len(data)

            if (getPacketType(data[0:4]) == PACKET_HIST):                        # Check histogram packet when it arrives, will look at paired low and high channels
                properPacketArrived = 1
                if(packet_len != TEST4_HIST_FRAME_SIZE):                         # Check packet length
                    printAndLog("ERROR: Bad HIST Frame Size, %d" % packet_len)
                    result = -1
                    break

                rtn = verifyAllHistBinValues(data,TEST4_NUMBINS,TEST4_HIST_BINVALUE+TEST4_HIST_BINVALUE_MAXERR,TEST4_HIST_BINVALUE-TEST4_HIST_BINVALUE_MAXERR)  # Check all histogram bin values
                if (rtn != 0):
                    result = -1
                    break

            time1 = datetime.datetime.now()
            if (time1 - time0 > datetime.timedelta(0,TEST4_RUNTIME,0)):
                break

        # Verify that a proper packet even arrived
        if (properPacketArrived != 1):
            printAndLog("ERROR: Proper Packet was never received")
            result = -1

        # Disable the channel
        reg_00 = 0x00000000
        writeUserReg(0x00, reg_00)
        time.sleep(1)

        try:
            data, address = sock.recvfrom(RX_BUFF_LEN)  # Receive (and ignore) any last data from buffer
        except: pass
        printAndLog("Closing Socket ...")
        closeSocket()
        printAndLog("Finished testing SYNC-%d-"%(sync_index))

    printAndLog("-------- Test 4 FINISHED --------")

    if (result != 0):
        writeToResults('[FAIL] Test 4')
    else:
        writeToResults('[SUCCESS] Test 4')

    return 0


def runTest5():
    result = 0
    printAndLog("-------- Test 5 --------")
    printAndLogTime()

    printAndLog("Opening Socket ...")
    rtn = openSocket()
    if (rtn != 0):
        writeToResults('[FAIL] Test 5')
        return -1
    printAndLog("Socket Successfully opened")

    printAndLog("Configuring Unit ...")
    rtn = configTest5()
    if (rtn != 0):
        printAndLog("ERROR during configuration")
        writeToResults('[FAIL] Test 5')
        return -1
    printAndLog("Configuration Complete")

    printAndLog("Closing Socket ...")
    closeSocket()

    signal_set = [TEST5_SIGNAL1, TEST5_SIGNAL2, TEST5_SIGNAL3]
    value_set = [TEST5_PMON_VALUE1, TEST5_PMON_VALUE2, TEST5_PMON_VALUE3]
    error_set = [TEST5_PMON_VALUE_MAXERR1, TEST5_PMON_VALUE_MAXERR2, TEST5_PMON_VALUE_MAXERR3]

    for signal_index in range(0,len(signal_set)):                                   # Loop over the input signals
        for pin_index in range(0,6):                                                # Loop over all PINx Inputs
            promptStr = "Apply a "+signal_set[signal_index]+" signal to PIN-%d-, then press ENTER" % (pin_index)
            printAndLog(promptStr)
            raw_input(promptStr)

            printAndLog("Opening Socket ...")
            rtn = openSocket()
            if (rtn != 0):
                writeToResults('[FAIL] Test 5')
                return -1
            printAndLog("Socket Successfully opened")

            time0 = datetime.datetime.now()
            ignoreFirstPacket = 1
            properPacketArrived = 0

            printAndLog("Starting Data Collection, running for - %d - [s] " % TEST5_RUNTIME)
            while True:
                try:
                    data, address = sock.recvfrom(RX_BUFF_LEN)
                except:
                    printAndLog("ERROR: No Data Received")
                    return -1

                if (ignoreFirstPacket == 1):
                    ignoreFirstPacket = 0
                    continue

                packet_len = len(data)

                if (getPacketType(data[0:4]) == PACKET_PMON):                        # Check power monitor packet when it arrives
                    properPacketArrived = 1
                    if(packet_len != PMON_FRAME_SIZE):                               # Check packet length
                        printAndLog("ERROR: Bad PMON Frame Size, %d" % packet_len)
                        result = -1
                        break

                    rtn = verifyPmonValue(data,pin_index,value_set[signal_index]+error_set[signal_index], value_set[signal_index]-error_set[signal_index])  # Check all histogram bin values
                    if (rtn != 0):
                        result = -1
                        break

                time1 = datetime.datetime.now()
                if (time1 - time0 > datetime.timedelta(0,TEST5_RUNTIME,0)):
                    printAndLog("Measurement OK")
                    break

            # Verify that a proper packet even arrived
            if (properPacketArrived != 1):
                printAndLog("ERROR: Proper Packet was never received")
                result = -1

            try:
                data, address = sock.recvfrom(RX_BUFF_LEN)  # Receive (and ignore) any last data from buffer
            except: pass
            printAndLog("Closing Socket ...")
            closeSocket()
            printAndLog("Finished testing PIN-%d-"%(pin_index))

    printAndLog("-------- Test 5 FINISHED --------")

    if (result != 0):
        writeToResults('[FAIL] Test 5')
    else:
        writeToResults('[SUCCESS] Test 5')

    return 0


### --- MAIN -----------------------------------------------------------------
def main():
    tagStr = raw_input("Test Name Tag? Note: No Spaces, Date will be added")

    rtn = startNewLog(tagStr)
    if (rtn != 0):
        printAndLog("Init Error, ABORTED")
        return

    if (RUN_TEST1 == True):
        rtn = runTest1()
        if (rtn != 0):
            printAndLog("Test 1 Error, ABORTED")

    if (RUN_TEST2 == True):
        rtn = runTest2()
        if (rtn != 0):
            printAndLog("Test 2 Error, ABORTED")

    if (RUN_TEST3 == True):
        rtn = runTest3()
        if (rtn != 0):
            printAndLog("Test 3 Error, ABORTED")

    if (RUN_TEST4 == True):
        rtn = runTest4()
        if (rtn != 0):
            printAndLog("Test 4 Error, ABORTED")

    if (RUN_TEST5 == True):
        rtn = runTest5()
        if (rtn != 0):
            printAndLog("Test 5 Error, ABORTED")

    printAndLog("---> ALL TESTS COMPLETE <---")
    stopLog()
    printResultsFile()
    return

if __name__ == '__main__':
    main()