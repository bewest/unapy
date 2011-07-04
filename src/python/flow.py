
import sys
import logging
log = logging.getLogger('tool')

from pbmodem import cli
from pbmodem import flow
from pbmodem.commands import at
from pprint import pformat

class TCPATRUN(flow.ATFlow):
  def get_config(self):
    self.tcpatruncfg = self.session.process(at.TCPATRUNCFG.query( ))
    log.info(' '.join( map( pformat, [
                  self.tcpatruncfg,
                  self.tcpatruncfg.getData( ) ]) ))

  def get_active_instances(self):
    self.active_instances = self.session.process(at.TCPATRUND.query( ))

  def flow(self, req):
    self.get_config()
    self.get_active_instances( )

class PDPContext(flow.ATFlow):
  apns = None
  def _get_config(self):
    # TODO: make this return something from a config file or database or cli
    # options
    default = {
      'apn': [ ]
    }
    return {
      'apn': [
        { 'cid': 1, 'name': 'webtrial.globalm2m.net' },
        ],
      'auth': [

      ],
      'attach': True,
    }

  def flow(self, req):
    config = self._get_config()
    self.set_module_verbose_error()
    self.get_apns( )

    for apn in config.get('apn', [ ]):
      if apn['name'] != self.get_apns:
        self.set_apn(**apn)
      if config.get('attach', False):
        if not self.is_attached( ):
          self.attach_grps( )

  def get_active_cids(self):
    self.cids = self.session.process(at.SGACT.query( ))

  def get_ip_addr(self):
    self.ip_addr_info = self.session.process(at.CGPADDR.assign(1))
    return self.ip_addr_info

  def get_apns(self):
    command = self.session.process(at.CGDCONT.query( ))
    self.apns = command.getData( )
    return self.apns

  def get_apn(self, ctx=1):
    r = ''
    if self.apns is None:
      self.get_apns( )
    try:
      r = self.apns[ctx].name
    except IndexError, e: pass # no apn
    return r
    

  def set_apn(self, name='webtrial.globalm2m.net', cid=1, pdp="IP"):
    oldapn = self.get_apn(cid)
    newapn = '"%s"' % oldapn
    if oldapn != name:
      name = '"%s"' % name
      pdp  = '"%s"' % pdp
      command = self.session.process(at.CGDCONT.assign(cid, pdp, name))
      self.get_apns( )
      newapn = self.get_apn(cid)
    return newapn


  def set_module_verbose_error(self):
    command = self.session.process(at.CMEE.assign(2))
    log.info(command.getData( ))

  def is_registered(self):
    command = self.session.process(at.CREG.query())
    result  = command.getData( )
    return result[1]

  def attach_grps(self):
    self.session.process(at.CGATT.assign(1))
    
  def is_attached(self):
    attached = self.session.process(at.CGATT.query()).getData( )
    return attached

  def hello(self):
    attached = link.process(at.CGATT.query()).data
    if int(attached[0][0]) == 0:
      print "GPRS PDP context not attached: %s" % attached
      attached = link.process(at.CGATT.assign(1))
    activated = link.process(at.SGACT.query()).data
    print "GPRS PDP context attached: %s" % attached
    print "GPRS PDP context activated: %s" % activated
    if int(attached[0][0]):
      print "context attached"
      if int(activated[0][1]) != 1:
        print "attempt sgact"
        link.process(at.SGACT.assign(1,1))

    print "ip address: ", ip_addr(link)

class Flow(flow.ATFlow):
  """Doesn't do much except check SIM status."""
  def check_sim(self, link):
    command = link.process(at.QSS.query())
    qss = command.getData( )
    self.log.info("sim status %r" % (qss, ))
    return qss

  def flow(self, req):
    self.log.info("do stuff with request here. %r" % req )
    req.io.setTimeout( 3 )
    req.sim_status = self.check_sim(req)
    print "SIM ENABLED: %s" % req.sim_status.status

class FlowTool(object):
  Flow = None
  def __init__(self, link, flows, opts):
    self.flows   = flows
    self.session = flow.Session(link, self)
    #self.args, self.options = 

  def selectFlow(self, name, options={}):
    self.Flow = self.flows[name]

  def runSelected(self):
    flows = self.Flow(self.session)
    log.info("starting to run flows")
    for flow in flows( ):
      flow(self.session)

  @classmethod
  def getFlows(klass):
    """Should return a dict of flows. The keys are the names of the commands, and the values are Flow objects.
    The flow objects are inspected by the tool to generate help and options
    automatically.
    """
    return { 'qss' : Flow, 'tcpatrun': TCPATRUN,
             'gsm' : PDPContext,
    }


class Application(cli.CLIApp):
  def custom_pre_run(self):
    super(type(self), self).custom_pre_run()
    logging.basicConfig( )
    self.set_logger_level(logging.getLogger(__name__))
    logging.getLogger('tool').setLevel(logging.INFO)
    #self.set_logger_level()
    self.tool = FlowTool(self.link, self.flows, (self.args, self.options))
    #self.tool.selectFlow('qss')
    self.interpret_args( )

  def set_custom_options(self):
    usage = """%prog [options] command options

    commands:
{commands}
    """
    cmd_help = [ ]
    self.flows = FlowTool.getFlows( )
    for cmd in self.flows:
      cmd_help.append("       %s" % cmd)
    super(type(self), self).set_custom_options()
    self.parser.set_usage(usage.format(commands="\n".join(cmd_help)))
    pass

  def interpret_args(self):
    args = list(self.args)
    flow = None
    try:
      flow = args.pop( )
      self.tool.selectFlow(flow)
    except (IndexError, KeyError), e:
      if flow not in [ '', 'help', 'ls', 'list' ]:
        print "unsupported flow: %r" % flow

      self.parser.print_usage( )
      sys.exit(0)

  def setup_pre_options(self):
    super(type(self), self).setup_pre_options()

  def run(self):
    self.tool.runSelected( )
    


if __name__ == '__main__':
  app = Application( )
  app( )

#####
# EOF
