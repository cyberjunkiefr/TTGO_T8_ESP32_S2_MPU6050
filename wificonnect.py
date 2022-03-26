
import network


def connectSTA(ssid, password, name='MicroPython'):
    global station
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print('Connecting to network...')
        station.active(True)
        print(ssid, password)
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    station.config(dhcp_hostname = name)
    print('network config:', station.ifconfig())
    print("station.config(dhcp_hostname) =", station.config('dhcp_hostname'))
    return station.ifconfig()[0]


def connectAP(name, password=''):
    global ap
    print('connecting the Access Point...')
    ap = network.WLAN(network.AP_IF)
    ap.active(True) #activating
    ap.config(essid=name, password=password)
    while ap.active() == False:
      pass
    print('Acces Point config:', ap.ifconfig())
    return ap.ifconfig()[0]