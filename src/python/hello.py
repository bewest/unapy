

import logging
import sys
import ge865
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)
from ge865.commands import at

from ge865 import models

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

def set_apn(link, name='webtrial.globalm2m.net', ctx=1, pdp="IP"):
  oldapn = get_apn(link)
  newapn = '"%s"' % oldapn
  if oldapn != name:
    name = '"%s"' % name
    pdp  = '"%s"' % pdp
    command = link.process(at.CGDCONT.assign(ctx, pdp, name))
    newapn = get_apn(link)
  return newapn

  
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
  print "SETTING APN"
  set_apn(link, name='webtrial.globalm2m.net')
  attached = link.process(at.CGATT.query()).data
  if int(attached[0][0]) == 0:
    print "GPRS PDP context not attached: %s" % attached
    attached = link.process(at.CGATT.assign(1))
    attached = link.process(at.CGATT.query()).data
  activated = link.process(at.SGACT.query()).data
  print "GPRS PDP context attached: %s" % attached
  print "GPRS PDP context activated: %s" % activated
  if int(attached[0][0]):
    print "context attached"
    if int(activated[0][1]) != 1:
      print "attempt sgact"
      link.process(at.SGACT.assign(1,1))

  print "ip address: ", ip_addr(link)

def use_network(link):
  print "attempt to use the network"
  # XXX: This reliably gets a CONNECT but leaves the device in a bad state.
  # I suspect we've connected and just need to figure out how to read/write to
  # the new serial line given to us.
  link.setTimeout(3)
  command = link.process(at.SD.assign(1, 0, 80, 'www.tonycode.com'))
  print command
  if command.response.isOK():
    link.write('''GET /tools/showHTTPHeaders.php HTTP/1.1
User-Agent: Foo/Bar
Host: www.tonycode.com
Accept: */*


    ''')
    page = long_read(link)
    print "### HTTP Request"
    print "\n".join(page)
  else:
    print "Did not connect."

def long_read(link, timeout=5, repeats=18):
  B = [ ]
  oldTimeout = link.getTimeout()
  link.setTimeout(timeout)
  for i in xrange(repeats):
    print "retry: %s" % i
    B += link.readlines( )
    if len(B) > 0 and B[-1].strip() == 'NO CARRIER':
      break
    time.sleep(1)
  link.setTimeout(oldTimeout)
  return B

def get_apn(link, ctx=1):
  command = link.process(at.CGDCONT.query())
  apn = None
  if command.response.isOK():
    try:
      apn = command.data[ctx-1][2]
    except IndexError: pass
  print apn
  return apn


def ip_addr(link):
  """How to find the IP address...
  """

  # inspect gets a list of context indices that can be queried for addresses.
  print link.process(at.CGPADDR.inspect()).data
  # CGPADDR uses the assign syntax to inspect IPs.
  # we only want the first one
  command = link.process(at.CGPADDR.assign(1))
  # result is in command.data, which is a list of tuples
  ip = None
  if command.response.isOK():
    try:
      ip = command.getData()
    except IndexError: pass
  
  print "IP address is ", ip
  return ip

def random(link):
  command = link.process(at.CMEE.assign(2))
  command = link.process(at.GCAP())
  command = link.process(at.SS())



if __name__ == '__main__':
  from ge865 import cli
  logging.info('hello world')
  opts, args = cli.parser.parse_args()

  #ge865.test('/dev/ttyUSB0')

  link = ge865.Link(opts.device)
  check_sim(link)
  #print "APN: ", get_apn(link)
  device = models.Device(link)
  print "device: %s" % device
  print "device manufacturer: %s" % device.manufacturer()
  #ip_addr(link)
  network_test(link)
  use_network(link)

#####
# EOF
