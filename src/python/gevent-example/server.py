#!/usr/bin/env python
"""Simple server that listens on port 6000 and echos back every input to the client.

Connect to it with:
  telnet localhost 6000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from gevent.server import StreamServer
from gevent.socket import timeout
import logging
logging.basicConfig(level=logging.DEBUG, format=' '.join(
                   ["%(created)-15s"
                   ,  "%(msecs)d%(levelname)8s"
                   ,  "%(thread)d"
                   ,  "%(name)s"
                   ,  "%(message)s"]))

log                = logging.getLogger(__name__)
import sys
import signal

# hack to mangle PYTHONPATH
import user
import ge865
from ge865.commands import at

class Input(object):
  length = 1024
  def __init__(self, rfile, socket, length = None):
    self.rfile  = rfile
    self.socket = socket
    log.debug(self.rfile)
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

class IoProcessor(ge865.link.AtProcessor):
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
class ATSession(Session):
  def __init__(self, io, handler):
    super(ATSession, self).__init__(io, handler)


class SniffIsMachineQuery(at.Command):
  def format(self):
    return """This is experimental software.
XXX: Replace with some kind of MOTD.
If you are not an AT machine, you should go away.
AT\r\nAT\r\n"""

class BaseFlow(object):
  """A Flow is a function which returns a list of flows to run.
  
  The original function and every called flow recieves a session object, which
  is useful for passing state between flows.
  """
  def __init__(self, session):
    self.session = session
  def __call__(self):
    yield self.flow
    raise StopIteration

  def flow(self, req):
    """
    Example flow: send a message, read input.
    You should write your own.
    """
    io = req.io
    io.throwError( )
    io.setTimeout(2)
    # first command
    log.debug( "writing command")
    io.write('XXXXHELLO WORLD\n')
    log.debug( "reading response")
    #msg = self.rfile.readline( )
    msg = io.readline( )
    #msg = io.readlines()
    io.write( "OK: %s" % msg )
    log.debug("got message: %s" % msg )

    # second command
    io.write('second command\n')
    msg = io.readline( )
    log.debug("got message 2: %s" % msg )
    io.write( "OK: %s" % msg )

    # third command
    io.write('third command:\n')
    msg = io.readlines( )
    io.write( "OK: %s" % msg )


    io.write("bye")
    log.debug("done with flow")

    return msg
  
class ATFlow(BaseFlow):

  def process(self, command):
    log.debug("%r.process" % (self))
    return self.session.process(command)

# Eventually load flows that can defer to other flows...
class Flow(ATFlow):

  def __call__(self):
    yield self.sniff
    if self.session.is_machine:
      yield self.identify
    raise StopIteration

  def identify(self, req):
    from ge865 import models
    device = models.Device(req)
    #command = req.process(models.M
    model = device.model
    req.device = device
    req.model  = model
    log.debug("device: %s" % device)
    log.debug("model: %s"  % model)

  def sniff(self, req):
    io = req.io
    req.is_machine = False
    try:
      io.setTimeout(26)
      # first command
      log.debug( "writing command")
      io.write('AT\r\n')
      msg = ''.join(io.readlines( ))
      log.debug('raw response: %r' % msg)
      if "OK" in msg:
        req.is_machine = True
        log.debug("skip rest of sniffing")
        return
      io.write('HELLO WORLD\n')
      log.debug( "reading response")
      #msg = self.rfile.readline( )
      msg = io.readline( )
      #msg = io.readlines()
      io.write( "OK: %s" % msg )
      log.debug("got message: %s" % msg )

      # second command
      io.write('second command\n')
      msg = io.readline( )
      log.debug("got message 2: %s" % msg )
      io.write( "OK: %s" % msg )

      # third command
      io.write('third command:\n')
      msg = io.readlines( )
      io.write( "OK: %s" % msg )

    except timeout, e:
      try:
        log.debug('sniffing machine...')
        command = self.process(SniffIsMachineQuery( ))
        log.debug("%s" % command)
        if command.isOK( ):
          req.is_machine = True
          log.info("pretty sure we found a machine.")
      except IndexError, e:
        # not an ATMachine
        log.info("pretty sure this is not a machine?")


    io.write("done sniffing\n")
    log.debug("done with flow")


class SessionHandler(object):
  def __init__(self, socket, addr):
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
    
  def handle(self):
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
    log.debug( "handling connection, starting flow")
    #self.session = session
    # a Flow is a list of callables recieving a session.
    flows = self.getFlow(session)
    log.debug('first flow: %s' % flows)
    try:
      for flow in flows( ):
        flow(session)
    except ge865.commands.core.InvalidResponse, e:
      log.info("XXX: invalid response!: closing flow%r" % e)
    log.debug("done with flow")
    self.close( )

  def getFlow(self, session):
    return Flow(session)
    return [ self.flow ]



class SessionServer(StreamServer):
  def handle(self, socket, address):
    handler = SessionHandler(socket, address)
    handler.handle()
    

# this handler will be run for each incoming connection in a dedicated greenlet
def simple_flow(socket, address):
  log.debug("new connection from %s:%s" % address)

  # setup
  session = SessionHandler(socket, address)
  session.flow( )
  session.close( )
  log.debug('flowing session: %s' % session)
  #return session

def echo(socket, address):
    print ('New connection from %s:%s' % address)
    # using a makefile because we want to use readline()
    fileobj = socket.makefile()
    fileobj.write('Welcome to the echo server! Type quit to exit.\r\n')
    fileobj.flush()
    while True:
        line = fileobj.readline()
        if not line:
            print ("client disconnected")
            break
        if line.strip().lower() == 'quit':
            print ("client quit")
            break
        fileobj.write(line)
        fileobj.flush()
        print ("echoed %r" % line)

class Application(object):
  def __init__(self):
    self.setup()
    signal.signal(signal.SIGINT, self.signal_handler)

  def signal_handler(self, signal, frame):
      print 'closing'
      self.server.close( )
      print 'Exiting!'
      sys.exit(0)

  def setup(self):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-v', '--verbosity', dest='verbose',
                      default=logging.DEBUG,
                      type=int,
                      help="Verbosity." )
    parser.add_option('-p', '--port', dest='port',
                      default='9339',
                      type=int,
                      help="Port listen." )
    
    parser.add_option('-n', '--host', dest='host',
                      default='0.0.0.0',
                      help="IP to bind socket." )
    opts, args = parser.parse_args( )
    self.options = opts

    self.set_logging()

  def set_logging(self):
    self.log = logging.getLogger(sys.argv[0])
    self.log.setLevel(self.options.verbose)
    
  def run(self):
    #self.server = StreamServer((self.options.host, self.options.port), echo)
    #self.server = StreamServer((self.options.host, self.options.port), simple_flow)
    self.server = SessionServer((self.options.host, self.options.port))
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print ('Starting echo server on %s:%s' % (self.options.host, self.options.port))
    self.server.serve_forever()


if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    app = Application( )
    app.run( )


#####
# EOF
