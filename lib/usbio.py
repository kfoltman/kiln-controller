import glob
import os
import time

useGPIO = False

usbport = None
usbbuf = ""

def init():
    global usbport
    global usbbuf
    dev = glob.glob("/dev/ttyACM*")[0]
    usbport = os.open(dev, os.O_RDWR)
    os.write(usbport, b"r")
    time.sleep(1)
    os.set_blocking(usbport, False)
    try:
        while os.read(usbport, 1):
            pass
    except BlockingIOError:
        pass
    os.set_blocking(usbport, True)
    usbbuf = ""

def measure():
    global usbbuf
    os.write(usbport, b"?")
    while True:
        ch = os.read(usbport, 1)
        if ch == b'\r' or ch == b'\n':
            data = usbbuf
            usbbuf = ''
            if data and '.' not in data:
                return int(data, 16)
            continue
        usbbuf += ch.decode('utf-8')

def heat():
    os.write(usbport, b"0")

def cool():
    os.write(usbport, b"1")

def cleanup():
    usbport.close()
