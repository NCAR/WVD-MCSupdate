

import sys, WeatherStationTCP as WS


if __name__ == '__main__':
    # Calling weather station probe function with system arguement variables
    Parameters = WS.WeatherStationProbe(IPAddress=sys.argv[1],
                                        Port=int(sys.argv[2]),
                                        Timeout=float(sys.argv[3])/1000.)
    # Converting the returned values to a response string for labview
    print('WS_Luft_WSData_' + '_'.join([str(Value) for Value in Parameters]))


