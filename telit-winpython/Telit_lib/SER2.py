#! python
#
#Telit Extensions
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
    freeser2 = serialwin32.Serial('No COM', 9600, timeout=10, rtscts=0)
    retry = 0
  except :
    ans = win32ui.MessageBox("The COM port is Busy! Please Verify that it's not used by another application and retry \r\nRetry?", "WARNING!",win32con.MB_YESNO)
    if ans == win32con.IDYES:
      retry = 1
    else:
      retry = 0
      raise StandardError, 'ERROR opening the COM port.!'

def send(string):
  global freeser2
  return freeser2.send(string,0)

def receive(timeout):
  global freeser2
  return freeser2.receive(timeout)

def read():
  global freeser2
  return freeser2.read()

def sendbyte(byte):
  global freeser2
  string = chr(byte)
  return freeser2.sendbyte(string,0)

def receivebyte(timeout):
  global freeser2
  return freeser2.receivebyte(timeout)

def readbyte():
  global freeser2
  return freeser2.readbyte()

def set_speed(speed, format='8N1'):
  global freeser2
  result = 1
  if speed == '300':
    freeser2.setBaudrate(300)
  elif speed == '600':
    freeser2.setBaudrate(600)
  elif speed == '1200':
    freeser2.setBaudrate(1200)
  elif speed == '2400':
    freeser2.setBaudrate(2400)
  elif speed == '4800':
    freeser2.setBaudrate(4800)
  elif speed == '9600':
    freeser2.setBaudrate(9600)
  elif speed == '19200':
    freeser2.setBaudrate(19200)
  elif speed == '38400':
    freeser2.setBaudrate(38400)
  elif speed == '57600':
    freeser2.setBaudrate(57600)
  elif speed == '115200':
    freeser2.setBaudrate(115200)
  else:
    result = -1
  if result == 1:
    if format == '8N1':
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_NONE
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '8N2':
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_NONE
      freeser2.stopbits = serialwin32.STOPBITS_TWO
    elif format == '8E1':
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_EVEN
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '8O1':
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_ODD
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '7N1':
      freeser2.bytesize = serialwin32.SEVENBITS
      freeser2.parity = serialwin32.PARITY_NONE
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '7N2':
      freeser2.bytesize = serialwin32.SEVENBITS
      freeser2.parity = serialwin32.PARITY_NONE
      freeser2.stopbits = serialwin32.STOPBITS_TWO
    elif format == '7E1':
      freeser2.bytesize = serialwin32.SEVENBITS
      freeser2.parity = serialwin32.PARITY_EVEN
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '7O1':
      freeser2.bytesize = serialwin32.SEVENBITS
      freeser2.parity = serialwin32.PARITY_ODD
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    elif format == '8E2':
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_EVEN
      freeser2.stopbits = serialwin32.STOPBITS_TWO
    else:
      freeser2.bytesize = serialwin32.EIGHTBITS
      freeser2.parity = serialwin32.PARITY_NONE
      freeser2.stopbits = serialwin32.STOPBITS_ONE
    freeser2.applyCharFormat()
  return result



