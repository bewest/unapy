
from optparse import *
import os
import sys

import scan

GUESSES = scan.scan( )

SOCKET  = None
try:
  SOCKET = scan.best_guess( )
except scan.ScanAttachedDevicesError, e:
  pass
SOCKET  = os.getenv('PBMODEM', SOCKET)
  

parser = OptionParser()
parser.add_option('-t', '--test', 
                  help="Test" )
parser.add_option('-d', '--device', 
                  dest='device',
                  help="""\
Device to use. We'll use the /dev/usb/ttyUSB* or similar if 
we can. We'll also use the environment variable PBMODEM if  
you have a weird setup we're not scanning and you don't want
to specify the device parameter every time.                 
BEST GUESS: %s                                              
GUESSES   : %r                                              
                  """ % (SOCKET, GUESSES ),
                  default = SOCKET)

opts, args = { }, [ ]
def get_link( ):
  global opts, args
  opts, args = parser.parse_args( )
  if opts.device is None:
    try:
      opts.device = scan.best_guess( )
    except scan.ScanAttachedDevicesError, e:
      print e
      print "See -h --help on using -d --device."
      sys.exit(1)
    
  import link
  return link.Link(opts.device)

def parse_args( ):
  global opts, args
  opts, args = parser.parse_args( )


if __name__ == '__main__':
  opts, args = parser.parse_args()
  print opts, args

#####
# EOF
