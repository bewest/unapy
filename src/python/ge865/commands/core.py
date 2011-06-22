import logging
import re
from pprint import pprint
from collections import namedtuple
import types

logger = logging.getLogger(__name__)

EXAMPLE_RESPONSE = "AT\r\r\nOK\r\n"
EXAMPLE_CONNECT_RESPONSE = '\r\r\nCONNECT\r\n'
EXAMPLE_SD='AT#SD=1, 0, 80, www.transactionalweb.com\r\r\nCONNECT\r\n'

EXAMPLE_IP_REPLY='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n\r\nOK\r\n'
EXAMPLE_IP_to_python='AT+CGPADDR=1\r\r\n+CGPADDR: 1,"10.215.15.91"\r\n'
EXAMPLE_CGPADDR = 'AT+CGPADDR=?\r\r\n+CGPADDR: (1,2,3)\r\n\r\nOK\r\n'
EXAMPLE_OK     = '''AT\r\r\nOK\r\n'''
EXAMPLE_ERROR  = '''AT+\r\r\nERROR\r\n'''
EXAMPLE_ERROR_CARRIER  = '''AT+\r\r\nNO CARRIER\r\n'''
EXAMPLE_ASSIGN = '''AT+CMEE=2\r\r\nOK\r\n'''
EX_GCAP='''AT+GCAP\r\r\n+GCAP: +CGSM,+DS,+FCLASS,+MS\r\n\r\nOK\r\n'''

def to_python(msg, Tuple=tuple):
  """

  I've seen a lot of code and commentary out there saying you need regexp to
  handle all this.

      Some people, when confronted with a problem, think
      "I know, I'll use regular expressions." Now they
      have two problems.
      
      - JWZ maybe? http://regex.info/blog/2006-09-15/247


    >>> len(to_python(EXAMPLE_IP_to_python))
    1
    >>> to_python(EXAMPLE_IP_to_python)
    [(1, '10.215.15.91')]

    >>> to_python(EXAMPLE_CGPADDR)
    [(1, 2, 3)]

    >>> to_python(EX_GCAP)
    [('+CGSM', '+DS', '+FCLASS', '+MS')]


  """
  lines  = msg.strip().splitlines()
  result = [ ]
  r      = ( )
  for l in lines:
    parts = l.split(': ')
    if len(parts) > 1:
      text = ''.join(parts[1:]
               ).replace('"', '').replace("'", "")
      parts = text.split(',')
      r = tuple(parts)
      if len(parts) > 1:
        try:
          r = ( int(parts[0]), ) + tuple(parts[1:])
        except ValueError, e:
          parts = text.replace('(', '').replace(')', '').split(',')
          try:
            r = tuple(map(int, parts))
          except ValueError, e:
            r = tuple(map(str, parts))
          
      result.append(Tuple(r))

  return result

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
    self.lines = [ l.strip( ) for l in raw.splitlines() ]
    if self.isOK( ):
      self.head = self.lines[0]
      self.body = self.lines[1:-1]
      self.tail = self.lines[-1]

  def isOK(self):
    last = self.lines[-1]
    if last in ['OK', 'CONNECT']:
      return True
    return False

  def getError(self):
    if not self.isOK():
      return self.lines[-1].strip( )

  def getData(self):
    if self.isOK():
      return "\n".join(self.body)
    return None

  def __repr__(self):
    comps = [ '### %s'        % str(type(self)),
              " -- len  : %s"   % len(self.raw),
              " -- isOK : %s"  % self.isOK( ),
              " -- data : %s"  % self.getData( ),
              " -- error: %s" % self.getError( ) ]
    if not self.isOK():
      comps.append(" -- no data")
    return '\n'.join(comps)

class ConnectedResponse(Response):
  """
    XXX: not used
    >>> ConnectedResponse(EXAMPLE_CONNECT_RESPONSE).isOK()
    True

  """
  def isOK(self):
    if self.lines[-1].startswith('CONNECT'):
      return True
    return False

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
  data         = None
  _fields   = None
  _Tuple        = tuple
  _ex_ok = '''AT\r\r\nOK\r\n'''

  class __Response__(Response): pass
  
  def __init__(self):
    self.response = None
    if self._fields is not None:
      name = 'ATResponse%s' % self.cmd
      self._Tuple = namedtuple(name, self._fields)

  def Tuple(self, args):
    try:
      return  self._Tuple(list(args))
    except TypeError, e:
      return  self._Tuple(*list(args))

    
  def format(self):
    """Returns formatted command.
      >>> str(Command().format())
      'AT\\r'

    """
    return bytearray("AT\r")

  def parse(self, raw):
    """Returns a response, sets self.response to a subclass of Response."""
    self.__raw__  = raw
    self.response = self.__Response__(self.__raw__)
    if self.response.isOK():
      self.data = self.getData()
    return self.response

  def __repr__(self):
    comp = [ '### %s'           % str(type(self)),
             ' -- CMD     : %s' % self.format( ),
             ' -- response: %r' % self.response ]
    return '\n'.join(comp)

  def getData(self):
    if self.response.isOK():
      return to_python(self.response.getData(), Tuple=self.Tuple)
    return None

class ATCommand(Command):
  """
  Example of an error
  ~~~~~~~~~~~~~~~~~~~
  AT+

  >>> ATCommand().parse(EXAMPLE_OK).isOK()
  True

  >>> ATCommand().parse(EXAMPLE_CONNECT_RESPONSE).isOK()
  True

  >>> not ATCommand().parse(EXAMPLE_ERROR).isOK()
  True

  >>> not ATCommand().parse(EXAMPLE_ERROR_CARRIER).isOK()
  True

  """
  sep = '+'
  pre = 'AT'
  cmd = ''
  _ex_ok = '''AT\r\r\nOK\r\n'''
  def __init__(self):
    """
    If cmd is None rename it using the class's name.
    This class is configured not to do this by default, making it a poor
    choice for this logic.
    cmd to None in order for this to work.
    """
    if self.cmd is None:
      self.cmd = self.__class__.__name__
    super(ATCommand, self).__init__( )

  def format(self):
    return bytearray("%s\r" % ( ''.join([ self.pre, self.sep, self.cmd ]) ))

class NoneCommand(ATCommand):
  cmd = None

class SimpleCommand(NoneCommand):
  """
    A subclassable command configured to rename itself according to class
    name.
    >>> str(SimpleCommand().format( ))
    'AT+SimpleCommand\\r'

    >>> class Foo(SimpleCommand): pass
    
    >>> str(Foo().format( ))
    'AT+Foo\\r'

    >>> Foo().parse("OK").isOK()
    True

    >>> class Bar(SimpleCommand): pass

    >>> str(Bar().format( ))
    'AT+Bar\\r'
      
  """

  def getData(self):
    lines = self.response.lines
    return '\n'.join(lines[1:-1]).strip()


# XXX:bewest.2011-05: This would be better off in ruby because you can have
# methods with question marks.

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
    self.args = map(str, args)
    self.kwds = kwds
    super(ATCommand, self).__init__()

  def format(self):
    """
      >>> str(Settable(1).format())
      'AT+=1\\r'

    """
    head = ''.join([ self.pre, self.sep, self.cmd ])
    tail = ', '.join(self.args)
    cmd  = '='.join([head, tail])
    return bytearray("%s\r" % cmd)

class Inspectable(Settable):
  def format(self):
    """
      >>> str(Inspectable(1).format())
      'AT+=?1\\r'
      >>> str(Inspectable().format())
      'AT+=?\\r'

    """
    head = ''.join([ self.pre, self.sep, self.cmd ])
    tail = ', '.join(self.args)
    cmd  = '=?'.join([head, tail])
    return bytearray("%s\r" % cmd)

class IdentCommand(Settable):
  cmd = 'I'
  sep = ''
  def format(self):
    """
      >>> str(IdentCommand(1).format())
      'ATI1\\r'

    """
    head = ''.join([ self.pre, self.sep, self.cmd ])
    tail = self.tail.format(*self.args, **self.kwds)
    cmd  = ''.join([head, tail])
    return bytearray("%s\r" % cmd)

class ConnectedCommand(ATCommand):
  '''
  XXX: not used
    >>> ConnectedCommand().parse(EXAMPLE_CONNECT_RESPONSE).isOK()
    True

  '''
  class __Response__(ConnectedResponse): pass

class NullQueryable(Queryable):
  cmd = None

class NullSettable(Settable):
  cmd = None

class NullInspectable(Inspectable):
  cmd = None

class MetaCommand(type):
  def __new__(meta, name, bases, dct):
    """Called when initializing the type object that creates a class type.
    None of python's inheritence is available.  `meta` is an unbound
    MetaCommand.
      * name - name of to be type/class
      * bases
      * dct
    Returns a class.
    """
    cmd = name.upper()
    if dct.get('cmd', None) is not None:
      cmd = dct['cmd']
    newdict = dct.copy()
    newdict['cmd']    = cmd
    t = type.__new__(meta, name, bases, newdict)
    return t

  def __init__(clss, name, bases, dct):
    """clss is a class (an instance of a type).
    It is the object representing the class that we are initializing and all
    of python's inheritence is available.

    We use this trick to call clss.__fix__, which gives the class an
    opportunity to juggle some things around.
    Returns initialized class (a type object).
    """
    newdict = dct.copy()
    #print "__init__"
    #pprint(['before', clss])
    super(MetaCommand, clss).__init__(name, bases, newdict)
    clss.__fix__()


class WellDefinedCommand(ATCommand):
  __metaclass__ = MetaCommand
  __variants__  = [ 'query', 'assign', 'inspect' ]

  class query(NullQueryable): pass
  class assign(NullSettable): pass
  class inspect(NullInspectable): pass

  @classmethod
  def __fix__(klass):
    """ Called during the creation of the class.  (During the class'
    __init__.)

    Allows us to rename our variant commands appropriately.
    """
    # Make a new type called cmd.variant
    for i in klass.__variants__:
      clname = '%s.%s' % (klass.cmd, i)
      setattr(klass, i,
              type(clname, (getattr(klass, i), ),
                  { 'cmd'    : klass.cmd
                  , 'sep'    : klass.sep
                  , '_Tuple' : klass._Tuple
                  , 'Tuple'  : klass.Tuple.im_func
                  , '_fields': klass._fields
                  }))

class Foo(WellDefinedCommand):
  """
  >>> str(Foo.query().format())
  'AT+FOO?\\r'

  >>> str(Foo.assign(1).format())
  'AT+FOO=1\\r'

  >>> str(Foo.inspect(1).format())
  'AT+FOO=?1\\r'
  >>> str(Foo.inspect().format())
  'AT+FOO=?\\r'
  """
  pass

class SoleItemCommand(ATCommand):
  """
  Our getData returns a single named tuple.
  """
  def getData(self):
    data = super(ATCommand, self).getData( )
    if data is not None and len(data) == 1:
      return data.pop( )
    return None

class WellDefinedSoleCommand(WellDefinedCommand, SoleItemCommand):
  class query(NullQueryable, SoleItemCommand): pass
  class assign(NullSettable, SoleItemCommand): pass
  class inspect(NullInspectable, SoleItemCommand): pass

class PoundSepCom(ATCommand):
  """
    >>> str(PoundSepCom().format())
    'AT#\\r'

  """
  sep = '#'

#class PoundSeparatedCommand(PoundSepCom):
class PoundSeparatedCommand(WellDefinedCommand):
  """

    >>> class MyCom(PoundSeparatedCommand):
    ...   cmd = 'FOO'

    >>> str(MyCom().format())
    'AT#FOO\\r'

    >>> str(MyCom.query().format())
    'AT#FOO?\\r'

    >>> str(MyCom.assign().format())
    'AT#FOO=\\r'

    >>> str(MyCom.inspect().format())
    'AT#FOO=?\\r'

  """
  sep = '#'
  class query(NullQueryable):
    sep = '#'

  class assign(NullSettable):
    sep = '#'

  class inspect(NullInspectable):
    sep = '#'


class FooPound(PoundSeparatedCommand):
  """
    >>> str(FooPound.query().format())
    'AT#FOOPOUND?\\r'

  """

EXAMPLE_CGDCONT = """AT+CGDCONT?\r\r\n+CGDCONT: 1,"IP","webtrial.globalm2m.net","",0,0\r\n+CGDCONT: 2,"IP","wap.cingular","",0,0\r\nOK\r\n"""

class BadNamed(WellDefinedCommand):
  """
  XXXX: Don't use.  Just here to test things.
  >>> str(BadNamed().format())
  'AT+Foo\\r'

  >>> str(BadNamed.assign(1).format())
  'AT+Foo=1\\r'

  >>> str(BadNamed.query().format())
  'AT+Foo?\\r'

  """
  cmd = 'Foo'

class CMEE(WellDefinedCommand):
  """
  >>> str(CMEE.query().format())
  'AT+CMEE?\\r'

  >>> str(CMEE.assign(2).format())
  'AT+CMEE=2\\r'

  """
  cmd = 'CMEE'

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
