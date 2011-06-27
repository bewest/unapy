from gevent.server import StreamServer
from gevent.socket import timeout
import logging

from commands.core import InvalidResponse
from flow import BaseFlow, ATFlow, Session

from util import Loggable

# kind of looks more like a serial port
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

class SessionHandler(Loggable):
  def __init__(self, socket, addr):
    self.getLog( )
    self.socket, self.addr = socket, addr
    self.rfile = socket.makefile()

  def close(self):
    # do not rely on garbage collection
    self.socket._sock.close()
    self.rfile._sock.close()
    self.__dict__.pop('socket')
    self.__dict__.pop('rfile')
    
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

class SessionServer(StreamServer, Loggable):
  def __init__(self, listener, application=None, backlog=None,
                     spawn='default', flow=BaseFlow, **ssl_args):
    StreamServer.__init__(self, listener, backlog=backlog, spawn=spawn, **ssl_args)
    self.flow = flow
    self.getLog( )

  def handle(self, socket, address):
    handler = SessionHandler(socket, address)
    handler.handle(self.flow)
    
#####
# EOF
