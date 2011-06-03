
from optparse import *
import os


import scan



SOCKET = os.getenv('TELIT', scan.best_guess())

parser = OptionParser()

parser.add_option('-d', '--device', 
                  dest='device',
                  help="Device to use. [default=%s]" % SOCKET,
                  default = SOCKET)

if __name__ == '__main__':
  opts, args = parser.parse_args()
  print opts, args


