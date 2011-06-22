import logging
import sys
import ge865
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)
from ge865.commands import at

from ge865 import models

if __name__ == '__main__':
  try:
    from ge865 import cli
  except ge865.scan.ScanAttachedDevicesError, e:
    print "%s" % e
    raise
    #sys.exit(1)
    
  cli.parser.add_option('-p', '--port', dest='port',
                    help="Port to connect to" )
  
  cli.parser.add_option('-n', '--host', dest='host',
                    help="Port to connect to" )

  opts, args = cli.parser.parse_args()

  #link = ge865.Link(opts.device)
  link = cli.get_link( )
  device = models.Device(link)
  print device.model

  config = link.process(at.TCPATRUNCFG.query( ))
  print config.getData( )

  config = link.process(at.TCPATRUNCFG.assign(1, 2, 1024, 9339, '"24.130.113.66"'))
  print config.getData( )
  print "Trying to connect..."
  link.process(at.TCPATRUND.assign(1))




#####
# EOF
