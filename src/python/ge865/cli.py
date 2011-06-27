
from optparse import *
import os
import sys

import signal
import scan
import logging

GUESSES = scan.scan( )

SOCKET  = None
try:
  SOCKET = scan.best_guess( )
except scan.ScanAttachedDevicesError, e:
  pass
SOCKET  = os.getenv('PBMODEM', SOCKET)
  

parser = OptionParser()
parser.add_option('-t', '--test', 
                  help="Test" )
parser.add_option('-d', '--device', 
                  dest='device',
                  help="""\
Device to use. We'll use the /dev/usb/ttyUSB* or similar if 
we can. We'll also use the environment variable PBMODEM if  
you have a weird setup we're not scanning and you don't want
to specify the device parameter every time.                 
BEST GUESS: %s                                              
GUESSES   : %r                                              
                  """ % (SOCKET, GUESSES ),
                  default = SOCKET)

opts, args = { }, [ ]
def get_link( ):
  global opts, args
  opts, args = parser.parse_args( )
  if opts.device is None:
    try:
      opts.device = scan.best_guess( )
    except scan.ScanAttachedDevicesError, e:
      print e
      print "See -h --help on using -d --device."
      sys.exit(1)
    
  import link
  return link.Link(opts.device)

def parse_args( ):
  global opts, args
  opts, args = parser.parse_args( )


class Application(object):
  def __init__(self):
    self.loglevel = logging.FATAL
    self._get_default_parser( )
    self.set_custom_options( )
    self.setup_pre_options()
    self.parse_options( )
    self.setup_post_options()
    self.set_logging( )

  def setup(self):
    pass
  
  def __call__(self):
    self.custom_pre_run( )
    self.run( )
    self.custom_post_run( )

  def _get_default_parser(self):
    self.parser = OptionParser()
    self.parser.add_option('-l', '--logging', dest='verbose',
                      default=logging.INFO,
                      action='store_const',
                      const=logging.INFO,
                      help="Info logging. %default" )
    self.parser.add_option('-v', '--verbosity', dest='verbose',
                      action='store_const',
                      const=logging.DEBUG,
                      help="Very verbose logging." )
    self.parser.add_option('-q', '--quiet', dest='verbose',
                      action='store_const',
                      const=logging.CRITICAL,
                      help="Less verbose logging." )

  def set_logger_level(self, log):
    log.setLevel(self.loglevel)

  def set_custom_options(self):
    pass

  def setup_pre_options(self):
    pass
    
  def parse_options(self):
    opts, args = self.parser.parse_args( )
    self.args    = args
    self.options = opts

    self.loglevel = self.options.verbose

  def setup_post_options(self):
    from pprint import pprint
    pprint(self.options)
    pass

  def set_logging(self):
    self.log = logging.getLogger(sys.argv[0])
    self.set_logger_level(self.log)


  def custom_pre_run(self):
    pass

  def run(self):
    """
    Subclass this class to do stuff.
    log is self.log
    """
    raise NotImplemented("%r.run must be implemented" % self)

  def custom_post_run(self):
    pass

class NetworkApp(Application):
  def set_custom_options(self):
    self.parser.add_option('-p', '--port', dest='port',
                      default='9339',
                      type=int,
                      help="Port listen. %default" )
    
    self.parser.add_option('-n', '--host', dest='host',
                      default='0.0.0.0',
                      help="IP to bind socket. %default" )
  def setup_post_options(self):
    signal.signal(signal.SIGINT, self.signal_handler)

  def signal_handler(self, signal, frame):
      print 'closing'
      self.server.close( )
      print 'Exiting!'
      sys.exit(0)
  def run(self):
    print "Binding to {host}:{port} ...".format(host=self.options.host, port=self.options.port)
  
class CLIApp(Application):
  def set_custom_options(self):
    self.parser.add_option('-d', '--device', 
                      dest='device',
                      help="""\
Device to use. We'll use the /dev/usb/ttyUSB* or similar if 
we can. We'll also use the environment variable PBMODEM if  
you have a weird setup we're not scanning and you don't want
to specify the device parameter every time.                 
BEST GUESS: %s                                              
GUESSES   : %r                                              
                  """ % (SOCKET, GUESSES ),
                      default = SOCKET)

  def setup_post_options(self):
    # get a device and a link
    from pprint import pprint
    pprint(self.options)
    self.get_link( )
    self.get_device( )

  def get_link(self):
    opts = self.options
    if opts.device is None:
      try:
        opts.device = scan.best_guess( )
      except scan.ScanAttachedDevicesError, e:
        print e
        print "See -h --help on using -d --device."
        sys.exit(1)
      
    self.log("creating device: %s\n" % opts.device)
    import link
    self.link = link.Link(opts.device)

  def get_device(self):
    from models import Device
    self.device = models.Device(self.link)
  def run(self):
    print "Sending AT:"
    self.link.write("AT\r")
    print "Response: ", self.link.readlines( )
    self.link.close( )
    

if __name__ == '__main__':
  opts, args = parser.parse_args()
  print opts, args

#####
# EOF
