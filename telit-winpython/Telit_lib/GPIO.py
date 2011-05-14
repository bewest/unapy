#Telit Extensions
#
#Copyright 2004, DAI Telecom S.p.A.
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


TIMEOUT_CMD = 20

def setIOvalue(GPIOnumber, value):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT#GPIO=',0)
    MDM.mdmser.send(str(GPIOnumber),0)
    MDM.mdmser.send(',',0)
    MDM.mdmser.send(str(value),0)
    MDM.mdmser.send(',1\r',0)

    timer = time.time() + TIMEOUT_CMD
    resp = MDM.mdmser.read()
    while((resp.find('OK') == -1) and (resp.find('ERROR') == -1) and (time.time() < timer)):
      #time.sleep(0.1)
      resp = resp + MDM.mdmser.read()

    if resp.find('ERROR') != -1:
      return -1
    else:
      return  1
  else:
    print 'dummy setIOvalue(', GPIOnumber, value, ')'
    return -1

def getIOvalue(GPIOnumber):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT#GPIO=',0)
    MDM.mdmser.send(str(GPIOnumber),0)
    MDM.mdmser.send(',2\r',0)
    timer = time.time() + TIMEOUT_CMD
    resp = MDM.mdmser.read()
    while((resp.find('OK') == -1) and (resp.find('ERROR') == -1) and (time.time() < timer)):
      #time.sleep(0.1)
      resp = resp + MDM.mdmser.read()

    if resp.find('ERROR') != -1:
      result = -1
    else:
      commapos = resp.find(',')
      stat = resp[commapos+1]
      result = int(stat)
  else:
    print 'dummy getIOvalue(', GPIOnumber, ')'
    result = -1
  return result

def setIOdir(GPIOnumber, value, dir):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT#GPIO=',0)
    MDM.mdmser.send(str(GPIOnumber),0)
    MDM.mdmser.send(',',0)
    MDM.mdmser.send(str(value),0)
    MDM.mdmser.send(',',0)
    MDM.mdmser.send(str(dir),0)
    MDM.mdmser.send('\r',0)

    timer = time.time() + TIMEOUT_CMD
    resp = MDM.mdmser.read()
    while((resp.find('OK') == -1) and (resp.find('ERROR') == -1) and (time.time() < timer)):
      #time.sleep(0.1)
      resp = resp + MDM.mdmser.read()

    if resp.find('ERROR') != -1:
      return -1
    else:
      return 1
  else:
    print 'dummy setIOdir(', GPIOnumber, value, dir, ')'
    return -1

def getIOdir(GPIOnumber):
  global MDM
  if MDM.mdmser.getDCD() == 0:
    MDM.mdmser.send('AT#GPIO=',0)
    MDM.mdmser.send(str(GPIOnumber),0)
    MDM.mdmser.send(',2\r',0)

    timer = time.time() + TIMEOUT_CMD  
    resp = MDM.mdmser.read()
    while((resp.find('OK') == -1) and (resp.find('ERROR') == -1) and (time.time() < timer)):
      #time.sleep(0.1)
      resp = resp + MDM.mdmser.read()

    if resp.find('ERROR') != -1:
      return -1
    else:
      commapos = resp.find(',')
      stat = resp[commapos-1]
      result = int(stat)
  else:
    print 'dummy getIOdir(', GPIOnumber, ')'
    result = -1
  return result
