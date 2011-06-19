
import logging
import serial
import sys
import os
import socket
import string
import asyncore

from asynchat import async_chat

PORT = 9339

class PortListener(async_chat):
  def collect_incoming_data(self):
    pass

  def found_terminator(self):
    pass

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
    pass

if __name__ == '__main__':
  app = Application( )
  app.run( )

#####
# EOF
