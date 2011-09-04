import logging
logger = logging.getLogger(__name__)

import commands
from link import Link

def test(name):
  logger.info("hello world %s" % __name__)
  d = Link('/dev/ttyUSB1')
  logger.debug("%s" % d)
  d = Link('/dev/ttyUSB1')
  logger.debug("%r" % d)
  if not d.isOpen():
    d.open()
  command = commands.ATCommand()
  result = d.process(command)
  print "%r" % command

  command = commands.CMEE.query()
  result = d.process(command)
  print "%r" % command

  command = commands.CMEE.assign(2)
  result = d.process(command)
  print "%r" % command

  command = commands.CGDCONT.query()
  result = d.process(command)
  print "%r" % command

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
