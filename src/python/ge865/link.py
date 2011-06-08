import logging
import serial
import time
from pprint import pprint, pformat

logger = logging.getLogger(__name__)
import util
import lib

class Link(serial.Serial, util.Loggable):
  __port__ = None
  __name__ = None
  def __init__(self, name = None):
    self.__name__ = name
    self.__port__ = super(type(self), self).__init__(name, timeout=2)
    self.getLog()
    self.log.debug('created device: %r' % self)

  def dump_port_settings(self):
    info = [ "Settings: %s  %s,%s,%s,%s" % (
                        self.portstr, self.baudrate,
                        self.bytesize, self.parity,
                        self.stopbits, ),
      ' -- software flow control %s' % (self.xonxoff and 'active' or 'inactive'),
      ' -- hardware flow control %s' % (self.rtscts and 'active' or 'inactive'),
    ]

    try:
      if self.isOpen():
        info.append(' -- CTS: %s  DSR: %s  RI: %s  CD: %s' % (
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

  def write( self, string ):
    r = super(type(self), self).write( string )
    io.info( 'link.write: %s\n%s' % ( len( string ),
                                         lib.hexdump( bytearray( string ) ) ) )
    return r

  def read( self, c ):
    r = super(type(self), self).read( c )
    io.info( 'link.read: %s\n%s' % ( len( r ),
                                        lib.hexdump( bytearray( r ) ) ) )
    return r
    
  def readline( self ):
    r = super(type(self), self).readline( )
    io.info( 'link.read: %s\n%s' % ( len( r ),
                                        lib.hexdump( bytearray( r ) ) ) )
    return r
      
  def readlines( self ):
    r = super(type(self), self).readlines( )
    io.info( 'link.read: %s\n%s' % ( len( r ),
                                        lib.hexdump( bytearray( ''.join( r ) ) ) ) )
    return r

  def process(self, command):
    """
      Synchronously process a single command.
    """
    # format the command
    message = command.format()
    self.log.info('process.write: %r' % message)

    # write it into the port
    self.write(message)
    self.log.info('reading...')

    # read response
    response = ''.join(self.readlines())
    self.log.info('process.response: %r' % response)

    # store response in the command
    result = command.parse(response)
    self.log.info('process.parse.result: %r' % result)
    return command

class FakeCommand(object):
  __examples__ = [ ("FOO", "OK") ]
  __example__ = ("FOO", "BAR")
  raw = 'ERROR'
  """Simulates a command and a response."""
  def format(self):
    return 'FOO'
  def parse(self, raw):
    if raw == "OK":
      self.raw = raw
    return self

class FakeLink(Link):
  def __init__(self): pass
  def process(self, command):
    """
      Fake process that can read from a script.
      Useful for testing.
      >>> link = FakeLink( )

      >>> link.process(FakeCommand( )).raw
      'OK'
      
    """
    k = command.format( )
    D = dict(command.__examples__)
    result = command.parse(D[k])
    return command

class FakeKeyedLink(FakeLink):
  comm = { }

  def process(self, command):
    key = command.format( )
    raw = self.comm.get(key)
    res = command.parse(raw)
    return command
    
class FakeListLink(FakeLink):
  """A fake link useful for testing.
  This one follows a script in the sense that it ignores formatting and
  writing commands, and always reads the next message in a list of messages.

  Eg  it iterates over `comms` for each invoctation of `process`, regardless
  of the command given.

  >>> class SimpleFake(FakeListLink):
  ...   comms = [ 1, 2, 3, 'hello', 'world', 'OK' ] 
  >>> link = SimpleFake( )

  >>> link.read( )
  1

  >>> link.read( )
  2

  >>> link.read( )
  3
  >>> link.read( )
  'hello'
  >>> link.process(FakeCommand( )).raw
  'ERROR'
  >>> link.process(FakeCommand( )).raw
  'OK'

  """
  comms = [ ]
  def __init__(self):
    self.index = 0

  def read(self):
    result = self.comms[self.index]
    self.incr( )
    return result

  def incr(self, step=1):
    for i in xrange(step):
      self.index += 1

  def decr(self, step=1):
    for i in xrange(step):
      self.index -= 1

  def process(self, command):
    """We ignore formatting the command completely, and just parse the next
    available message using whatever command you gave us."""
    response = command.parse(self.read( ))
    return command

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
