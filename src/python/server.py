"""
%prog [options]
Network Daemon to speak AT commands over TCP/IP.

Example of how to subclass ATFlow to use the network socket.

TODO:  A cool version would list available flows, and use a config to
assemble the correct list of flows, or even defer processing to other sockets or proc/IO. (EG dispatch to PHP.)
"""

import logging

from ge865 import cli
from ge865 import flow
from ge865 import network
from ge865.commands import at
from gevent import timeout

class Flow(flow.ATFlow):
  def is_machine(self, link):
    link.is_machine = link.process(at.Command( )).isOK( )
    return link.is_machine

  def check_tcpatrun(self, link):
    atruns = link.process(at.TCPATRUND.query( ))
    self.log.info('tcpatrun :' )
    self.log.info(atruns.getData( ))

  def verbose_error(self):
    self.log.info( "turning on transparent mode")
    self.session.process(at.CMEE.assign(2))


  def transparent_mode_on(self):
    self.log.info( "turning on transparent mode")
    self.tcpatrunconser = self.session.process(at.TCPATRUNCONSER.assign(1, 9600))

  def transparent_mode_off(self):
    self.log.info( "turning off transparent mode")
    self.tcpatrunconser = self.session.io.write('+++')

  def turn_off_tcpatrun(self, link):
    link.process(at.TCPATRUNCLOSE( ))

  def check_sim(self, link):
    command = link.process(at.QSS.query())
    qss = command.getData( )
    self.log.info("sim status %r" % (qss, ))
    return qss

  def flow(self, req):
    # replace a la flow.py, and hello.py
    self.log.info("do stuff with request here. %r" % req )
    req.io.setTimeout( 3 )
    req.io.write("hi there! what's your name?\r\n>>> ")
    name = req.io.readline( ).strip( )

    req.io.write("thanks, %s, I'm going now...\n" % name )

    if not name:
      self.log.info("%r probably not a human?" % name)

    self.verbose_error( )
    status = self.check_sim(req)
    self.log.info("at machine has a sim: %r" % (status,))

    self.is_machine(req)
    self.log.info("is a machine? %r" % req.is_machine)
    #req.io.setTimeout( 3 )

    self.check_tcpatrun(req)
    #req.io.setTimeout( 10 )
    self.transparent_mode_on()
    self.transparent_mode_off()
    self.turn_off_tcpatrun(req)


class Application(cli.NetworkApp):
  def set_custom_options(self):
    super(type(self), self).set_custom_options( )
    self.parser.set_usage(__doc__)
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
