import logging
import serial
import time
from pprint import pprint, pformat

logger = logging.getLogger(__name__)

import util

class Link(serial.Serial, util.Loggable):
  __port__ = None
  __name__ = None
  def __init__(self, name = None):
    self.__name__ = name
    self.__port__ = super(type(self), self).__init__(name, timeout=2)
    self.getLog()
    self.log.debug('created device: %r' % self)

  def dump_port_settings(self):
    info = [ "Settings: %s  %s,%s,%s,%s\n" % (
                        self.portstr, self.baudrate,
                        self.bytesize, self.parity,
                        self.stopbits, ),
      'software flow control %s\n' % (self.xonxoff and 'active' or 'inactive'),
      'hardware flow control %s\n' % (self.rtscts and 'active' or 'inactive'),
    ]

    try:
      if self.isOpen():
        info.append('CTS: %s  DSR: %s  RI: %s  CD: %s\n' % (
            ((self.isOpen() and self.getCTS()) and 'active' or 'inactive'),
            (self.getDSR() and 'active' or 'inactive'),
            (self.getRI() and 'active' or 'inactive'),
            (self.getCD() and 'active' or 'inactive'),
            ))
    except serial.portNotOpenError:
      info.append("port is not open")

    except serial.SerialException:
        # on RFC 2217 ports it can happen to no modem state notification was
        # yet received. ignore this error.
        pass
    return "\n".join(info)

  def __repr__(self):
    return self.dump_port_settings()


  def process(self, command):
    """
      Synchronously process a single command.
    """
    message = command.format()
    self.log.info('process.read: %r' % message)
    self.write(message)
    self.log.info('reading...')
    response = ''.join(self.readlines())
    self.log.info('process.respnse: %r' % response)
    result = command.parse(response)
    self.log.info('process.parse.result: %r' % result)
    return command

EXAMPLE_RESPONSE = "AT\r\r\nOK\r\n"

class Response(object):
  """
  Basic Response to the AT commands

  >>> Response('AT\\r\\r\\nOK\\r\\n').isOK()
  True

  """
  def __init__(self, raw):
    self.raw = raw
    self.lines = raw.splitlines()

  def isOK(self):
    if 'OK' == self.lines[-1]:
      return True
    return False

  def getError(self):
    if not self.isOK():
      return self.lines[-1]

  def getData(self):
    if self.isOK():
      lines = list(self.lines)
      lines.pop()
      return "\n".join(lines)
    return None

  def __repr__(self):
    comps = [ str(type(self)),
              "   str: %s" % self.raw,
              "  isOK: %s" % self.isOK(),
              "length: %s" % len(self.getData()) ]
    return '\n'.join(comps)

class Command(object):
  """
    Your basic AT command.

    >>> Response("AT\\r\\r\\nOK\\r\\n").isOK()
    True

    >>> c = Command()
    ... c.parse("AT\\r\\r\\nOK\\r\\n")
    ... assert(c.response != None)
  """

  __raw__      = None
  __timeout__  = None
  response     = None

  class __Response__(Response): pass
  
  def __init__(self):
    self.response = None

  
  def format(self):
    return bytearray("AT\r")

  def parse(self, raw):
    self.__raw__  = raw
    self.response = self.__Response__(self.__raw__)
    return self.response
    
  def __repr__(self):
    comp = [ str(type(self)), '  msg: %s' % self.format(),
             '  response: %r' % self.response ]
    return '\n'.join(comp)


def test(name):
  logger.info("hello world %s" % __name__)
  d = Link('/dev/ttyUSB0')
  logger.debug("%s" % d)
  d = Link('/dev/ttyUSB0')
  logger.debug("%r" % d)
  if not d.isOpen():
    d.open()
  command = d.process(Command())
  print "%r" % command
  command = d.process(command)
  print "%r" % command
  command = d.process(Command())
  print "%r" % command


if __name__ == '__main__':
  import doctest
  doctest.testmod()



#####
# EOF
