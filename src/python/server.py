"""
%prog [options]
Network Daemon to speak AT commands over TCP/IP.

Example of how to subclass ATFlow to use the network socket.

TODO:  A cool version would list available flows, and use a config to
assemble the correct list of flows, or even defer processing to other sockets or proc/IO. (EG dispatch to PHP.)
"""

import logging

from unapy import cli
from unapy import flow
from unapy import network
from unapy.commands.core import InvalidResponse
from unapy.commands import at
from gevent import timeout

class Flow(flow.ATFlow):
  def __call__(self):
    yield self.flow
    yield self.turn_off_tcpatrun
    raise StopIteration

  def is_machine(self, link):
    link.is_machine = link.process(at.Command( )).isOK( )
    return link.is_machine

  def check_tcpatrun(self, link):
    atruns = link.process(at.TCPATRUND.query( ))
    self.log.info('tcpatrun :' )
    self.log.info(atruns)
    self.log.info(atruns.getData( ))

  def verbose_error(self):
    self.session.process(at.CMEE.assign(2))


  def transparent_mode_on(self):
    self.log.info("what's SII?")
    self.log.info(self.session.process(at.SII.query( )))
    #self.session.process(at.SII.assign(1))
    self.log.info( "turning on transparent mode")
    rates = [ 300, 1200, 2400, 4800, 9600, 19200,
              38400, 57600, 115200 ]
    connected = False
    ports = [ 0, 1 ]
    for port in ports:
      for rate in rates:
        self.tcpatrunconser = self.session.process(at.TCPATRUNCONSER.assign(port, rate))
        if self.tcpatrunconser.isOK( ):
          break
      if self.tcpatrunconser.isOK( ):
        break
    self.log.info(self.tcpatrunconser)
    if self.tcpatrunconser.isOK( ):
      self.log.info("tcpatrunconser is OK")
    else:
      self.log.info("tcpatrunconser is NOT OK")
    return self.tcpatrunconser.isOK( )

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

  def at_check(self, link):
    self.log.info(link.process(at.AT()))

  def flow(self, req):
    # replace a la flow.py, and hello.py
    self.log.info("do stuff with request here. %r" % req )
    junk = ''.join(req.io.long_read(repeats=2)).strip( )
    if junk != '':
      self.log.info("found this junk: %s" % junk)
    req.io.setTimeout( 3 )
    req.io.write("hi there! your name?\r\n>>> ")
    name = req.io.readline( ).strip( )

    req.io.write("thanks, %s, I'm going now...\n" % name )

    if not name:
      self.log.info("%r probably not a human?" % name)

    self.at_check(req)
    self.verbose_error( )
    status = self.check_sim(req)
    self.log.info("at machine has a sim: %r" % (status,))

    self.is_machine(req)
    self.log.info("is a machine? %r" % req.is_machine)
    #req.io.setTimeout( 3 )

    self.check_tcpatrun(req)
    #req.io.setTimeout( 10 )
    try:
      if self.transparent_mode_on( ) and self.tcpatrunconser.isOK( ):
        #response = req.io.long_read( )
        import meter
        response = meter.get_mini(req)
        #req.io.write("DM@\r\n")
        #response = req.io.long_read( )
        self.log.info("response: %r" % response)
        self.log.info('turn off transparent mode.')
        self.transparent_mode_off()
      else:
        self.log.info("couldn't turn on transparent mode.")
    except InvalidResponse, e:
      self.log.info('caught invalid response')
      self.log.error(e)
      pass
    self.log.info('turn off tcpatrun for next run.')
    self.turn_off_tcpatrun(req)


class Application(cli.NetworkApp):
  def set_custom_options(self):
    super(type(self), self).set_custom_options( )
    self.parser.set_usage(__doc__)
  def custom_pre_run(self):
    logging.basicConfig( )
    self.set_logger_level(logging.getLogger(__name__))
    self.set_logger_level(logging.getLogger('unapy'))

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
