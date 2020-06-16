# Written By: Robert Stillwell
# Written For: NCAR

#%% Imported needed libraries
import socket, time 

#%% Defining the common communication class
class Common(object):
    # Initializer to hold all variables. Variables with _ in front are private
    def __init__(self,IPAdd,Port,Timeout,HeaderLen=None,BodyLen=None,TermChar=None,Type=None):        
        self._IPAddress  = IPAdd
        self._Port       = Port
        self._Timeout    = Timeout
        self._HeaderLen  = HeaderLen
        self._BodyLen    = BodyLen
        self._TermChar   = TermChar
        self._Type       = Type
        self.Socket      = None
        self.SocketError = False
        self.ErrorString = None
    def _CommSingle(self,String):
        self.Send(String)
        time.sleep(0.050)
        H = self.Read(self._HeaderLen)
        R = self.Read(self._BodyLen)
        return (H,R)
    # Method to do communications with a single string or a list of strings
    def Communicate(self,Strings):
        self.Connect()
        if type(Strings) is list:
            Header = []; Response = []
            for String in Strings:
                (H,R) = self._CommSingle(String)
                Header.append(H); Response.append(R)
        else:
            (Header,Response) = self._CommSingle(Strings)
        self.Disconnect()
        return Header,Response,self.ErrorString
    # Method used to initialize the socket for TCP communications
    def Connect(self):
        try:
            if self._Type == 'TCP':
                self.Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            elif self._Type == 'UDP':
                self.Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            else:
                raise(AttributeError)
            self.Socket.settimeout(self._Timeout)
            self.Socket.connect((self._IPAddress,self._Port))
        except:
            self.ErrorHandler('Initialization')    
    # Method used to close out the socket for TCP communications
    def Disconnect(self):
        try:
            self.Socket.close()
        except:
            pass
    # Method used to clean up errors and signal errors 
    def ErrorHandler(self,Where):
        self.Disconnect()
        self.Socket      = None
        self.SocketError = True
        self.ErrorString = 'Error in the ' + Where + ' method'
                
#%% Defining raw TCP socket communication class     
class TCPComms(Common):
    """Definition string"""
    # Initilizer...uses common initilaizer but specifies TCP type
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, Type = 'TCP')            
    # Method used to send data to a socket via TCP communications
    def Send(self,Message):
        if self.Socket is not None and self.SocketError is False:
            try:
                self.Socket.send(Message)
            except:
                self.ErrorHandler('Send')
    # Methods used to read data from a socket via TCP communications
    def Read(self,Length):
        if None not in [self.Socket,Length] and self.SocketError is False:
            try:
                return self._ReadChunks(Length)
            except:
                self.ErrorHandler('Read')
                return None
    def _ReadChunks(self,Length):
        Chunks = []; BytesReceived = 0; Timeout  = False; TermChar = False;
        Start = time.time()
        while BytesReceived < Length and True not in [Timeout,TermChar]:
            # Reading a chunk of data availible at the TCP port
            Chunks.append(self.Socket.recv(Length))
            BytesReceived += len(Chunks[-1])
            # Checking predefined stop conditions...either a timeout or the 
            # response contains the expected termination character 
            if time.time()>(Start+self._Timeout): Timeout  = True  
            if self._TermChar in Chunks[-1]:      TermChar = True
            # Raise an exception if the socket crashes
            if Chunks[-1] == '': print('Connection closed unintentionally')
            # Adding a small delay to prevent possibe race condition
            time.sleep(0.050)
        # Return the chunk data combined into a single response
        return(b"".join(Chunks))
    
