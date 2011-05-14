#Telit Extensions
#
#Copyright 2006-2007, Telit Communications S.p.A.
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
import MDM

def powerOnOff(status):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSP=',2)
    MDM.mdmser.send(str(status),2)
    MDM.mdmser.send('\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      result = 1
    else:
      result = -1
  else:
    print 'dummy powerOnOff(', status, ')'
    result = -1
  return

def getPowerOnOff():
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSP?\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      colonPos = data.find(':')
      status = data[colonPos+2]
      result = int(status)
    else:
      result = -1
  else:
    print 'dummy getPowerOnOff()'
    result = -1
  return result

def resetMode(mode):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSR=',2)
    MDM.mdmser.send(str(mode),2)
    MDM.mdmser.send('\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      result = 1
    else:
      result = -1
  else:
    print 'dummy resetMode(', mode, ')'
    result = -1
  return result

def getAntennaVoltage():
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSAV?\r',2)
    data = ''
    timeMax = time.time() + 8.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      colonPos = data.find(':')
      mVolt = data[colonPos+2 : ]
      CRpos = mVolt.find('\r')
      mVolt = mVolt[ : CRpos]
      result = int(mVolt)
    else:
      result = -1
  else:
    print 'dummy getAntennaVoltage()'
    result = 3520
  return result

def getAntennaCurrent():
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSAI?\r',2)
    data = ''
    timeMax = time.time() + 8.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      colonPos = data.find(':')
      mAmp = data[colonPos+2 : ]
      CRpos = mAmp.find('\r')
      mAmp = mAmp[ : CRpos]
      result = int(mAmp)
    else:
      result = -1
  else:
    print 'dummy getAntennaCurrent()'
    result = 31
  return result

def getActualPosition():
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSACP\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
      OKPos = data.find('OK\r')
      ERRORPos = data.find('ERROR\r')
    if data.find('OK\r') != -1:
      GPSACPPos = data.find('GPSACP:')
      data = data[GPSACPPos+8 : ]
      CRPos = data.find('\r')
      result = data[ : CRPos+1]
    else:
      result = ''
  else:
    print 'dummy getActualPosition()'
    result = '151956.999,4542.8100N,01344.2665E,1.4,207.5,3,11.78,0.46,0.25,141206,05'
  return result

def powerSavingMode(mode, pushToFixPeriod):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSPS=',2)
    MDM.mdmser.send(str(mode),2)
    MDM.mdmser.send(',',2)
    MDM.mdmser.send(str(pushToFixPeriod),2)
    MDM.mdmser.send('\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      result = 1
    else:
      result = -1
  else:
    print 'dummy powerSavingMode(', mode, pushToFixPeriod, ')'
    result = -1
  return result

def powerSavingWakeUp():
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT$GPSWK\r',2)
    data = ''
    timeMax = time.time() + 5.0
    data = data +  MDM.mdmser.read()
    while data.find('OK\r') == -1 and data.find('ERROR\r') == -1 and time.time() < timeMax:
      data = data +  MDM.mdmser.read()
    if data.find('OK\r') != -1:
      result = 1
    else:
      result = -1
  else:
    print 'dummy powerSavingWakeUp()'
    result = -1
  return result

def getLastGGA():
  print 'dummy getLastGGA()'
  return '$GPGGA,151956.999,4542.8100,N,01344.2665,E,1,05,1.4,207.5,M,45.2,M,,0000*52\r'

def getLastGLL():
  print 'dummy getLastGLL()'
  return '$GPGLL,4542.8100,N,01344.2665,E,151956.999,A,A*54\r'

def getLastGSA():
  print 'dummy getLastGSA()'
  return '$GPGSA,A,3,03,19,18,22,16,,,,,,,,,1.4,*32\r'

def getLastGSV():
  print 'dummy getLastGSV()'
  return '$GPGSV,3,1,10,03,82,274,28,19,50,303,36,18,44,058,26,22,65,120,21*73\r$GPGSV,3,2,10,21,20,069,20,16,30,193,31,26,04,021,14,08,04,321,23*73\r$GPGSV,3,3,10,07,09,124,00,11,01,264,13*72\r'

def getLastRMC():
  print 'dummy getLastRMC()'
  return '$GPRMC,151957.999,A,4542.8100,N,01344.2666,E,0.19,23.59,141206,,,A*54\r'

def getLastVTG():
  print 'dummy getLastVTG()'
  return '$GPVTG,23.59,T,,M,0.19,N,0.36,K,A*0D\r'

def getPosition():
  print 'dummy getPosition()'
  return (457134155, 'N', 137378358, 'E')

