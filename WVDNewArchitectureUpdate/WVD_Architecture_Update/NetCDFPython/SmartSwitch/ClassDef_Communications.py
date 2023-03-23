#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written By: Robert Stillwell
# Written For: NCAR
# This set of classes is used to define TCP and UDP communication for Holodec.
# An inherited class called Common is available for all subsequent classes and 
# only contains methods, not attributes. The main goal of these methods is to 
# allow for conversion of all attributes from a class to a string. The second 
# inherited class defines general methods for ethernet communication that are
# specified by the TCP/UDP classes if necessary. If their generality suffices,
# the methods are not overwritten.  
#%% Importing needed libraries
import functools, socket, time
#%% Defining class for conversion to/from strings (for use with string queues)
class Common:
    # Calling an empty constructor if needed
    def __init__(self):
        pass    
    # Defining a shortcut to concatenate strings using a plus sign
    def __add__(self,other):
        return(str(self) + self._Delimiter() + other)
    def __radd__(self,other):
        return(other + self._Delimiter() + str(self))
    # Defining the number of attributes in the class
    def __len__(self):
        return(len(self.__dict__))
    # Defining how this class is printed (as semicolon delimitated string)
    def __repr__(self):
        return (str(self))
    def __str__(self):
        # Making a list of all defined attribute keys and values
        L = [str(E) for P in zip(self.__dict__.keys(),self.__dict__.values())\
                    for E in P]
        return(self._Delimiter().join(L)) 
    # Defining initial attributes 
    def _DefineAttribute(self,Variable):
        return(str(Variable) if Variable is not None else '')
    # Return delimiter without adding attribute (variable not counted in len)
    def _Delimiter(self):  
        return(';')
    # Filling structure from a long string and returning the extra string
    def FromString(self,String):
        # Determining the number of elements to remove from the string
        El = len(self)
        # Defining attributes from input string
        P = String.split(self._Delimiter())  
        for Attr,Val in zip(P[0:El*2:2],P[1:El*2:2]): setattr(self, Attr, Val) 
        # Returning the remaining string
        return(self._Delimiter().join(P[El*2:]))
    # Making a public facing method to convert class to string
    def ToString(self):
        return(str(self))
#%% Defining the ethernet class and methods 
# Possible calls:
# 1) Class  = Comms('192.168.0.116',9500,1000,-1,-1,'\r\n')
# 2) R         = Comms()
#    Remaining = R.FromString(String= str(Class) + ';Something;SomethingElse')
class Comms(Common):
    """ This class contains elements needed for ethernet communications:
        IPAddress:  Local IP of the target of communication
        Port:       Ethernet port to use for communications
        Timeout:    Time to allow communications before closing [seconds]
        HeaderLen:  The length of the header of the response to be thrown away
                    (a value of -1 forces this attribute to be ignored)
        BodyLen:    The length of the body to be returned
                    (a value of -1 forces this attribute to be ignored)
        TermChar:   The termination character of the response string
        String:     A semicolon delimitated string that contains all the 
                    attribute names and values to construct the class      """
######################## Defining the TCP attributes #########################
    def __init__(self,IPAdd=None, Port=None, Timeout=None, HeaderLen=None, \
                      BodyLen=None, TermChar=None,String=None):        
        if String is None:
            self.BodyLen      = self._DefineAttribute(BodyLen)
            self.HeaderLen    = self._DefineAttribute(HeaderLen)
            self.IPAddress    = self._DefineAttribute(IPAdd)
            self.Port         = self._DefineAttribute(Port)
            self.TermChar     = self._DefineAttribute(TermChar)
            self.Timeout      = self._DefineAttribute(Timeout)
            self._Socket      = self._DefineAttribute(None)
            self._SocketError = self._DefineAttribute(None)
            self._ErrorString = self._DefineAttribute(None)
        else:
            self.FromString(String)      
########################## Defining error handling ###########################
    # This method defines the steps to follow if a socket error is encountered
    def _ErrorHandler(self,Where,Error):
        self.Disconnect()
        self._Socket      = None
        self._SocketError = True
        self._ErrorString = 'Error in the ' + Where + ' method: ' + str(Error)
        print(self._ErrorString)
    # This decorator will call a method. If it fails it call the error handler   
    def _TryCommand(Func):
        @functools.wraps(Func) # Bringing docstring & metadata from input Func
        def Wrapper(self,*args,**kwargs):
            try:
                return(Func(self,*args,**kwargs))
            except Exception as e:
                if Func.__name__ != 'Disconnect': 
                    self._ErrorHandler(Func.__name__,e)
            return
        return(Wrapper)
    # This decorator checks for a live socket and a lack of recorded errors
    def _CheckError(Func):
        @functools.wraps(Func) # Bringing docstring & metadata from input Func
        def Wrapper(self,*args,**kwargs):
            if self._Socket is not None and self._SocketError is False:
                return(Func(self,*args,**kwargs))
        return(Wrapper)
####################### Defining general communication #######################
########## Note here that the default values are set to TCP settings #########
    # Method used to connect to a socket (decorated with error handler)
    @_TryCommand
    def Connect(self,Type='SOCK_STREAM'):
        self._Socket = socket.socket(socket.AF_INET,getattr(socket,Type))
        self._Socket.settimeout(int(self.Timeout))
        self._SocketError = False
        self._ErrorString = ''    
    # Method used to close out the socket (decorated with error handler)
    @_TryCommand
    def Disconnect(self):
        self._Socket.close()
    # Method to read data from a socket (decorated with check & error handler)
    @_TryCommand
    @_CheckError
    def Read(self,ReadType='recv',Bytes=1024):
        return(getattr(self._Socket,ReadType)(Bytes))
    # Method to send data to a socket (decorated with check & error handler)
    @_TryCommand
    @_CheckError
    def Send(self,Message='',SendType='sendall'):
        getattr(self._Socket,SendType)(Message)
 #%% Defining the TCP class and methods   
class TCP(Comms):
    # Explicitly copying doc string from Comms class
    __doc__ = Comms.__doc__
    # Calling the inherited constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
    # Calling the inherited "Connect" method but specifying the socket type 
    # then actually connecting to the socket
    @Comms._TryCommand
    def Connect(self):
        super().Connect('SOCK_STREAM')
        self._Socket.connect((self.IPAddress,int(self.Port)))

    def SlowRead(self,ReadType='recv',Bytes=1024,Wait=0.05):
        time.sleep(Wait)
        return(self.Read(ReadType=ReadType,Bytes=Bytes))

#%% Defining the UDP class and methods
class UDP(Comms):
    # Explicitly copying doc string from Comms class
    __doc__ = Comms.__doc__
    # Calling the inherited constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
    # Calling the inherited "Connect" method but specifying socket type as UDP
    def Connect(self):
        super().Connect('SOCK_DGRAM')
    # Calling inherited "Read" method but specifying reading method for UDP 
    def Read(self,*args, **kwargs):
        return(super().Read(ReadType='recvfrom',*args, **kwargs)[0])  
    # Sending data using inherited decorators. This can't be generalized as
    # the number of parameters called is different than for TCP
    @Comms._TryCommand
    @Comms._CheckError
    def Send(self,Message):
        self._Socket.sendto(Message,(self.IPAddress,int(self.Port)))