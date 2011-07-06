############################################
#   gauge4free WS2300 Python application   #
#     Copyright 2008, © Round Solutions    #
#                                          # 
############################################

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
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS``AS
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

#version 20080128.1

import MAIN
import LOCALS

# Change values below

# GPRS APN settings
# incorrect values lead to imposibility to use GPRS  
apn = 'internet'
gprs_userid = ''
gprs_passw = ''

# gauge4free password
g4f_passw = 'demo'

# Interval between data upload to server
# in 1/10 of second
interval = 18000

# WS2300 driver
# how many times a command will be retried before declare fail
LOCALS.maxtrials = 30
# receive timeout when reading from WS2300
LOCALS.receive_timeout = 3

'''
Debug level is in LOCALS.debug_level
if bit 2 is set print driver level messages
if bit 1 is set print low level applications messages
if bit 0 is set print high level applications messages
'''
LOCALS.debug_level = 3

# !!! Do not change anything from here !!!
LOCALS.cgdcont = apn
LOCALS.gprsuserid = gprs_userid
LOCALS.gprspassw = gprs_passw 

LOCALS.g4fpassw = g4f_passw
 
LOCALS.interval = interval

MAIN.main()
