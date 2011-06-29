
from util import Loggable
import link

class IoProcessor(link.AtProcessor):
  """
  A file like object implementing a callable that callable that calls
  self.process.

  :term:`io` should be an :class:`AtProcessor` (an object with a process method that expects to
  process :term:`core`
  """
  """An object with a process method. (an AtProcessor)"""
  io = None
  def __init__(self, io):
    self.io      = io
    super(IoProcessor, self).__init__()

  def read(self):
    return self.io.read()

  def readline(self):
    return self.io.readline( )

  def readlines(self):
    return self.io.readlines( )

  def write(self, msg):
    return self.io.write(msg)

  def __call__(self, command):
    return self.process(command)

class Session(IoProcessor):
  io      = None
  handler = None

  def __init__(self, io, handler):
    self.io      = io
    self.handler = handler
    self.process = IoProcessor(io)


class BaseFlow(Loggable):
  """A Flow is a class implementing a callable.  The class is initialized
  with the session at the start of the connection, and is expected to return
  a list of flows to run when it is called.

  The session object is an ATCommand processor, and useful for passing state
  between flows.
  This implementation simply executes the flow method once before exiting the
  session.
  """
  "Set during __init__."
  session = None
  def __init__(self, session):
    """
    sets self.session
    """
    self.session = session
    self.getLog( )
  def __call__(self):
    yield self.flow
    raise StopIteration

  def flow(self, req):
    """
    Example flow: send a message, read input.
    You should write your own.
    """
    io = req.io
    #io.throwError( )
    #io.setTimeout(2)
    # first command
    self.log.debug( "writing command")
    io.write('XXXXHELLO WORLD\n')
    self.log.debug( "reading response")
    #msg = self.rfile.readline( )
    msg = io.readline( )
    #msg = io.readlines()
    io.write( "OK: %s" % msg )
    self.log.debug("got message: %s" % msg )

    # second command
    io.write('second command\n')
    msg = io.readline( )
    self.log.debug("got message 2: %s" % msg )
    io.write( "OK: %s" % msg )

    # third command
    io.write('third command:\n')
    msg = io.readlines( )
    io.write( "OK: %s" % msg )


    io.write("bye")
    self.log.debug("done with flow")

    return msg
  
class ATFlow(BaseFlow):

  def process(self, command):
    self.log.debug("%r.process" % (self))
    return self.session.process(command)


#####
# EOF
