#! /usr/bin/env python
"""\
Scan for serial ports. Linux specific variant that also includes USB/Serial
adapters.

Part of pySerial (http://pyserial.sf.net)
(C) 2009 <cliechti@gmx.net>
"""

import serial
import glob

def scan():
    """scan for available ports. return a list of device names."""
    return glob.glob('/dev/tty.usb*') + glob.glob('/dev/ttyUSB*')

def usable_response(lines):
  for l in lines:
    if 'OK' == l:
      return True
  return False

def link_usable(candidate):
  try:
    port = serial.Serial(candidate, timeout=6)
    port.write("AT")
    if usable_response(port.readlines()):
      return True
    port.close()
  except serial.SerialException: pass

  return True


if __name__=='__main__':
    print "Found ports:"
    for name in scan():
        print name
