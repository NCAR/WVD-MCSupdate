
from CommsClass import TCPComms as TCP

def WeatherStationProbe(IPAddress='192.168.0.110',Port=4760,Timeout=1,Body=30,Term=b"\r"):
    # Defining commands to be sent
    CommList  = [b"& 28673 M 00160\r", b"& 28673 M 00260\r", 
                 b"& 28673 M 00360\r", b"& 28673 M 00270\r"]
    Range     = [110.,100.,900.,1000.]
    Offset    = [-50.,  0.,300.,   0.]
    # Initializing the communication class
    S = TCP(IPAdd=IPAddress,Port=Port,Timeout=Timeout,BodyLen=Body,TermChar=Term)
    # Send the communications
    _ , Response, Error, ErrorNumber = S.Communicate(CommList)
    # Parsing and understanding the response
    ResponseList = CheckResponse(CommList,Response,ErrorNumber,Term,Range,Offset)
    return(ResponseList)
    
def CheckResponse(Commands,Response,Error,Term,Range,Offset):
    # Checking the response or return error code instead of the data
    return(Decode(Commands,Response,Term,Range,Offset) if Error is None else [Error]*len(Commands))
    
def Decode(Commands,Responses,TermChar,Ranges,Offsets):
    # Looping over all of the responses and checking that they are reasonable
    # Note: weather station echos the command with a different init character
    Value = []
    for Comm,Resp,Range,Offset in zip(Commands,Responses,Ranges,Offsets):
        # Stripping off the initiation and termination characters
        Strip = lambda S: S.decode("utf-8").replace(TermChar.decode("utf-8"),'')[1:]
        Comm = Strip(Comm); Resp = Strip(Resp);
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