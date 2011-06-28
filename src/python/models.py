import logging
import sys
import ge865
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
from pprint import pprint

ge865.logger.setLevel(logging.DEBUG)
from ge865.commands import at

from ge865 import models

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
    from ge865 import cli
  except ge865.scan.ScanAttachedDevicesError, e:
    print "%s" % e
    raise
    #sys.exit(1)
    

  logging.info('hello world')

  opts, args = cli.parser.parse_args()

  #link = ge865.Link(opts.device)
  link = cli.get_link( )
  print link
  device = models.Device(link)

  for func in [ model, sim, sms ]:
    M = func(device)


