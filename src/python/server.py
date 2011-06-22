
import logging
import serial
import sys
import os
import socket
import string
import asyncore

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

class Flow(object):
  def __call__(self):
    pass

class CommandChannel(async_chat):
  data = [ ]
  allow_reuse_address = True

  def __init__(self, server, sock, addr):
    async_chat.__init__(self, sock)
    self.request = None
    self.server  = server
    self.addr = addr
    self.data = [ ]

    self.push( "ARE YOU HUMAN?" )
    self.set_terminator('\r\n')
    self.shutdown = 0

  def collect_incoming_data(self, data):
    self.data.append(data)


  def found_terminator(self):
    # search self.data to see if it's parseable.
    #
    # 
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
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

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



class Application(object):
  def __init__(self):
    self.setup()

  def setup(self):
    sys.argv
    self.set_logging()

  def set_logging(self):
    self.log = logging.getLogger(sys.argv[0])
    self.log.setLevel(logging.INFO)
    
  def run(self):
    server = EchoServer('0.0.0.0', PORT)
    asyncore.loop()

if __name__ == '__main__':
  app = Application( )
  app.run( )

#####
# EOF
