#!/usr/bin/python
"""
http://parijatmishra.wordpress.com/2008/01/06/pythons-asynchat-module/
"""


import logging
import asyncore
import asynchat
import socket

logging.basicConfig(level=logging.DEBUG,
        format="%(created)-15s %(levelname)8s %(thread)d %(name)s %(message)s")

log                     = logging.getLogger(__name__)
BACKLOG                 = 5
SIZE                    = 1024

class EchoHandler(asynchat.async_chat):

    LINE_TERMINATOR     = "\r\n"

    def __init__(self, conn_sock, client_address, server):
      asynchat.async_chat.__init__(self, conn_sock)
      self.server             = server
      self.client_address     = client_address
      self.ibuffer            = []
      self.set_terminator(self.LINE_TERMINATOR)

    def collect_incoming_data(self, data):
      log.debug("collect_incoming_data: [%s]" % data)
      self.ibuffer.append(data)

    def found_terminator(self):
      log.debug("found_terminator")
      self.send_data()

    def send_data(self):
      data = "".join(self.ibuffer)
      log.debug("sending: [%s]" % data)
      self.push(data+self.LINE_TERMINATOR)
      self.ibuffer = []

    def handle_close(self):
      log.info("conn_closed: client_address=%s:%s" % \
                (self.client_address[0],
                self.client_address[1]))

      asynchat.async_chat.handle_close(self)

class EchoServer(asyncore.dispatcher):


    allow_reuse_address         = False
    request_queue_size          = 5
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM

    def __init__(self, address, handlerClass=EchoHandler):
      self.address            = address
      self.handlerClass       = handlerClass

      asyncore.dispatcher.__init__(self)
      self.create_socket(self.address_family, self.socket_type)

      if self.allow_reuse_address:
        self.set_resue_addr()

      self.server_bind()
      self.server_activate()

    def server_bind(self):
      self.bind(self.address)
      log.debug("bind: address=%s:%s" % \
                 (self.address[0], self.address[1]))

    def server_activate(self):
      self.listen(self.request_queue_size)
      log.debug("listen: backlog=%d" % self.request_queue_size)

    def fileno(self):
      return self.socket.fileno()

    def serve_forever(self):
      asyncore.loop()

    # TODO: try to implement handle_request()
    # Internal use
    def handle_accept(self):
      (conn_sock, client_address) = self.accept()
      if self.verify_request(conn_sock, client_address):
        self.process_request(conn_sock, client_address)

    def verify_request(self, conn_sock, client_address):
      return True

    def process_request(self, conn_sock, client_address):
      log.info("conn_made: client_address=%s:%s" % \
                (client_address[0],
                client_address[1]))
      self.handlerClass(conn_sock, client_address, self)

    def handle_close(self):
      self.close()

#####
# EOF
