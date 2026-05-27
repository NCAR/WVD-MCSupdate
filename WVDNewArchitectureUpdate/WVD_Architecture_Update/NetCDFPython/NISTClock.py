# pip install ntplib, pip install pathlib

import datetime, ntplib, pathlib 

def ConvertTS2Date(TimeStamp):
   return(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d'))
    
def ConvertTS2Hour(Time,Precision=8):
    return("{:.{}f}".format((float(Time.strftime('%H'))         ) + \
                            (float(Time.strftime('%M'))    /60  ) + \
                            (float(Time.strftime('%S.%f')) /3600),Precision))

def WriteData(String,FileName):
    File = pathlib.Path(FileName)
    File.parent.mkdir(exist_ok=True, parents=True)
    with open(File,"a") as f:
        f.write(String)

def check_time_difference(FileName):
    # Official NIST time servers (e.g., time.nist.gov)
    nist_server = "time.nist.gov"

    try:
        # Create an NTP client and request time from the NIST server
        response = ntplib.NTPClient().request(nist_server, version=3)
        # Calculate local vs. server time difference
        offset = response.offset
        # Calculate the datetimes
        now  = datetime.datetime.now(datetime.timezone.utc)
        nist = datetime.datetime.fromtimestamp(response.tx_time,datetime.UTC)
        # Converting datetimes to strings
        LocalString = ConvertTS2Date(now)  + '\t' + ConvertTS2Hour(now)  + '\t'
        NistString  = ConvertTS2Date(nist) + '\t' + ConvertTS2Hour(nist) + '\t'
        # Writting data
        WriteData(LocalString + NistString + "{:.{}f}".format(offset,6) + '\n',FileName)
               
    except Exception:
        ErrorString = '-1000.00\t-1000.00000\t'*2 + "{:.{}f}".format(-10,6) + '\n'
        WriteData(ErrorString,FileName)