# #################################################################
#     Terminal Connect Python application                         #
#     Configurations                                              #
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

# create dict
config = {}

# GPIO of your status LED
statLED = 19


def initConfig():
    global config
    # configuration file and save parameter into "config"
    liste = []
    f = open('konfig.dat','r')
    inh = f.read()
    f.close()

    tmpArr = inh.split('|')
    for x in tmpArr:
        if ( (x.find('#') != -1) or (len(x) < 5) ):
            continue
        liste.append(x)

    for x in liste:
        x = x.replace('\'','')
        tmpArr = x.split('=')
        k = tmpArr[0].strip()
        v = tmpArr[1].strip()
        if ( v.find('[') != -1 ):
            v = v.replace('[','')
            v = v.replace(']','')
            vArr = v.split(',')
            config[k] = vArr
        else:
            config[k] = v
    return 1


# read configuration ------------------------------------------
def readConfig():
    o = ''
    ck = config.keys()
    for x in ck:
        o = o + '|' + str(x) + '=' + str(config[x])
    return o

# write configuration -----------------------------------------
def writeConfig():
    rr = readConfig()
    f = open('konfig.dat','wb')
    f.write(rr)
    f.close()
    return

# update configuration ----------------------------------------
def updateConfig():
    rr = readConfig()
    f = open('konfig.dat','wb')
    f.write(rr)
    f.close()
    listTel()
    return

