from machine import *
from random import *
import mpu6050
import time, utime, wificonnect, st7789, picoweb
import vga1_bold_16x32, vga1_8x16, s2mini, vga1_8x8  # font
import tft_config_s2 as tft_config
from wificonnect import *

# definition du display
tft = tft_config.config(rotation=0)
tft.init()

def connection(ssid='', password='', name=''):
    ip = ''
    ap = True
    tft.rotation(3)
    tft.text(vga1_8x16, "Connecting STA...", 6, 10, st7789.CYAN)
    time.sleep_ms(2000)
    try:
        ip = connectSTA(ssid, password,name)
        ap = False
    except:
        ip = ''
        try:
            tft.text(vga1_8x16, "Connecting AP....", 6, 10, st7789.CYAN)
            time.sleep_ms(2000)
            ip = connectAP(name)
        except:
            ip = ''
    tft.rotation(0)
    tft.fill(st7789.BLACK)
    return ip, ap


def initMPU():
    global mpu
    i2c = SoftI2C(scl=Pin(7), sda=Pin(8))     #initializing the I2C method for ESP32
    mpu= mpu6050.accel(i2c)
def inittft(firstline=50,separation=20):
    global ipaddress
    tft.text(vga1_bold_16x32, "DATAS:", 6, 10, st7789.CYAN)
    tft.hline(0,42,135,st7789.RED)
    tft.hline(0,43,135,st7789.RED)
    tft.text(vga1_8x16, "AcX:", 6, firstline, st7789.GREEN)
    tft.text(vga1_8x16, "AcY:", 6, firstline + 1 * separation, st7789.GREEN)
    tft.text(vga1_8x16, "AcZ:", 6, firstline + 2 * separation, st7789.GREEN)
    tft.text(vga1_8x16, "Tmp:", 6, firstline + 3 * separation, st7789.MAGENTA)  
    tft.text(vga1_8x16, "GyX:", 6, firstline + 4 * separation, st7789.YELLOW)
    tft.text(vga1_8x16, "GyY:", 6, firstline + 5 * separation, st7789.YELLOW)
    tft.text(vga1_8x16, "GyZ:", 6, firstline + 6 * separation, st7789.YELLOW)
    tft.text(vga1_8x16, ipaddress , 1, firstline + 8 * separation, st7789.WHITE)

def showtft(firstline=50,separation=20):
    global datas
    datas = mpu.get_values()
    tft.text(vga1_bold_16x32, "DATAS:", 6, 10, st7789.CYAN)
    tft.text(vga1_8x16, str(datas['AcX']), 50, firstline, st7789.GREEN)
    tft.text(vga1_8x16, str(datas['AcY']), 50, firstline + 1 * separation, st7789.GREEN)
    tft.text(vga1_8x16, str(datas['AcZ']), 50, firstline + 2 * separation, st7789.GREEN)
    tft.text(vga1_8x16, str(datas['Tmp']), 50, firstline + 3 * separation, st7789.MAGENTA)  
    tft.text(vga1_8x16, str(datas['GyX']), 50, firstline + 4 * separation, st7789.YELLOW)
    tft.text(vga1_8x16, str(datas['GyY']), 50, firstline + 5 * separation, st7789.YELLOW)
    tft.text(vga1_8x16, str(datas['GyZ']), 50, firstline + 6 * separation, st7789.YELLOW)

def readdatas():
    global datas
    datas = mpu.get_values()

def handleInterrupt(timer):
    global station
    readdatas()
    showtft()

# ---- Routing Picoweb ------------------------------------ 
app = picoweb.WebApp(__name__)
@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.sendfile(resp, '/web/index.html')


@app.route("/get_datas")
def get_volume(req, resp):
    global datas
    yield from picoweb.jsonify(resp, datas)


@app.route("/style.css")
def css(req, resp):
    print("Send style.css")
    yield from picoweb.start_response(resp)
    yield from app.sendfile(resp, '/web/style.css')


@app.route("/logonew.jpg")
def image(req, resp):
    print("Download JPG")
    yield from picoweb.start_response(resp)
    try:
        with open("web/logonew.jpg", 'rb') as img_binary:
            img= img_binary.read()
        yield from resp.awrite(img)
    except Exception:
        print("Image file not found.")
        pass

@app.route("/favicon.ico")
def image(req, resp):
    print("Download ICO")
    yield from picoweb.start_response(resp)
    try:
        with open("web/favicon.ico", 'rb') as img_binary:
            img= img_binary.read()
        yield from resp.awrite(img)
    except Exception:
        print("Image file not found.")
        pass

#---------MAIN---------------------    
ipaddress, ap = connection(ssid='Roel_Was_Here', password='Rj060195', name='MPU6050_Test')
if ipaddress:
    print(ipaddress)
    initMPU()
    inittft()
    timer = Timer(0)
    timer.init(period=500, mode=Timer.PERIODIC, callback=handleInterrupt)
    try:
        app.run(debug=True, host = ipaddress, port = 80)
    except KeyboardInterrupt:
        timer.deinit()
        print ('KeyboardInterrupt exception is caught')
    else:
        print ('No exceptions are caught')
else:
    print("No connection....")
