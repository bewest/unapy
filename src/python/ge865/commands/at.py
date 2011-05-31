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


    >>> str(CMUX.assign(mode=0, subset=0).format())
    'AT+CMUX=0,0\\r'
  
  """
  class assign(NullSettable):
    tail = '{mode},{subset}'
    

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
