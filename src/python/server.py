
import logging
import serial
import sys
import os
import socket
import string
import asyncore
import signal

# http://parijatmishra.wordpress.com/2008/01/04/writing-a-server-with-pythons-asyncore-module/#HelpedImmensely.
logging.basicConfig(level=logging.DEBUG, format=' '.join(
                   ["%(created)-15s"
                   ,  "%(msecs)d%(levelname)8s"
                   ,  "%(thread)d"
                   ,  "%(name)s"
                   ,  "%(message)s"]))

log                = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


from asynchat import async_chat

PORT = 9339
SIZE = 1024


class NetworkResponse(object):
  VALID_ENDINGS = [ "OK", "ERROR", "CONNECT", "NO CARRIER" ]
  def __init__(self, raw):
    self.raw = raw
  def isValid(self):
    log.debug('valid? %s' % self.raw)
    if str(self.raw).strip( ) in VALID_ENDINGS:
      return True
    return False
  def getRaw(self):
    return self.raw

class ATMachineResponse(NetworkResponse):
  def isValid(self):
    if str(self.raw).strip( ) == "OK":
      return True

class Flow(object):
  def __init__(self, channel):
    self.channel = channel

  def __call__(self):
    pass
    
  def write(self, msg):
    self.channel.push(msg)

  def read(self):
    msg = self.channel.read()
    return msg

  def start_command(self):
    self.write("HELLO WORLD")

  def network_response(self):
    return NetworkResponse
    
  def finish_command(self):
    pass
     
  def __iter__(self):
    return self

  def next(self):
    # XXX: Just once for now.
    return self
    raise StopIteration( )

  # XXX: incorrect
  def process(self, command):
    self.command = command
    self.write(command.format( ))
    # allow the channel's buffer to fill up
    msg = self.read( )
    r = command.parse(msg)
    return command


class CommandChannel(async_chat):
  data = [ ]
  allow_reuse_address = True

  def __init__(self, server, sock, addr):
    async_chat.__init__(self, sock)
    self.request = None
    self._flow   = None
    self.server  = server
    self.addr = addr
    self.data = [ ]

    #self.push( "ARE YOU HUMAN?" )
    self.set_terminator('\r\n')
    self.shutdown = 0
    #self.connect( )

  def handle_connect(self):
    log.info( "connect event")
    self.flow( )

  # XXX: untested
  def flow(self, Flow):
    flow = Flow(self)
    log.info( 'flow: %r' % flow )
    for f in iter(flow):
      log.info( 'in iter flow: %s' % f)
      self._flow = f
      f.start_command()

      log.info(f)
      #f.fin(''.join( self.data ))
    self.push("\r\nGOOD BYE\r\n")
    self.push("")
    self.close( )
      

  def collect_incoming_data(self, data):
    self.data.append(data)

  def found_terminator(self):
    # search self.data to see if it's parseable.
    # we inspect each line to see.
    #
    # 
    if self._flow and self._flow.isValid(self.data):
      log.debug("found valid response? finish_command %r" % self.data)
      self._flow.finish_command()
    if self.data[-1].strip( ) == "OK":
      log.debug("THIS IS A MACHINE")


class EchoHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, client_addr, server):
      # We just connected.
      self.server      = server
      self.client_addr = client_addr
      self.buffer      = ""

      log.debug('Do have something to write: Hello world, MOTD, INIT COMMAND')
      # XXX: Set to True
      self.is_writable = False

      asyncore.dispatcher_with_send.__init__(self, sock)
      log.debug("created handler; waiting for loop. TODO: send message.")

    def readable(self):
      return True # always happy to read

    def writable(self):
      return self.is_writable # maybe

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoServer(asyncore.dispatcher):

    allow_reuse_address = True
    def __init__(self, host, port):
        log.info("binding to %s:%s" % (host, port))
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.handlers = [ ]

    def close(self):
      asyncore.dispatcher.close(self)
      for h in self.handlers:
        h.close( )

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            conn, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            log.debug("scheduling: creating handler")
            #handler = EchoHandler(conn, addr, self)
            handler = CommandChannel(self, conn, addr)
            self.handlers.append(handler)



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
    self.server = EchoServer(self.options.host, self.options.port)
    asyncore.loop()

if __name__ == '__main__':
  app = Application( )
  app.run( )

#####
# EOF
