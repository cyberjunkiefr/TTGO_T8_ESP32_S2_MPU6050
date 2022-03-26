"""Generic ESP32_S2 with ST7789 240x320 display"""

from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=31250000, sck=Pin(36), mosi=Pin(35)),
        135,
        240,
        reset=Pin(38, Pin.OUT),
        cs=Pin(34, Pin.OUT),
        dc=Pin(37, Pin.OUT),
        backlight=Pin(33, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)