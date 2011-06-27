
import logging

from ge865 import cli
from gevent.server import StreamServer


from ge865 import network

class Flow(network.ATFlow):
  def flow(self, req):
    print self.log
    self.log.warn("AHWARNA")
    self.log.debug("AHDEBUG")
    self.log.info("AHINFOA")
    self.log.critical("CRITAHA")
    self.log.fatal("AHFATAL")

class Application(cli.NetworkApp):
  def custom_pre_run(self):
    logging.basicConfig( )
    self.set_logger_level(logging.getLogger(__name__))
  def run(self):
    self.server = network.SessionServer((self.options.host, self.options.port), flow=Flow)
    #self.server = StreamServer((self.options.host, self.options.port))
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print ('Starting %s on %s:%s' % (self.server, self.options.host, self.options.port))
    self.server.serve_forever()

if __name__ == '__main__':
  app = Application( )
  app( )

#####
# EOF
