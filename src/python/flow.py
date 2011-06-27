
from ge865 import cli

import sys
import logging
log = logging.getLogger('tool')

from ge865 import cli
from ge865 import flow
from ge865.commands import at
from ge865 import network

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

def find_flows( ):
  return [ Flow ]



class FlowTool(object):
  def __init__(self, link, flows):
    self.flows   = flows
    self.session = flow.Session(link, self)

  def listFlows(self):
    return self.flows

  def selectFlow(self, name, options={}):
    self.select = self.flows[name]

  def runSelected(self):
    flows = self.select(self.session)
    log.info("starting to run flows")
    for flow in flows( ):
      flow(self.session)

def getFlows( ):
  return { 'qss' : Flow }


class Application(cli.CLIApp):
  def custom_pre_run(self):
    super(type(self), self).custom_pre_run()
    logging.basicConfig( )
    self.set_logger_level(logging.getLogger(__name__))
    #self.set_logger_level()
    self.tool = FlowTool(self.link, getFlows( ))
    #self.tool.selectFlow('qss')
    self.interpret_args( )

  def set_custom_options(self):
    usage = """%prog [options] command options

    commands:
      help
      qss
    """
    self.flows = getFlows( )
    super(type(self), self).set_custom_options()
    self.parser.set_usage(usage)
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
