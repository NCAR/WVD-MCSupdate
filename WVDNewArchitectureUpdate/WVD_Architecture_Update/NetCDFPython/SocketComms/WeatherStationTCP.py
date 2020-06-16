
from CommsClass import TCPComms as TCP

def WeatherStationProbe(IPAddress='192.168.0.111',Port=4760,Timeout=1,Body=300,Term=b"\r"):
    # Defining commands to be sent
    CommList  = [b"$ 28763 M 00160\r", b"$ 28763 M 00260\r", 
                 b"$ 28763 M 00360\r", b"$ 28763 M 00270\r"]
    Range     = [110.,100.,900.,1000.]
    Offset    = [-50.,  0.,300.,   0.]
    # Initializing the communication class
    S = TCP(IPAdd=IPAddress,Port=Port,Timeout=Timeout,BodyLen=Body,TermChar=Term)
    # Send the communications
    _ , Response, Error = S.Communicate(CommList)
    # Parsing and understanding the response
    ResponseList = WeatherStationCheckResponse(CommList,Response,Error,Term,Range,Offset)
    return(ResponseList)
    
def WeatherStationCheckResponse(CommList,Response,Error,Term,Range,Offset):
    # Checking the weather station response
    if Error is None :
        # No error occurred
        ResponseList = WeatherStationDecode(CommList, Response,Term,Range,Offset)
    else:
        # An error occured so make a fake response
        if   Error == 'Error in the Initialization method':  ErrorCode = -2001
        elif Error == 'Error in the Send method':            ErrorCode = -2002
        elif Error == 'Error in the Read method':            ErrorCode = -2003
        else:                                                ErrorCode = -2000       
        ResponseList = [ErrorCode]*len(CommList)
    return(ResponseList)
    
def WeatherStationDecode(Commands,Responses,TermChar,Ranges,Offsets):
    # Looping over all of the responses and checking that they are reasonable
    # Note the weather station echos the command
    Value = []
    for Comm,Resp,Range,Offset in zip(Commands,Responses,Ranges,Offsets):
        # Stripping off the termination characters
        Comm = Comm.decode("utf-8").replace(TermChar.decode("utf-8"),'')
        Resp = Resp.decode("utf-8").replace(TermChar.decode("utf-8"),'')
        # Checking for the command echo and converting to a physical value
        try:
            Resp = int(Resp.replace(Comm,'')) if Comm in Resp else -99
            Value.append((Resp/65520)*Range+Offset)
        except ValueError:
            # Value error arrises from empty response which makes int('')
            Value.append(-2004)
        except:
            Value.append(-2000)
    return(Value)
    
if __name__ == '__main__':
    print(WeatherStationProbe())