import re

import logging
logger = logging.getLogger(__name__)

from core import Command, ATCommand, Response, NullSettable, NullQueryable
from core import IdentCommand, WellDefinedCommand, MetaCommand
 
"""
3gpp commands

"""

"""
Generic Modem Control
~~~~~~~~~~~~~~~~~~~~~
"""
class GCAP(ATCommand):
  """List device capabilities."""
  cmd = 'GCAP'


class CMEE(WellDefinedCommand):
  """Set/read extended error reporting."""


class X(ATCommand):
  """Extended result codes. pg 53"""
  sep = ''
  cmd = 'X'

class I(IdentCommand):
  """Identification information"""
  cmd = 'I'

class C(IdentCommand):
  """Data Carrier Detect
  """
  sep = '&'
  cmd = 'C'

class D(IdentCommand):
  """Dial"""
  sep = ''
  cmd = 'D'
  tail = '{0}'

class H(ATCommand):
  """Hangup."""
  cmd = 'D'
  sep = ''

class CGMI(WellDefinedCommand):
  """Manufacturer Information."""

class CGMM(WellDefinedCommand):
  """Manufacturer ID Code."""

class CGMR(WellDefinedCommand):
  """Manufacturer Revision ID."""

class CGSN(WellDefinedCommand):
  """Product Serial No."""

class CIMI(WellDefinedCommand):
  """Request internal mobile subscriber number on SIM."""

class CMUX(WellDefinedCommand):
  """Multiplexing Mode

  Set command is used to enable/disable the 3GPP TS 27.010 multiplexing
  protocol control channel.
  AT+CMUX= <mode> [,<subset>]
  Parameters:

    * <mode> multiplexer transparency mechanism
      0 - basic option; it is currently the only supported value.

    * <subset>
      0 - UIH frames used only; it is currently the only supported value.
  Note: after entering the Multiplexed Mode an inactive timer of five seconds
  starts. If no CMUX control channel is established before this inactivity
  timer
  expires the engine returns to AT Command Mode
  Note: all the CMUX protocol parameter are fixed as defined in GSM07.10
  and cannot be changed.
  AT+CMUX?
  AT+CMUX=?
  Reference
  3.5.4.1.8.
  Note: the maximum frame size is fixed: N1=128
  Read command returns the current value of <mode> and <subset>
  parameters, in the format:
  +CMUX: <mode>,<subset>
  Test command returns t


    >>> str(CMUX.assign(0, 0).format())
    'AT+CMUX=0, 0\\r'
  
  """
  #class assign(NullSettable):
    #tail = '{mode},{subset}'
    
class CHUP(WellDefinedCommand):
  "Hangup call"

class CBST(WellDefinedCommand):
  """Select Bearer Service Type."""
  class assign(NullSettable):
    tail = '{speed}, {name}, {ce}'

class CRLP(WellDefinedCommand):
  """Radio Link Protocol"""
  class assign(NullSettable):
    tail = '{iws}, {mws}, {t1}, {n2}, {ver}'


class CR(WellDefinedCommand):
  """Service reporting control

  >>> str(CR.assign(1).format())
  'AT+CR=1\\r'
  """

class CRC(WellDefinedCommand):
  """Cellular result codes."""

class CSNS(WellDefinedCommand):
  """Single numbering scheme."""

class CVHU(WellDefinedCommand):
 """Sets whether ATH and drop DTR causes voice disconnect."""

class CNUM(WellDefinedCommand):
  """Get MSISDN (phone number.
  
   see also: .. py:`ENS`
  """

class COPN(WellDefinedCommand):
  """Read operator names."""

class CREG(WellDefinedCommand):
  """Network registration report.
  """

class CPIN(WellDefinedCommand):
  """sim/ready pin report.
  """

class COPS(WellDefinedCommand):
  """Operator Selection.
    >>> str(COPS.assign(1, 1, 2).format())
    'AT+COPS=1, 1, 2\\r'

  """

class CLCK(WellDefinedCommand):
  """Facility lock/unlock.
  """
  class assign(NullSettable):
    tail = '{fac}, {mode}, {passwd} {class}'

class CPWD(WellDefinedCommand):
  """change facility password.
  """
  class assign(NullSettable):
    tail = '{fac}, {oldpasswd}, {newpasswd}'

class CLIP(WellDefinedCommand):
  """Enable/disable calling line identity."""

class CLIR(WellDefinedCommand):
  """calling line identity restriction management. pg 113."""

class CLCC(WellDefinedCommand):
  """list current calls."""

class CSSN(WellDefinedCommand):
  """ss notification.
    >>> str(CSSN.assign(1,2).format())
    'AT+CSSN=1, 2\\r'
  """
  class assign(NullSettable):
    tail = '{0}, {1}'

class CPOL(WellDefinedCommand):
  """Preferred Operator List."""
  class assign(NullSettable):
    tail = '{0}, {1}, {2]'

class CPAS(WellDefinedCommand):
  """Phone activity status."""

class CFUN(WellDefinedCommand):
  """Set phone functionality."""

class CIND(WellDefinedCommand):
  """Indicator control."""

class CMER(WellDefinedCommand):
  """mobile equipment event reporting."""


"""
IP Easy Operations
"""
class CGDCONT(WellDefinedCommand):
  """Set up PDP context.

  At minimum requires args:
    * cid
    * PDP type "IP" or "PPP"
    * APN
    * PDP_addr - requested IP
    * d_comp - data compressions
    * h_comp - PDP heaer compression
  """

class CGQMIN(WellDefinedCommand):
  """Miminum quality of service.
    * cid - 1..5

    * precedence - 0..3
      * 0: subscribed
      * 1: high pri
      * 2: normal
      * 3: low pri

    * delay - max delay: 0..4
      * 0: subscribed (default)
      * 1: delay class 1
      * 2: delay class 2
      * 3: delay class 3
      * 4: delay class 4

    * reliability - 0..5
      * 0: subscribed
      * 1: reliability 1 (acknowledged GTP, LLC, RLC; protected data )
      * 2: reliability 2 (unacknowledged GTP, acked LLC and RLC; protected
           data )
      * 3: reliability 3 (unacknowledged GTP and LLC, acked RLC; protected data )
      * 4: reliability 4 (unacked GTP, LLC, and RLC; protected data )
      * 5: reliability 5 (unacked GTP, LLC, and RLC; unprotected data )

    * peak -  0..9 (7.8 - 2000kbps
      * 0: subscribed
    * mean - 0..31

    Telit suggests:
    AT+CGQMIN=1,0,0,3,0,0

  """

class CGREQ(WellDefinedCommand):
  """ Request quality of service
    * cid
    * precedence
    * delay
    * reliability
    * peak
    * mean

  """

class CGEQMIN(WellDefinedCommand):
  """ Request minimum quality of service
    * cid
    * traffic class - type of app:
      * 0: conversational
      * 1: streaming
      * 2: interactive
      * 3: background
      * 4: subscribed (default)
    * maxmimum bitrate UL([0] 1..512 max kbit/s)
    * maxmimum bitrate DL([0] 1..1600 max kbit/s)
    * guaranteed bitrate UL([0] 1..512 max kbit/s)
    * guaranteed bitrate DL([0] 1..1600 max kbit/s)
    * delivery order: UMTS bearer should privde in-sequential SDU deliveries
      * 0: no
      * 1: yes
      * 2: subscribed (default)
    * max SDU size: [0] 1.1520
    * SDU error ratio
    * residual bit error ratio
    * delivery or erroneious SUDs
      * 0: no
      * 1: yes
      * 2: no detect
      * 3: subscribed value (Default)
    * transfer delay - (ms, [0], 100..4000)
    * traffic handling priority ([0] 1..3)


  Telit suggests AT+CGEQMIN=1,4,0,0,0,0,2,0,"0E0", "0E0", 3,0,0
  """

class CGEQREQ(WellDefinedCommand):
  """ Request minimum quality of service
    * cid
    * traffic class - type of app:
      * 0: conversational
      * 1: streaming
      * 2: interactive
      * 3: background
      * 4: subscribed (default)
    * maxmimum bitrate UL([0] 1..512 max kbit/s)
    * maxmimum bitrate DL([0] 1..1600 max kbit/s)
    * guaranteed bitrate UL([0] 1..512 max kbit/s)
    * guaranteed bitrate DL([0] 1..1600 max kbit/s)
    * delivery order: UMTS bearer should privde in-sequential SDU deliveries
      * 0: no
      * 1: yes
      * 2: subscribed (default)
    * max SDU size: [0] 1.1520
    * SDU error ratio
    * residual bit error ratio
    * delivery or erroneious SUDs
      * 0: no
      * 1: yes
      * 2: no detect
      * 3: subscribed value (Default)
    * transfer delay - (ms, [0], 100..4000)
    * traffic handling priority ([0] 1..3)
  """


  Telit suggests AT+CGEQMIN=1,4,0,0,0,0,2,0,"0E0", "0E0", 3,0,0


class CGACT(WellDefinedCommand):
  """PDP Context Activate/Deactivate
    * state 0/1
    * cid x
  """

class CGPADDR(WellDefinedCommand):
  """Inspect IP address.
  """

class CGATT(WellDefinedCommand):
  """Attach GPRS"""

class SCFG(WellDefinedCommand):
  """ 
  """
  sep = '#'

"""
Enable SIM Application Toolkit
~~~~~~~~
"""

class STIA(WellDefinedCommand):
  sep = '#'

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
