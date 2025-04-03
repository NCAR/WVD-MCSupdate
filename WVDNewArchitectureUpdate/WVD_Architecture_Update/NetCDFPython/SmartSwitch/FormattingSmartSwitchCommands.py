#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:48:32 2023

@author: stillwel
"""
from copy import deepcopy
from enum import Enum, unique
from ClassDef_Communications import TCP

#%% Defining enums for settings
@unique
class ControlSignals(Enum):
    """Binary options for the control signals"""
    Start       = 1<<0
    Done        = 1<<1
    Idle        = 1<<2
    Ready       = 1<<3
    AutoRestart = 1<<7

@unique
class Timers(Enum):
    """Names of each of the hardwared timers"""
    Timer_0 = 0  # TSOA         = 0    # Value of 1: on    , 0: off
    Timer_1 = 1  # Online       = 1    # Value of 1: on    , 0: off
    Timer_2 = 2  # Offline      = 2    # Value of 1: on    , 0: off
    Timer_3 = 3  # OnOffMux     = 3    # Value of 1: online, 0: offline
    Timer_4 = 4  # LongShortMux = 4    # Value of 1: short , 0: long
    Timer_5 = 5  # KeyedMux     = 5    # Value of 1: keyed , 0: not keyed
    Timer_6 = 6  # Detector Date
    Timer_7 = 7
    
    
#%% Defining the pulse block definitions   
class WordFormatter:
############### Methods to create commands to the smart switch ################
    # Format a base 10 decimal number into a base 2 binary string
    def _FormatBitString(self,Number,Width=8):
        return(str.format('0x{:0'+str(Width)+'b}', Number))
    # Format a base 10 decimal number into a base 16 hex string
    def _FormatByteString(self,Number,Width=8):
         return(str.format('0x{:0'+str(Width)+'X}', Number)[2:])
    # Format a command like Adam to send read data to screen
    def _FormatCommand(self,Address,Value,Read):
        return(('r ' if Read else 'w ')+Address+' '+self._FormatByteString(Value,8))
###############################################################################
    
############# Methods defining how to interface with register map #############
    # Defining how to traverse register map for pulse definitions
    def _AccessPulseDef(self,Type,SeqNum,Read=True):
        # Find register map address and then format request
        Base,_,Width,_ = self._AccessRegisterMapPulse(Type,self._RegMap,self._RegMapConvert)
        ReadWrite = "Reading" if Read else "Writing"
        if SeqNum is not None:
            HumanRead = ' : '+ReadWrite+' pulse definition #'+str(SeqNum)+' '+Type
            Address   = self._FormatByteString(Base+SeqNum*Width) 
        else:
            HumanRead = ' : '+ReadWrite+' '+Type
            Address   = self._FormatByteString(Base) 
        return(Address,HumanRead)
    # Defining how to traverse register map for bus (common variable) definitions
    def _AccessRegisterMapBus(self,String,RegMap,Convert):
        # Formatting the Register Map Strings using Adam's naming convention
        S1 = 'XMPD_CONTROLLER_CFG_BUS_ADDR_';
        Address = int(RegMap[S1+Convert[String]],0)
        return(self._FormatByteString(Address))
    # Defining method to convert between C++ header file and python for pulse definitions
    def _AccessRegisterMapPulse(self,String,RegMap,Convert):
        # Determining the converted string
        CStr = Convert[String]
        # Formatting the Register Map Strings using Adam's naming convention
        S1 = 'XMPD_CONTROLLER_CFG_BUS_'; S2 = '_CFG_PULSE_SEQUENCE_'
        return(int(RegMap[S1+'ADDR'+S2+CStr+'_BASE'],0),  # Units: [Bytes]
               int(RegMap[S1+'ADDR'+S2+CStr+'_HIGH'],0),  # Units: [Bytes]
               int(int(RegMap[S1+'WIDTH'+S2+CStr],0)/8),  # Units: [Bytes]
               int(int(RegMap[S1+'DEPTH'+S2+CStr],0)/8))  # Units: [Bytes]
    # Defining how to change Adam's variable naming convention to python
    def _DefineRegMapNaming(self):
        # Looping over the 8 Pulse Definitions
        A = ['TIMER_OFFSET_','TIMER_WIDTH_','OOK_SEQUENCE_'] # Adam's version
        P = ['Offset','Width','OOKSequence']                 # Python version
        Converter = {p+str(m):a+str(m) for a,p in zip(A,P) for m in range(0,len(Timers))}
        # Adding the common pulse definitions
        Converter['PulseRepTime']   = 'PRT'
        Converter['PulseNum']       = 'NUM_PULSES'
        Converter['OfflineNum']     = 'NUM_OFFLINE_PULSES'
        Converter['OnlineNum']      = 'NUM_ONLINE_PULSES'
        Converter['BlockPostTime']  = 'BLOCK_POST_TIME'
        Converter['ControlFlags']   = 'CONTROL_FLAGS'
        Converter['DAC']            = 'DAC'
        # Adding the bus definitions 
        Converter['AP']             = 'AP_CTRL'
        Converter['StartStopIndex'] = 'CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA'
        Converter['Pulses2Execute'] = 'CFG_NUM_PULSES_TO_EXECUTE_DATA'
        return(Converter)
    # Reading the C++ header file for Smart Switch to determine register map
    def _ReadRegisterMapFile(self,File='xmpd_controller_hw.h'):
        # Reading data file
        Definitions = {}
        with open(File) as header:
            for line in header:
                if line[0:8] == '#define ':
                    SplitLine = line.split()
                    key, value = SplitLine[1], SplitLine[2]
                    Definitions[key] = value
        return(Definitions)    
###############################################################################
    # Formatting a write or read command for pulse sequence parameters
    def FormatPulseSequence(self,Type,SeqNum=None,Read=True):
        if Read:
            Value = 0
        else:
            # Checking if the commanded type to set is recognized
            if Type in ['PulseRepTime','PulseNum','OfflineNum','OnlineNum','BlockPostTime','ControlFlags']:
                Value = getattr(self,Type)
            elif Type.startswith(('Offset','Width','OOKSequence')):
                Value = getattr(self.Timers[int(Type[-1])],Type[:-1])
            elif Type in ['DAC']:
                Value = ((self.dacB<<16) + self.dacA)            
            else:
                return('Unknown variable to set')
        # If not returned because of unknown command, find register map address
        # and then format response
        Address,HumanRead = self._AccessPulseDef(Type,SeqNum,Read)
        return(self._FormatCommand(Address,Value,Read),HumanRead)
    # Formatting a write or read command for 
    def FormatSchedule(self,StartIndex, StopIndex, Read=True):
        ''''Formatting the string to set or read: cfg_pulse_sequence_start_stop_indexes'''
        HumanRead = ' : {} control scheduler start/stop indices'.format('Reading' if Read else 'Writing')
        Address = self._AccessRegisterMapBus('StartStopIndex',self._RegMap,self._RegMapConvert)#'XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA'
        Value   = 0 if Read else (StopIndex<<16) + StartIndex 
        return(self._FormatCommand(Address,Value,Read),HumanRead)
    # Formatting a write or read command for 
    def FormatPulses2Execute(self,Pulses, Read=True):
        '''Formatting the string to set or read: CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA'''
        HumanRead = ' : {} number of pulses to execute'.format('Reading' if Read else 'Writing')        
        Address = self._AccessRegisterMapBus('Pulses2Execute',self._RegMap,self._RegMapConvert)
        Value   = 0 if Read else Pulses 
        return(self._FormatCommand(Address,Value,Read),HumanRead)
    # Formatting a write or read command for 
    def FormatControlStartStop(self,Start=True, Read=True):
        ''''Formatting the string to set or read: CFG_BUS_ADDR_CFG_NUM_PULSES_TO_EXECUTE_DATA'''
        if Read:
            HumanRead = ' : Reading controller start/stop state'
        else:
            HumanRead = ' : {} controller'.format('Starting' if Start else 'Stopping')
        Address = self._AccessRegisterMapBus('AP',self._RegMap,self._RegMapConvert)
        return(self._FormatCommand(Address,Start,Read),HumanRead)

    
         
class PulseTimer:
    def __init__(self,m):
        self.TimerNum    = m
        self.Offset      = 0   # First, wait this many cycles before setting pulse
        self.Width       = 0   # Then, wait this many cycles before clearing pulse
        self.OOKSequence = 0   # Step through these bits, LSB to MSB, each 'Width' long
    def SetFullPulse(self,Offset,Width,OOK):
        self.Offset      = Offset
        self.Width       = Width
        self.OOKSequence = OOK
    
class PulseBlockDefinition(WordFormatter):
    def __init__(self):
        self.PulseRepTime     = 14200    # Pulse repetition time [in fpga cycles]
        self.PulseNum         = 2        # Generate this many pulses
        self.OfflineNum       = 1        # Number of online pulses 
        self.OnlineNum        = 1        # Number of offline pulses
        self.BlockPostTime    = 0        # Time at the end of the group of pulses, [in cycles]
        self.ControlFlags     = 0        # Set the CONTROL_FLAGS output to this value
        self.dacA             = 52428    # Set DAC voltage A to these values
        self.dacB             = 65535    # Set DAC voltage B to these values
        self.Timers           = [PulseTimer(m) for m in range(0,len(Timers))]
        self._RegMap          = self._ReadRegisterMapFile()
        self._RegMapConvert   = self._DefineRegMapNaming()
        
    def VariablesToSet(self):
        # Defining what variables I would like to set/read
        ToSet = ['PulseRepTime','PulseNum','OfflineNum','OnlineNum','BlockPostTime','ControlFlags','DAC']  + \
                  [n + str(m) for n in ['Offset','Width','OOKSequence'] for m in range(0,len(Timers))]
        return(ToSet)
        
        
#%% General Function to be used
def Coerce(Val,Bot,Top):
    return(Val if (Bot <= Val <= Top) else (Bot if Bot > Val else Top))
    
def HRPrint(Command,HR,PrintHR=False):
    '''Printing commans to the smart switch with human readable information'''
    print(Command+HR if PrintHR else Command)
    
def SendRead(T,Command):
    CommandToSend = bytes(Command,'utf-8') + b'\r\n'
    T.Send(CommandToSend)
    print('Sent: ', CommandToSend, 'Response: ', T.Read())

def ReadWriteAllPulseDefinitions(T,PulseDefs,Start=0,Stop=0,Pulses2Execute=0,Read=True,HReadable=True):
    # Setting or reading variables needed to define all pulse blocks
    for a,SeqNum in zip(PulseDefs,range(0,len(PulseDefs))):
        for Param in a.VariablesToSet(): 
            Command,_ = a.FormatPulseSequence(Param,SeqNum,Read)
            SendRead(T,Command)
    # Setting or reading variables common to all pulse blocks
    Command,_ = a.FormatSchedule(StartIndex=Start,StopIndex=Stop,Read=Read)
    SendRead(T,Command)
    Command,_ = a.FormatPulses2Execute(Pulses2Execute,Read=Read)
    SendRead(T,Command)
    Command,_ = a.FormatControlStartStop(ControlSignals.Start.value,Read=Read)
    SendRead(T,Command)


#%% Formatting string commands to be sent to the Smart Switch
if __name__ == '__main__':
      # Instantiating a TCP connection
      T = TCP(IPAdd='192.168.0.150',Port=2222,Timeout=1,HeaderLen=-1,BodyLen=-1,TermChar='\r\n')
      T.Connect()

      # Instantiating a default pulse block definition
      A = PulseBlockDefinition()
      B = deepcopy(A); C = deepcopy(A); D = deepcopy(A);
      ############## Creating unique pulse definitions ##############
      PulseDefs = []
      # Timer 0 (Long pulses)
      A.Timers[Timers.Timer_0.value].SetFullPulse(300, 100, 1) # WV TSOA
      A.Timers[Timers.Timer_1.value].SetFullPulse(300, 110, 1) # On/Off TWA
      A.Timers[Timers.Timer_2.value].SetFullPulse(290, 120, 1) # Gate
      A.Timers[Timers.Timer_4.value].SetFullPulse(300, 100, 1) # Sync 0
      A.Timers[Timers.Timer_5.value].SetFullPulse(300, 100, 1) # O2 TSOA
      A.ControlFlags = (1<<2) + (1<<6) + (0<<7) + (1<<20);     # Flag 2 & 20: Timer 2 Inverted,
                                                               # Flag 6: RF1, Flag 7: RF2
      A.dacA = 52428
      A.dacB = 65535
      PulseDefs.append(A)

      # Timer 1 (Short Pulses)
      B.Timers[Timers.Timer_0.value].SetFullPulse(300, 20, 1)  # WV TSOA
      B.Timers[Timers.Timer_1.value].SetFullPulse(300, 30, 1)  # On/Off TWA
      B.Timers[Timers.Timer_2.value].SetFullPulse(290, 30, 1)  # Gate
      B.Timers[Timers.Timer_3.value].SetFullPulse(300,100, 1)  # Sync 1
      B.Timers[Timers.Timer_5.value].SetFullPulse(300, 20, 1)  # O2 TSOA
      B.ControlFlags = (1<<2) + (0<<6) + (1<<7) + (1<<20);     # Flag 2 & 20: Timer 2 Inverted,
                                                               # Flag 6: RF1, Flag 7: RF2
      B.dacA = 52428
      B.dacB = 65535
      PulseDefs.append(B)
      
      # Timer 2 (Long Pulse Scan Mode)
      C.Timers[Timers.Timer_1.value].SetFullPulse(300, 2000, 1) # On/Off TWA
      C.Timers[Timers.Timer_4.value].SetFullPulse(300, 2000, 1) # Sync 0
      C.ControlFlags = (1<<2) + (1<<6) + (0<<7) + (1<<20);     # Flag 2 & 20: Timer 2 Inverted,
                                                               # Flag 6: RF1, Flag 7: RF2
      C.dacA = 52428
      C.dacB = 65535
      PulseDefs.append(C)
      
      # Timer 3 (Short Pulse Scan Mode)
      D.Timers[Timers.Timer_1.value].SetFullPulse(300, 2000, 1) # On/Off TWA
      D.Timers[Timers.Timer_3.value].SetFullPulse(300, 2000, 1) # Sync 0
      D.ControlFlags = (1<<2) + (0<<6) + (1<<7) + (1<<20);     # Flag 2 & 20: Timer 2 Inverted,
                                                               # Flag 6: RF1, Flag 7: RF2
      D.dacA = 52428
      D.dacB = 65535
      PulseDefs.append(D)
    
      # Writting (or reading) pulse definitions
      ReadWriteAllPulseDefinitions(T,PulseDefs,Start=0,Stop=0,Read=False,HReadable=False)

      T.Disconnect()
