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

def reactivatePython():
  # simulation impossible
  return

def secCounter():
  sec = time.time()
  return int(sec)

def sleep(tenthOfSec):
  sec = int((tenthOfSec+5)/10)
  time.sleep(sec)
  return

def powerSaving(seconds):
  time.sleep(seconds)
  print 'dummy powerSaving(', seconds, ')'
  return

def powerSavingExitCause():
  print 'dummy powerSavingExitCause()'
  return 1

def watchdogEnable(seconds):
  print 'dummy watchdogEnable(', seconds, ')'
  return

def watchdogReset():
  print 'dummy watchdogReset()'
  return

def watchdogDisable():
  print 'dummy watchdogDisable()'
  return

