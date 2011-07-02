
from util import Loggable
import link

class IoProcessor(link.AtProcessor):
  """
  A file like object implementing a callable that callable that calls
  self.process.

  :term:`io` should be an :class:`AtProcessor` (an object with a process method that expects to
  process :term:`core`
  """
  """An object with a process method. (an AtProcessor)"""
  io = None
  def __init__(self, io):
    self.io      = io
    super(IoProcessor, self).__init__()

  def read(self):
    return self.io.read()

  def readline(self):
    return self.io.readline( )

  def readlines(self):
    return self.io.readlines( )

  def write(self, msg):
    return self.io.write(msg)

  def getTimeout(self):
    return self.io.getTimeout()

  def setTimeout(self, timeout):
    self.io.setTimeout(timeout)

  def __call__(self, command):
    return self.process(command)

class IoSocketProcessor(IoProcessor):
  length = 1024
  writeTimeout = None
  readTimeout  = None
  def __init__(self, socket, length = None, readTimeout=5, writeTimeout=3):
    self.getLog( )
    self.socket = socket
    self.rfile  = socket.makefile()
    if readTimeout:
      self.readTimeout = readTimeout
    if writeTimeout:
      self.writeTimeout = writeTimeout
    self.socket = socket
    self.log.debug(self.rfile)
    if length is not None:
      self.length = length

  def close(self):
    # do not rely on garbage collection
    self.rfile.write('+++\r')
    self.socket._sock.close()
    self.rfile._sock.close()
    self.__dict__.pop('socket')
    self.__dict__.pop('rfile')

  def getTimeout(self):
    return self.rfile._sock.gettimeout()

  def setTimeout(self, timeout):
    self.socket.settimeout(timeout)
    self.rfile._sock.settimeout(timeout)

  def read(self, length=None):
    if length is None:
      length = self.length
    return self.rfile.read()


  def readline(self):
    from gevent.socket import timeout
    prev = self.getTimeout()
    r    = ''
    if self.readTimeout:
      self.setTimeout(self.readTimeout)

    try:
      r = self.rfile.readline( )
    except timeout, e: pass
    if prev:
      self.setTimeout(prev)
    return r

  def readlines(self):
    return list(self)

  def __iter__(self):
    return self

  def write(self, msg):
    prev = self.getTimeout()
    if self.writeTimeout:
      self.setTimeout(self.writeTimeout)
    self.rfile.write(msg)
    self.rfile.flush( )
    if prev:
      self.setTimeout(prev)

  def next(self):
    try:
      line = self.readline( )
    except timeout, e:
      raise StopIteration
    if not line:
      raise StopIteration
    return line

class Session(Loggable):
  io      = None
  handler = None
  def __init__(self, io, handler):
    self.io      = io
    self.handler = handler
    self.getLog()
    self.process = IoProcessor(io)


class NetworkSession(Loggable):

  def __init__(self, io, handler):
    self.io      = IoSocketProcessor(io)
    self.handler = handler
    self.getLog()

  def process(self, command):
    return self.io.process(command)

  


class BaseFlow(Loggable):
  """A Flow is a class implementing a callable.  The class is initialized
  with the session at the start of the connection, and is expected to return
  a list of flows to run when it is called.

  The session object is an ATCommand processor, and useful for passing state
  between flows.
  This implementation simply executes the flow method once before exiting the
  session.
  """
  "Set during __init__."
  session = None
  def __init__(self, session):
    """
    sets self.session
    """
    self.session = session
    self.getLog( )
  def __call__(self):
    yield self.flow
    raise StopIteration

  def flow(self, req):
    """
    Example flow: send a message, read input.
    You should write your own.
    """
    io = req.io
    #io.throwError( )
    #io.setTimeout(2)
    # first command
    self.log.debug( "writing command")
    io.write('XXXXHELLO WORLD\n')
    self.log.debug( "reading response")
    #msg = self.rfile.readline( )
    msg = io.readline( )
    #msg = io.readlines()
    io.write( "OK: %s" % msg )
    self.log.debug("got message: %s" % msg )

    # second command
    io.write('second command\n')
    msg = io.readline( )
    self.log.debug("got message 2: %s" % msg )
    io.write( "OK: %s" % msg )

    # third command
    io.write('third command:\n')
    msg = io.readlines( )
    io.write( "OK: %s" % msg )


    io.write("bye")
    self.log.debug("done with flow")

    return msg
  
class ATFlow(BaseFlow):

  def process(self, command):
    self.log.debug("%r.process" % (self))
    return self.session.process(command)


#####
# EOF
