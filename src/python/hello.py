

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
  attached = link.process(at.CGATT.query()).data
  if int(attached[0][0]) == 0:
    print "GPRS PDP context not attached: %s" % attached
    attached = link.process(at.CGATT.assign(1)).data
  activated = link.process(at.SGACT.query()).data
  print "GPRS PDP context attached: %s" % attached
  print "GPRS PDP context activated: %s" % activated
  if int(attached[0][0]):
    print "context attached"
    if activated[0][1] != 1:
      print "attempt sgact"
      link.process(at.SGACT.assign(1,1))

  ip_addr(link)

  print "attempt to use the network"
  # XXX: This reliably gets a CONNECT but leaves the device in a bad state.
  # I suspect we've connected and just need to figure out how to read/write to
  # the new serial line given to us.
  command = link.process(at.SD.assign(1, 0, 80, 'www.transactionalweb.com'))
  print command
  link.write('GET /ip.htm\n\n')
  link.setTimeout(60)
  page = link.readlines()
  print page


def get_apn(link):
  ctx = link.process(at.CGDCONT.query())
  print ctx.data


def ip_addr(link):
  """How to find the IP address...
  """

  # inspect gets a list of context indices that can be queried for addresses.
  print link.process(at.CGPADDR.inspect()).data
  # CGPADDR uses the assign syntax to inspect IPs.
  # we only want the first one
  command = link.process(at.CGPADDR.assign(1))
  # result is in command.data, which is a list of tuples
  ip = command.data
  print "IP address is ", ip[0][1]

def random(link):
  command = link.process(at.CMEE.assign(2))
  command = link.process(at.GCAP())
  command = link.process(at.SS())



if __name__ == '__main__':
  logging.info('hello world')
  logging.debug('hello world')
  #ge865.test('/dev/ttyUSB0')

  link = ge865.Link('/dev/ttyUSB0')
  #check_sim(link)
  get_apn(link)
  ip_addr(link)
  network_test(link)

#####
# EOF
