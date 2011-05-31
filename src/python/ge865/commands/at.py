import re

import logging
logger = logging.getLogger(__name__)

from core import Command, ATCommand, Response
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
  cmd = 'I'
  """Identification information"""

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
