# #################################################################
#     Terminal Connect Python application                         #
#     main                                                        #
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

# ################## Modules ##################
import MDM      # Use AT command interface
import MOD      # Use build in module
import SER      # Use serial
import CONFIG   # Configurations
import FUNC     # Functions

conf = CONFIG.config

# settings ---------------------------------
# 0 flow control OFF
res = MDM.send('AT&K0\r', 0) 
res = MDM.receive(10)

# Konfiguration laden ---------------------------------------------------
res = CONFIG.initConfig()

SER.set_speed(conf['COM'],'8N1')
a = SER.send('\r\n***************************************************************************')
a = SER.send('\r\n*        Start Terminal Connection - © Triptec Service                    *')
a = SER.send('\r\n***************************************************************************\r\n')
a = SER.send('\r\n- wait for connection to network ----------------\r\n')
r = FUNC.openGPRS(conf['PIN_SIM'],conf['APN'],conf['GPRS_USER'],conf['GPRS_PASS']) #openGPRS(P,A,GU,GP)
a = FUNC.setGPIO(CONFIG.statLED,1)
a = SER.send('\r\n\r\n- wait for data input ----------------\r\n')

# start Schleife --------------------------------------------------------
while 1:
    a = FUNC.setGPIO(CONFIG.statLED,0)
    MOD.sleep(10)
    a = FUNC.setGPIO(CONFIG.statLED,1)
    res = SER.read()
    if ( res != '' ):
        data = conf['PREF'] + '=' + str(res)
        lang = len(data)
        r = FUNC.sendData(conf['PIN_SIM'],conf['POST'],conf['HOST'],conf['APN'],conf['GPRS_USER'],conf['GPRS_PASS'],data,lang)
        


a = SER.send('\r\n\r\n***************************************************************************')
a = SER.send('\r\n*                             END of script                                   *')
a = SER.send('\r\n***************************************************************************\r\n')


