from gevent.server import StreamServer
from gevent.socket import timeout
import logging

from commands.core import InvalidResponse

from util import Loggable
import link

class Input(Loggable):
  length = 1024
  def __init__(self, rfile, socket, length = None):
    self.getLog( )
    self.rfile  = rfile
    self.socket = socket
    self.log.debug(self.rfile)
    if length is not None:
      self.length = length

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
    return self.rfile.readline( )

  def readlines(self):
    return list(self)

  def __iter__(self):
    return self

  def write(self, msg):
    self.rfile.write(msg)
    self.rfile.flush( )

  def next(self):
    try:
      line = self.readline( )
    except timeout, e:
      raise StopIteration
    if not line:
      raise StopIteration
    return line

class IoProcessor(link.AtProcessor):
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

  def __call__(self, command):
    return self.process(command)

class Session(IoProcessor):
  io      = None
  handler = None

  def __init__(self, io, handler):
    self.io      = io
    self.handler = handler
    self.process = IoProcessor(io)


class BaseFlow(Loggable):
  """A Flow is a function which returns a list of flows to run.
  
  The original function and every called flow recieves a session object, which
  is useful for passing state between flows.
  """
  def __init__(self, session):
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

class SessionHandler(Loggable):
  def __init__(self, socket, addr):
    self.getLog( )
    self.socket, self.addr = socket, addr
    self.rfile = socket.makefile()

  def write(self, msg):
    self.rfile.write(msg)
    self.rfile.flush( )

  def read(self):
    msg = self.rfile.readline( )
    return msg

  def close(self):
    # do not rely on garbage collection
    self.socket._sock.close()
    #self.rfile._sock.close()
    
  def handle(self, Flow):
    """
    Package up a client connection, socket, usable file object, and execute a
    flow.
    Close the connection, when done.
    """
    # XXX: Move this to session or to __init__?
    io      = Input(self.rfile, self.socket)
    # A Session is a combination of input/output and handler
    # Useful for attaching stuff as it goes through various flows.
    session = Session(io, self)
    self.log.debug( "handling connection, starting flow")
    #self.session = session
    # a Flow is a list of callables recieving a session.
    flows = Flow(session)
    self.log.debug('flows: %r' % flows)
    try:
      for flow in flows( ):
        flow(session)
    except InvalidResponse, e:
      log.info("XXX: invalid response!: closing flow%r" % e)
    self.log.debug("done with flow")
    self.close( )

  def getFlow(self, session):
    return self.flow(session)
    return Flow(session)
    return [ self.flow ]



class SessionServer(StreamServer, Loggable):
  def __init__(self, listener, application=None, backlog=None, spawn='default',
                     flow=BaseFlow, **ssl_args):
    StreamServer.__init__(self, listener, backlog=backlog, spawn=spawn, **ssl_args)
    self.flow = flow
    self.getLog( )
  def handle(self, socket, address):
    handler = SessionHandler(socket, address)
    handler.handle(self.flow)
    

