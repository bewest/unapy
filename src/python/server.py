
import logging

from ge865 import cli
from ge865 import flow
from ge865 import network

class Flow(flow.ATFlow):
  def flow(self, req):
    self.log.info("do stuff with request here. %r" % req )
    req.io.setTimeout( 3 )
    req.write("hi there! what's your name?\r\n>>> ")
    name = req.readline( ).strip( )
    req.write("thanks, %s, I'm going now...\n" % name )

class Application(cli.NetworkApp):
  def custom_pre_run(self):
    logging.basicConfig( )
    self.set_logger_level(logging.getLogger(__name__))

  def run(self):
    addr_info   = (self.options.host, self.options.port)
    self.server = network.SessionServer(addr_info, flow=Flow)

    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print ('Starting %s on %s' % (self.server,
                       '%s:%s' %  addr_info))
    self.server.serve_forever()

if __name__ == '__main__':
  app = Application( )
  app( )

#####
# EOF
