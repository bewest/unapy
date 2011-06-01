

import logging
import sys
import ge865
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)
from ge865.commands import at

EXAMPLE_IP_REPLY='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n\r\nOK\r\n'
EXAMPLE_IP_to_python='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n'

def to_python(msg):
  """
    >>> len(to_python(EXAMPLE_IP_to_python))
    1
    >>> to_python(EXAMPLE_IP_to_python)
    [(1, '10.215.91')]

  """
  lines  = msg.strip().splitlines()
  result = [ ]
  r      = ( )
  for l in lines:
    parts = l.split(': ')
    if len(parts) > 1:
      parts = ''.join(parts[1:]
               ).replace('"', '').replace("'", "").split(',')
      r = tuple(parts)
      if len(parts) > 1:
        r = ( int(parts[0]), ) + tuple(parts[1:])
      result.append(r)
  return result

def check_sim(link):
  command = link.process(at.QSS.query())
  print command.response.getData()

def network_test(link):
  print "network test"
  command = link.process(at.CMEE.assign(2))
  print command.data
  command = link.process(at.CGMR())
  print command.data
  command = link.process(at.CREG.query())
  print command.data
  command = link.process(at.CSQ())
  print command.data

  
def ip_addr(link):
  print link.process(at.CGPADDR.inspect()).data
  # CGPADDR uses the assign syntax to inspect IPs.
  command = link.process(at.CGPADDR.assign(1))
  ip = command.data
  print "IP address is ", ip

def random(link):
  command = link.process(at.CMEE.assign(2))
  command = link.process(at.GCAP())
  command = link.process(at.SS())



if __name__ == '__main__':
  logging.info('hello world')
  logging.debug('hello world')
  #ge865.test('/dev/ttyUSB0')

  link = ge865.Link('/dev/ttyUSB1')
  #check_sim(link)
  network_test(link)
  ip_addr(link)

#####
# EOF
