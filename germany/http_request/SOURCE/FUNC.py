# #################################################################
#     Terminal Connect Python application                         #
#     Functions                                                   #
#     Last modification:    24.05.2011                            #
#     Copyright 2010,2011                      © Triptec Service  #
#                                                                 #
# #################################################################

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


import MDM2
import MOD
import SER
import GPIO

# set PIN and check login -------------------------------------
def checkCon(pin):
    #print '\r\ncheckCon PIN:',pin
    res = MDM2.send('AT+CREG?\r',0)
    res = MDM2.receive(30)
    if (res.find('0,1') > -1):
        return 1

    ret = ''
    ret = setPin(pin)
    if ( ret != 1 ):
        GPIO.setIOdir(19,1,1)
        return -1 

    timer = MOD.secCounter() + 120
    while ((res.find('0,1') == -1)):
        res = MDM2.send('AT+CREG?\r',0)
        res = MDM2.receive(20)
        if ( MOD.secCounter() > timer ):
            return -1
        MOD.sleep(50)
    MOD.sleep(20)
    return 1 

def setPin(pin):
    rr = ''
    tt = MOD.secCounter() + 30
    while ( rr.find('READY') == -1):
        rr = MDM2.send('AT+CPIN?\r',0)                   # CPIN Status
        rr = MDM2.receive(5)
        if ( rr.find('SIM PIN') != -1 ):
            bb = MDM2.send('AT+CPIN=' + pin + '\r',0)    # set PIN
            MOD.sleep(10)                                # wait 1sec
        if ( MOD.secCounter() > tt ):
            return -1 
        MOD.sleep(10)
    return 1

# read GPIO ---------------------------------------------
def setGPIO(id,d):
    a = GPIO.setIOdir(id,1,d)
    return a

# toggle GPIO -------------------------------------------
def toggleGPIO(id,z_on,z_off,anz):
    ra = ''
    while anz > 0:
        ra = GPIO.setIOdir(id,1,1)
        MOD.sleep(z_on)
        ra = GPIO.setIOdir(id,0,1)
        MOD.sleep(z_off)
        # flash continusly
        if ( anz != 99 ):
            anz = anz - 1
    return ra


# POST ------------------------------------------------------
def sendData(PIN,PO,HO,A,GU,GP,data,ll):
    a = openGPRS(PIN,A,GU,GP)
    a = openSD(HO)
    res = MDM2.send('POST /' + PO + ' HTTP/1.1 Connection: close\r\n', 0)
    res = MDM2.send('HOST: ' + HO + '\r\n', 0)
    res = MDM2.send('User-Agent: Terminal Connect\r\n', 0)
    res = MDM2.send('Content-Type: application/x-www-form-urlencoded\r\n', 0)
    res = MDM2.send('Content-Length: '+ str(ll) +'\r\n\r\n', 0)
    res = MDM2.send(data, 0)
    res = MDM2.send('\r\n\r\n', 0)
    cnt = 20
    res = MDM2.receive(20)
    a = SER.send('\r\nresponse from server ------------------------\r\n')
    while ( (res.find('EOT') == -1) and (cnt > 0) ):
        a = SER.send(res)
        res = MDM2.receive(20)
        cnt = cnt - 1
    a = SER.send(res)
    res = closeCon()
    a = SER.send('\r\nend -----------------------------------------\r\n')
    return res

def openGPRS(P,A,GU,GP): #PIN = CONFIG.config['PIN_SIM'],H = CONFIG.config['HOST'],A = CONFIG.config['APN']
    ret = checkCon(P)
    if ( ret != 1 ):
        return -1
    res = MDM2.send('AT#SGACT?\r', 2)
    timer = MOD.secCounter() + 20
    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if ((res.find(',0') >= 0) ):
            timer = timer - 100
        if ((res.find(',1') >= 0) ):
            timer = timer - 100
            #print 'GPRS stil active\r'
            return 1
        MOD.sleep(10)

    res = MDM2.send('AT+CGDCONT=1,"IP","' + A + '","0.0.0.0",1,1\r', 0)
    timer = MOD.secCounter() + 30
    # check answer CGDCONT
    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if ((res.find('OK') >= 0) ):
            timer = timer - 100
        MOD.sleep(10)

    if (GU != ''):
        print 'set GPRS username\r'
        res = MDM2.send('AT#USERID="'+ GU + '"\r', 2)
        res = MDM2.receive(20)
        res = res.find ('OK')
        if (res == -1):
            a = SER.send('\r\nerror setting GPRS username\r')    

    if (GP != ''):
        print 'set GPRS password\r'
        res = MDM2.send('AT#PASSW="'+ GP + '"\r', 2)
        res = MDM2.receive(20)
        res = res.find ('OK')
        if (res == -1):
            a = SER.send('\r\nerror setting GPRS password\r') 


    res = MDM2.send('AT#SGACT=1,1\r', 1)
    timer = MOD.secCounter() + 50

    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if (res.find('#SGACT:') >= 0):
            timer = timer - 100
            res = cleanCRLF(res)
            res = res.replace('#SGACT:','')
            res = res.replace('OK','')
            a = SER.send('\r\nConnected with IP:' + str(res))
            return 1
        MOD.sleep(10)
    return -1

def openSD(H):
    res = MDM2.send('AT#SD=1,0,80,' + H +',0\r', 0)
    timer = MOD.secCounter() + 30
    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if ((res.find('CONNECT') >= 0) ):
            timer = timer - 100
            return 1
        MOD.sleep(10)
    return -1

def closeCon():
    res = MDM2.send('+++\r', 10)
    timer = MOD.secCounter() + 30
    # Antwort +++ auswerten
    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if ((res.find('OK') >= 0) ):
            timer = timer - 100
        MOD.sleep(10)

    res = MDM2.send('AT#SH=1\r', 0)
    timer = MOD.secCounter() + 30
    # answere AT#SD
    while (MOD.secCounter() < timer):
        res = MDM2.receive(10)
        if ((res.find('OK') >= 0) ):
            timer = timer - 100
        MOD.sleep(10)
    # print '\r\ncloseCon =',res
    return res

def cleanCRLF(s):
	s = s.replace('\r','')
	s = s.replace('\n','')
	return s

