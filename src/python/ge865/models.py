import logging

logger = logging.getLogger(__name__)

from commands import at

class _dumbLink(object):
  def process(self, command):
    command.parse('')
    return command


class Device(object):
  """A device contains manufacturer, serial info, etc...

  It's a safe base class for any high level feature set.  Obtaining
  information about a device is always a safe set of operations, and a
  particularly easy one to group.
  """
  __cache__ = { }
  link = None
  __attrs__ = { 'manufacturer': at.GMI,
                'model': at.GMM,
                'serial': at.GSN,
                'capabilities': at.GCAP,
                'revision': at.GMR, }
  def __init__(self, link):
    self.link = link
    self.__fetch__()

  def __repr__(self):
    l = ['### %r' % self.__class__ ]
    for k, v in self.__cache__.iteritems():
      l.append(' -- %20s %50s' % (k, v))
    return '\n'.join(l)

  def __fetch__(self):
    d = { }
    for k, v in self.__attrs__.iteritems():
      d[k] = getattr(self, k)
    return d
    
  def __getattr__(self, name):
    if name in self.__attrs__:
      data = self.__cache__.get(name,
               self.link.process(self.__attrs__[name]( )).getData( ))
      if name not in self.__cache__:
        self.__cache__[name] = data
      return data
    raise AttributeError("%s")
   
  def manufacturer(self):
    r = self.__cache__.get( 'manufacturer',
        self.link.process(at.GMI()).getData())
    if 'manufacturer' not in self.__cache__:
      self.__cache__['manufacturer'] = r
    return r


class Socket(Device):
  pass

class SIM(Device):
  pass

class PDP(object):
  def __init__(self, link, ):
    pass

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
