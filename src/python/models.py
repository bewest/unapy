import logging
import sys
import unapy
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
from pprint import pprint

unapy.logger.setLevel(logging.DEBUG)
from unapy.commands import at

from unapy import models

def model(device):
  model = device.model
  print "device: %s" % device

def sim(device):
  sim = device.inspect(models.SIM)
  print sim, ' enabled? ', sim.isEnabled( )


def sms(device):
  sms = device.inspect(models.SMSMessagesList)
  print sms
  print "sms elements:"
  print sms.elements( )
  for el in sms.elements( ):
    print el
    pprint(sms.decode_pdu(el.message).data)

if __name__ == '__main__':
  try:
    from unapy import cli
  except unapy.scan.ScanAttachedDevicesError, e:
    print "%s" % e
    raise
    #sys.exit(1)
    

  logging.info('hello world')

  opts, args = cli.parser.parse_args()

  #link = unapy.Link(opts.device)
  link = cli.get_link( )
  print link
  device = models.Device(link)

  for func in [ model, sim, sms ]:
    M = func(device)


