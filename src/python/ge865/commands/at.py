import re

import logging
logger = logging.getLogger(__name__)

from core import Command, ATCommand, Response
from core import WellDefinedCommand, MetaCommand
 
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



if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
