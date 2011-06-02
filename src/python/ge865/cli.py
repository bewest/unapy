
from optparse import *
import os


import scan

_candidates = filter(scan.link_usable, scan.scan())


SOCKET = os.getenv('TELIT', _candidates[0])

parser = OptionParser()

parser.add_option('-d', '--device', 
                  dest='device',
                  help="Device to use. [default=%s]" % SOCKET,
                  default = SOCKET)

if __name__ == '__main__':
  opts, args = parser.parse_args()
  print opts, args


