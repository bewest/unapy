#!/usr/bin/python

# Python debugger for arduino

import serial
import os, sys
import logging
import time
from insulaudit import lib
logging.basicConfig( )
log = logging.getLogger('dumb')
log.setLevel(logging.INFO)
log.info("hello world")

weird  = [ 0xFE ] * 14
tail   = [ 0xFF ] * 3

set_rate = bytearray( [ ':', '6', ';', 0x0D])
confirm_command = bytearray( [ ':', '!', ';', 0x0D])
reset_arduino = bytearray([':', '#', ';', 0x0D])
keep_alive = bytearray( [0xFE] * 8)

def send_command(port, comm):
  log.info("sending:")
  log.info(lib.hexdump(bytearray(comm)))
  port.write(str(comm))
  time.sleep(1)
  response = ''.join(port.readlines( ))
  if len(response) > 0:
    print "RESPONSE!!!!"
    print lib.hexdump(bytearray(response))
  return response
  
  

def main(device):
  log.info( "opening device: %s" % device )
  ser = serial.Serial(device)
  ser.setTimeout(2)
  time.sleep(2)
  send_command(ser, set_rate)
  send_command(ser, confirm_command)
  send_command(ser, keep_alive)  
  send_command(ser, reset_arduino)
  send_command(ser, confirm_command)
  send_command(ser, keep_alive)
  ser.close( )


if __name__ == '__main__':
  main(sys.argv[1])
#####
# EOF
