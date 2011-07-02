from gevent.server import StreamServer
from gevent.socket import timeout
import logging

from commands.core import InvalidResponse
from flow import BaseFlow, ATFlow, Session, NetworkSession
#from gevent import timeout

from util import Loggable

class SessionHandler(Loggable):
  def __init__(self, socket, addr):
    self.getLog( )
    self.socket, self.addr = socket, addr
    self.rfile = socket.makefile()

  def close(self):
    # do not rely on garbage collection
    self.rfile.write('+++\r\n')
    self.socket._sock.close()
    self.rfile._sock.close()
    self.__dict__.pop('socket')
    self.__dict__.pop('rfile')
    
  def handle(self, Flow):
    """
    Package up a client connection, socket, usable file object into a Session,
    and execute a flow against the session.  A Session is a combination of
    input/output and handler Flows should implement the iterable protocol so
    that we can dynamically iterate over flows.  Implementing __call__ as a
    generator, provides an easy way to create state machines.  The default
    implementation provided just calls Flow#flow once.

    Close the connection, when done.
    """
    # Useful for attaching stuff as it goes through various flows.
    session = NetworkSession(self.socket, self)
    self.log.debug( "handling connection, starting flow")
    #self.session = session
    # a Flow is a list of callables recieving a session.
    flows = Flow(session)
    self.log.debug('flows: %r' % flows)
    try:
      for flow in flows( ):
        flow(session)
    except InvalidResponse, e:
      self.log.info("XXX: invalid response!: closing flow%r" % e)
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
