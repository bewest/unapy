from gevent.server import StreamServer
from gevent.socket import timeout
import logging

import sys
from gevent import socket
from gevent.socket import EWOULDBLOCK
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
      flows.error(e)
      self.log.info("XXX: invalid response!: closing flow%r" % e)
    self.log.debug("done with flow")
    self.close( )

class WeirdServer(StreamServer, Loggable):
  def _do_accept(self):
    for _ in xrange(self.max_accept):
      address = None
      try:
        if self.full( ):
          self.stop_accepting()
          return
        try:
          client_socket, address = self.socket.accept( )
        except socket.error, err:
          if err[0] == EWOULDBLOCK:
            return
          raise
        self.delay = self.min_delay
        client_socket = socket.socket(_sock=client_socket)
        spawn = self._spawn
        if spawn is None:
          self._handle(client_socket, address)
        else:
          spawn(self._handle, client_socket, address)
      except:
        self.loop.handle_error((address, self), *sys.exc_info( ))
        ex = sys.exc_info( )[1]
        if self.is_fatal_error(ex):
          self.kill( )
          sys.stderr.write('ERROR: %s failed with %s\n' % (self,
                           str(ex) or repr(ex)))
          return
        if self.delay >= 0:
          self.stop_accepting( )
          self._start_accepting_timer = self.loop.timer(self.delay)
          self._start_accepting_timer.start(self._start_accepting_if_started)
          self.delay = min(self.max_delay, self.delay * 2)
        break

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
