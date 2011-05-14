#! python
#
# Telit Extensions
#
# Copyright 2006-2007, Telit Communications S.p.A.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without 
#modification, are permitted provided that the following conditions 
#are met:
#
#Redistributions of source code must retain the above copyright notice, 
#this list of conditions and the following disclaimer.
#
#Redistributions in binary form must reproduce the above copyright 
#notice, this list of conditions and the following disclaimer in 
#the documentation and/or other materials provided with the distribution.
#
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
#IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import time
import win32ui
import win32con
import serialwin32

retry = 1
while retry > 0: 
  try:
    mdmser = serialwin32.Serial('COM1', 115200, timeout=10, rtscts=1)
    retry = 0
  except :
    ans = win32ui.MessageBox("The COM port is Busy! Please Verify that it's not used by another application and retry \r\nRetry?", "WARNING!",win32con.MB_YESNO)
    if ans == win32con.IDYES:
      retry = 1
    else:
      retry = 0
      raise StandardError, 'ERROR opening the COM port.!'
  

retry = 1
while retry > 0: 

  i = 3
  while i > 0:
    i = i -1
    if mdmser.getCTS() <> 0:
      i = -1
    else:
      time.sleep(0.1)

  if i == 0:
    ans = win32ui.MessageBox("The module seems not connected! Please Verify that it's connected and Turned ON\r\nDo you want to retry to communicate?", "WARNING!",win32con.MB_YESNO)
    if ans == win32con.IDYES:
      retry = 1
    else:
      retry = 0
      mdmser.close()
      del mdmser
      raise StandardError, 'ERROR: The module seems not connected!'
      #  print "...Proceeding anyway without Hardware Flow Control.."
      #  mdmser.close()
      #  del mdmser
      #  mdmser = serial.Serial('COM1', 115200, timeout=0, rtscts=0)
    
  else:
    retry = 0  

retry = 1
while retry > 0: 

    mdmser.send('ATE0\r',2)
    timer = time.time() + 2
    res = mdmser.read()
    while((res == '') and (time.time() < timer)):
      res = res + mdmser.read()

    # try again....
    mdmser.send('ATE0\r',2)
    timer = time.time() + 2
    res = mdmser.read()
    while((res == '') and (time.time() < timer)):
      res = res + mdmser.read()
      
    if res == "":
      ans = win32ui.MessageBox("The module is not responding!\r\nDo you want to retry to communicate?", "WARNING!",win32con.MB_YESNO)
      if ans == win32con.IDYES:
        retry = 1
      else:
        retry = 0
        mdmser.close()
        del mdmser
        raise StandardError, 'ERROR: The module is not responding!'
    else:
      retry = 0
      mdmser.flushInput()


def send(string, timeout):
  global mdmser
  return mdmser.send(string,timeout)

def receive(timeout):
  global mdmser
  return mdmser.receive(timeout)

def read():
  global mdmser
  return mdmser.read()

def sendbyte(byte, timeout):
  global mdmser
  string = chr(byte)
  return mdmser.sendbyte(string,timeout)

def receivebyte(timeout):
  global mdmser
  return mdmser.receivebyte(timeout)

def readbyte():
  global mdmser
  return mdmser.readbyte()

def getDCD():
  global mdmser
  return mdmser.getDCD()

def getCTS():
  global mdmser
  return mdmser.getCTS()

def getDSR():
  global mdmser
  return mdmser.getDSR()

def getRI():
  global mdmser
  return mdmser.getRI()

def setRTS(rts):
  print 'warning - not emulable feature on Pc'
  return

def setDTR(dtr):
  global mdmser
  mdmser.setDTR(dtr)
  return
