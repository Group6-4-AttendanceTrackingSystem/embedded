#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import qrcode
import pifacecad
import os
import signal
import sys
import requests

cad = pifacecad.PiFaceCAD()

# you can ignore these three lines of code
# they are needed so that you can end the
# program by pressing Ctrl+C
def signal_handler(signal, frame):
    if sys.version_info < (3,0): 
        # the python2 code forks
        os.kill(os.getppid(),9)
    os.kill(os.getpid(),9)
signal.signal(signal.SIGINT, signal_handler)

# event handler that is called after a button is
# pressed. The event handler is linked to the
# button press by listener.register(...) below
def read_qrcode(event):
    cad.lcd.clear()
    cad.lcd.write("Searching QR Code")
    print "Searching QR Code"
    result=qrcode.lesen().strip()
    cad.lcd.clear()
    cad.lcd.write("Sending Attendance to Server")
    print "Sending Attendance to Server"
    url = "http://ase2017-group6-4.appspot.com/attendance/"
    response = requests.put(url, data=result)
    if (response.status_code==200):
        cad.lcd.clear()
        cad.lcd.write("Success")
	print "Success"
    else:
        cad.lcd.clear()
        cad.lcd.write("Failure")
	print "Failure"
    

cad = pifacecad.PiFaceCAD()
cad.lcd.write("Application Started")
print "Application Started"
listener = pifacecad.SwitchEventListener(chip=cad)


listener.register(0, pifacecad.IODIR_FALLING_EDGE, read_qrcode)
# listener.register(1, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
listener.activate()
