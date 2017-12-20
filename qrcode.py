#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Read QR-Codes
'''
import os, signal, subprocess
    
def read():
    zbarcam=subprocess.Popen("zbarcam --raw --nodisplay /dev/video0", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print "zbarcam started"
    
    while True:
        qrcodetext=zbarcam.stdout.readline()
        if qrcodetext!="":
            break
        
    os.killpg(zbarcam.pid, signal.SIGTERM)  # Prozess stoppen
    print "zbarcam stopped"
    return qrcodetext


