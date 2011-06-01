import logging
import re
from pprint import pprint

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
              "  isOK: %s" % self.isOK(),
              "  data: %s" % self.getData(), ]
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
    self.args = map(str, args)
    self.kwds = kwds

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

class NullQueryable(Queryable):
  cmd = None

class NullSettable(Settable):
  cmd = None

class NullInspectable(Inspectable):
  cmd = None

class MetaCommand(type):
  def __new__(meta, name, bases, dct):
    cmd = name.upper()
    if dct.get('cmd', None) is not None:
      cmd = dct['cmd']
    newdict = dct.copy()
    newdict['cmd']    = cmd
    """
    newdict['query']  = meta.glom(meta.getQuery(cmd, dct),
                        dct, ['sep', 'pre'])
    newdict['assign'] = meta.glom(meta.getAssign(cmd, dct),
                        dct, ['sep', 'pre'])
    newdict['inspect'] = meta.glom(meta.getInspect(cmd, dct),
                        dct, ['sep', 'pre'])

    """
    t = type.__new__(meta, name, bases, newdict)

    """
    print "__new__"
    pprint(['t', t, 'meta', meta, 'name', name,
            'bases', bases, 'newdict', newdict])
    """

    return t

  def __init__(clss, name, bases, dct):
    newdict = dct.copy()
    #print "__init__"
    #pprint(['before', clss])
    super(MetaCommand, clss).__init__(name, bases, newdict)
    clss.__fix__()
    """
    pprint(['clss', clss, 'name', name,
            'bases', bases, 'newdict', newdict])
    """

  @staticmethod
  def glom(target, src, props):
    for f in props:
      if src.get(f, None) is not None:
        setattr(target, f, src.get(f))
    return target
      


  @staticmethod
  def getQuery(name, dct):
    class query(dct.get('query', NullQueryable)):
      cmd = name
    if '__query__' in dct:
      query.__Response__ = dct['__query__']
    return query

  @staticmethod
  def getAssign(name, dct):
    class assign(dct.get('assign', NullSettable)):
      cmd = name
    if '__assign__' in dct:
      assign.__Response__ = dct['__assign__']
    return assign

  @staticmethod
  def getInspect(name, dct):
    class inspect(dct.get('inspect', NullInspectable)):
      cmd = name
    if '__inspect__' in dct:
      inspect.__Response__ = dct['__inspect__']
    return inspect


class WellDefinedCommand(ATCommand):
  __metaclass__ = MetaCommand
  __variants__  = [ 'query', 'assign', 'inspect' ]

  class query(NullQueryable): pass
  class assign(NullSettable): pass
  class inspect(NullInspectable): pass

  @classmethod
  def __fix__(klass):
    for i in klass.__variants__:
      clname = '%s.%s' % (klass.cmd, i)
      setattr(klass, i,
              type(clname, (getattr(klass, i), ),
                  {'cmd':klass.cmd}))

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

class CGDCONT(WellDefinedCommand):
  """
    XXX: Broken.

    This was experimental.
    Example of how to replace the query parsing logic.
    WellDefinedCommand's copy __query__ and __assign__ to the query and
    assign's __Response__ field's respectively.
    >>> # type(CGDCONT.query().parse(EXAMPLE_CGDCONT).getData())
    <type 'list'>

    >>> # CGDCONT.query().parse(EXAMPLE_CGDCONT).getData()[0]
    [1, 'IP', 'webtrial.globalm2m.net', '', 0, 0, ['0']]

  """
  class __query__(Response):
    def getData(self):
      results = [ ]
      if self.isOK():
        for line in self.lines:
          if line.startswith('+CGDCONT: '):
            parts = line.replace('"', '').split('+CGDCONT: ')
            parts = parts[-1].split(',')
            cid      = int(parts[0])
            pdp_t    = parts[1]
            apn      = parts[2]
            pdp_addr = parts[3]
            d_comp   = int(parts[4])
            h_comp   = int(parts[5])
            params   = parts[5:]
            
            results.append([ cid, pdp_t, apn, pdp_addr, d_comp, h_comp,
                             params ])
      return results

      
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
