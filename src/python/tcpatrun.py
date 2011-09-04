import logging
import sys
import unapy
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

unapy.logger.setLevel(logging.DEBUG)
from unapy.commands import at

from unapy import models

if __name__ == '__main__':
  try:
    from unapy import cli
  except unapy.scan.ScanAttachedDevicesError, e:
    print "%s" % e
    raise
    #sys.exit(1)
    
  cli.parser.add_option('-p', '--port', dest='port',
                    help="Port to connect to" )
  
  cli.parser.add_option('-n', '--host', dest='host',
                    help="Port to connect to" )

  opts, args = cli.parser.parse_args()

  #link = unapy.Link(opts.device)
  link = cli.get_link( )
  device = models.Device(link)
  print device.model

  config = link.process(at.TCPATRUNCFG.query( ))
  print config.getData( )

  config = link.process(at.TCPATRUNCFG.assign(1, 2, 1024, opts.port, '"%s"' % opts.host))
  print config.getData( )
  print "Trying to connect..."
  link.process(at.TCPATRUND.assign(1))




#####
# EOF
