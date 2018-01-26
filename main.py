#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import qrcode
import pifacecad
import os
import signal
import sys
import requests
import json
import time

cad = pifacecad.PiFaceCAD()

user_email = ""
user_session_key = ""
listener = pifacecad.SwitchEventListener(chip=cad)

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
    global user_email
    global user_session_key
    global listener
    cad.lcd.clear()
    cad.lcd.write("Searching QR Code")
    print "Searching QR Code"
    result=qrcode.read().strip()
    presented = False
    if (event.pin_num == 2):
        presented = True

    sendAttendance(result,presented)

def sendAttendance(qrResult, presented):
    global user_email
    global user_session_key
    global listener
    results = qrResult.split(":")
    stu_email = results[0]
    stu_group_number = results[2]
    stu_week_id = results[4]

    attendance = "{\"attendance_id\":\"" + qrResult +"\",\"student_id\":\"" + stu_email + "\",\"tutorial_id\":\"" + stu_group_number + "\",\"week_id\":\"" + stu_week_id + "\",\"presented\":\"" + str(presented) +"\"}"
    print qrResult
    print attendance    
    cad.lcd.clear()
    cad.lcd.write("Sending Attendance to Server")
    print "Sending Attendance to Server"
    url = "http://ase2017-group6-4.appspot.com/rest/attendance/lecturer/" + user_email + "/session/" + user_session_key
    response = requests.put(url, data=attendance)
    if (response.status_code==200):
        cad.lcd.clear()
        cad.lcd.write("Success @ Attendance")
        print "Success @ Attendance"
    else:
        cad.lcd.clear()
        cad.lcd.write("Failure @ Attendance")
        print "Failure @ Attendance"

    time.sleep(1)    
    cad.lcd.clear()
    cad.lcd.write("1. Scan without presentation 2. Scan with presentation 3. Logout")
    print "1. Scan without presentation 2. Scan with presentation 3. Logout"

def logout(event):
    global user_email
    global user_session_key
    global listener
    url = "http://ase2017-group6-4.appspot.com/rest/authentication/logout"
    print user_email
    print user_session_key
    credentials = "{\"email\":\""+user_email+"\",\"sessionKey\":\""+user_session_key+"\"}"
    response = requests.post(url, data=credentials)
    
    user_email = ""
    user_session_key = ""
    cad.lcd.clear()
    cad.lcd.write("Logged out")
    print "Logged out"

    time.sleep(1)

    cad.lcd.clear()
    cad.lcd.write("Press 0 for Login")
    print "Press 0 for Login"

def login(event):
    global user_email
    global user_session_key
    global listener
    cad.lcd.clear()
    cad.lcd.write("Logging in")
    print "Logging in"
    url = "http://ase2017-group6-4.appspot.com/rest/authentication/login"
    credentials = "{\"email\":\""+"saahil@tum.de"+"\",\"password\":\""+"saahil"+"\"}"
    print credentials
    response = requests.post(url, data=credentials)
    if (response.status_code==200):
        response_json = response.json()
        user_email = response_json['email']
        user_session_key = response_json['sessionKey']
        cad.lcd.clear()
        cad.lcd.write("Logged in")
        print "Logged in"

        cad.lcd.clear()
        cad.lcd.write("1. Scan + 2. Scan - 3. Logout")
        print "1. Scan without presentation 2. Scan with presentation 3. Logout"
    else:
        cad.lcd.clear()
        cad.lcd.write("Access denied.")
        print "Access denied."
        time.sleep(1)
        cad.lcd.clear()
        cad.lcd.write("Press 0 for Login")
        print "Press 0 for Login"
    


cad.lcd.write("Press 0 for Login")
print "Press 0 for Login"

listener.register(0, pifacecad.IODIR_FALLING_EDGE, login)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, read_qrcode)
listener.register(2, pifacecad.IODIR_FALLING_EDGE, read_qrcode)
listener.register(3, pifacecad.IODIR_FALLING_EDGE, logout)  
listener.activate()



