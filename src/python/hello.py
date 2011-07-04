

import logging
import sys
import pbmodem
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

pbmodem.logger.setLevel(logging.DEBUG)
from pbmodem import cli
from pbmodem.commands import at

from pbmodem import models

EXAMPLE_IP_REPLY='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n\r\nOK\r\n'
EXAMPLE_IP_to_python='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n'


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
  attached = link.process(at.CGATT.query()).getData( )
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

class Flow(object):
  pass

class Application(cli.CLIApp):
  def run(self):
    """
    Do everything interesting here.
    """
    check_sim(self.link)
    #print "APN: ", get_apn(self.link)
    #device = models.Device(self.link)
    #print "device: %s" % device
    #print "device manufacturer: %s" % device.manufacturer()
    ip_addr(self.link)
    network_test(self.link)
    use_network(self.link)


if __name__ == '__main__':
  logging.info('hello world')

  app = Application( )
  app.run( )

  #pbmodem.test('/dev/ttyUSB0')

#####
# EOF
