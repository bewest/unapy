import logging

logger = logging.getLogger(__name__)

EXAMPLE_RESPONSE = "AT\r\r\nOK\r\n"

class Response(object):
  """
  Basic Response to the AT commands

  >>> Response('AT\\r\\r\\nOK\\r\\n').isOK()
  True
  >>> Response('AT+\\r\\r\\nERROR\\r\\n').isOK()
  False

  """
  def __init__(self, raw):
    self.raw = raw
    self.lines = raw.splitlines()

  def isOK(self):
    if 'OK' == self.lines[-1]:
      return True
    return False

  def getError(self):
    if not self.isOK():
      return self.lines[-1]

  def getData(self):
    if self.isOK():
      lines = list(self.lines)
      lines.pop()
      return "\n".join(lines)
    return None

  def __repr__(self):
    comps = [ str(type(self)),
              "   str: %s" % self.raw,
              "  isOK: %s" % self.isOK(), ]
    if self.isOK():
      comps.append("length: %s" % len(self.getData()))
    else:
      comps.append("no data")
    return '\n'.join(comps)

class Command(object):
  """
    Your basic AT command.

    >>> Response("AT\\r\\r\\nOK\\r\\n").isOK()
    True

    >>> c = Command()
    ... c.parse("AT\\r\\r\\nOK\\r\\n")
    ... assert(c.response != None)
  """

  __raw__      = None
  __timeout__  = None
  response     = None

  class __Response__(Response): pass
  
  def __init__(self):
    self.response = None

  def format(self):
    """Returns formatted command."""
    return bytearray("AT\r")

  def parse(self, raw):
    """Returns a response, sets self.response to a subclass of Response."""
    self.__raw__  = raw
    self.response = self.__Response__(self.__raw__)
    return self.response

  def __repr__(self):
    comp = [ str(type(self)), '  msg: %s' % self.format(),
             '  response: %r' % self.response ]
    return '\n'.join(comp)

class ATCommand(Command):
  """
  Example of an error
  ~~~~~~~~~~~~~~~~~~~
  AT+
  """
  sep = '+'
  pre = 'AT'
  cmd = ''

  def format(self):
    return bytearray("%s\r" % ( ''.join([ self.pre, self.sep, self.cmd ]) ))

# XXX:bewest.2011-05: This would be better off in ruby because you can have
# methods with question marks.
# XXX:bewest.2011-05: Would probably be better with some kind of metaclass
# trickery that I've forgotten how to do.
#
"""
Ideally you could define stuff like this:
class CMEE(FancyCommand):
  cmd = 'CMEE'
  class query:
    def decode(self, mesg):
      pass
  class assign:
    def decode(self, mesg):
      pass

'''AT+CMEE?

+CMEE: 2

OK
'''


'''AT+CMEE=2

OK
'''

"""

EXAMPLE_OK     = '''AT\r\r\nOK\r\n'''
EXAMPLE_ERROR  = '''AT+\r\r\nERROR\r\n'''
EXAMPLE_ASSIGN = '''AT+CMEE=2\r\r\nOK\r\n'''

class Queryable(ATCommand):
  """
  >>> Queryable().parse(EXAMPLE_OK).isOK()
  True

  >>> str(Queryable().format())
  'AT+?\\r'
  """

  @staticmethod
  def query(klass):
    """Return an instance of the command configured for querying."""
    command = klass()
    return command

  def format(self):
    head = ''.join([ self.pre, self.sep, self.cmd ])
    tail = '?'
    cmd  = ''.join([head, tail])
    return bytearray("%s\r" % cmd)

class Settable(ATCommand):
  """
  >>> Settable(1).parse(EXAMPLE_OK).isOK()
  True

  >>> str(Settable(1).format())
  'AT+=1\\r'

  """

  # Copied from __init__
  args = [ ]
  kwds = { }

  """The tail is used as the string to format args and kwds.
  """
  tail = "{0}"

  def __init__(self, *args, **kwds):
    self.args = args
    self.kwds = kwds

  def format(self):
    """
      >>> str(Settable(1).format())
      'AT+=1\\r'
    """
    head = ''.join([ self.pre, self.sep, self.cmd ])
    tail = self.tail.format(*self.args, **self.kwds)
    cmd  = '='.join([head, tail])
    return bytearray("%s\r" % cmd)

class WellDefinedCommand(object):
  pass

class CMEE(Queryable):
  """
  >>> str(CMEE.query().format())
  'AT+CMEE?'

  >>> str(CMEE.assign(2).format())
  'AT+CMEE=2'
  """
  cmd = 'CMEE'

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
