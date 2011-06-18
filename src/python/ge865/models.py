import logging

logger = logging.getLogger(__name__)

from commands import at

class _dumbLink(object):
  def process(self, command):
    command.parse('')
    return command


class Feature(object):
  device = None
  name   = 'Feature'
  __attrs__ = {'hello': at.ATCommand }
  __cache__ = { }
  def __init__(self, device):
    self.setDevice(device)
    self.refresh( )
  def setDevice(self, device):
    self.device = device
  def getDevice(self):
    return self.device
  def process(self, command):
    return self.device.link.process(command)

  def refresh(self):
    keys = self.__attrs__.keys( )
    keys.sort( )
    for k in keys:
      command = self.__cache__.get(k,
                  self.process(self.__attrs__[k]( )))
      self.__cache__[k] = command

class FakeFeature(Feature):
  """ """
  def process(self, command):
    """Assume we have a FakeListLink and add our command's __ex_ok to the
    comms list just before reading it.
    """
    self.device.link.comms.append(command.__ex_ok)
    return self.device.link.process(command)

class ModelInfo(Feature):
  """Groups a bunch of attributes as a feature against a device.

  A device contains manufacturer, serial info, etc...

  It's a safe base class for any high level feature set.  Obtaining
  information about a device is always a safe set of operations, and a
  particularly easy one to group.

  """
  __attrs__ = { 'manufacturer': at.GMI,
                'model': at.GMM,
                'serial': at.GSN,
                'capabilities': at.GCAP,
                'revision': at.GMR, }
  __cache__ = { }
  def __repr__(self):
    # Only show instantiated attributes.
    l = ['### %r' % self.__class__ ]
    for k, v in self.__fetch__().iteritems( ):
      l.append(' -- %20s %50s' % (k, v))
    return '\n'.join(l)

  def __fetch__(self):
    d = { }
    for k, v in self.__attrs__.iteritems():
      d[k] = getattr(self, k)
    return d
    
  def __getattr__(self, name):
    if name in self.__attrs__:
      command = self.__cache__.get(name,
                  self.process(self.__attrs__[name]( )))
      if name not in self.__cache__:
        self.__cache__[name] = command
      return command.getData( )
    raise AttributeError("%s has no attribute: %s" % (self, name))
   

class Device(object):
  __features__ = { 'model': ModelInfo }
  __cache__ = { }
  link = None
  def __init__(self, link):
    self.link = link

  def __repr__(self): 
    l = ['### %r' % self.__class__ ]
    for k, v in self.__features__.iteritems():
      l.append(' -- %20s %50s' % (k, v))
    return '\n'.join(l)
    
  def __getattr__(self, name):
    if name in self.__features__:
      feature = self.__cache__.get(name,
               self.inspect(self.__features__[name]))
      if name not in self.__cache__:
        self.__cache__[name] = feature
      return feature
    raise AttributeError("%s has no attribute: %r" % (self, name))

  def inspect(self, Feature):
    feature = Feature(self)
    self.__features__[feature.__class__.__name__] = feature
    #feature.setDevice(self)
    return feature

# class DeviceData
class FakeDevice(Device):
  """For testing."""
  def __init__(self):
    from link import OKExampleLink
    self.link = OKExampleLink( )



class EnablerDisabler(Feature):
  name = 'EnableDisableControl'
  __query__ = at.WellDefinedCommand
  __enabled__ = False
  def __init__(self, device):
    super(EnablerDisabler, self).__init__(device)
    self.query()
  def query(self):
    """
    """
    q = self.process(self.__query__.query( ))
    self.__enabled__ = q.getData( ) == 1
    return self.isEnabled( )
  def isEnabled(self):
    """
    """
    return self.__enabled__
  def enable(self):
    """
    """
    q = self.process(self.__query__.assign(1))
    if q.isOK( ):
      self.__enabled__ = True

  def disable(self):
    """
    """
    q = self.process(self.__query__.assign(0))
    if q.isOK( ):
      self.__enabled__ = True

  def __repr__(self):
    # Only show instantiated attributes.
    l = ['### %r' % self.__class__]
    l.append(' -- %20s %50s' % ('enabled:', self.__enabled__))
    return '\n'.join(l)


class ElementList(Feature):
  name = "ElementListControl"
  __query__    = at.WellDefinedCommand
  __elements__ = None

  def clear(self):
    self.__elements__ = None

  def query(self, clear=False):
    """
      >>> el = ElementList( FakeDevice() )
      ... el.__elements__ = [ ]
    """
    if clear:
      self.clear( )
    q = self.process(self.__query__.query( ))
    if self.__elements__ is None:
      self.__elements__ = q.getData( )
    return self.__elements__

  def elements(self, elements=None):
    """
    """
    if elements is not None:
      self.clear( )
      # XXX: This is inefficient but straightforward.
      for el in elements:
        self.setElement(el)
    return self.query( )

  def setElement(self, el):
    """
    XXX: This will throw exceptions.
    """
    q   = self.process(self.__query__.assign(*el))
    _el = q.getData( )
    assert _el == el, "In theory these should be equal."
    # update cache
    self.__elements__[_el[0]] = _el
    return _el
  

class NetworkContext(ElementList):
  __query__ = at.CGDCONT


class Socket(Device):
  pass

class SIM(Feature):
  """
  QSS
  CSIM pg 380
    read/write to SIM

  """
  name = 'Query SIM Status'
  __attrs__ = { 'status': at.QSS.query, }
  def status(self):
    status = self.__cache__['status']
    return status

  def isEnabled(self):
    return self.status( ).getData( ).status


class TCPATRUN(object):
  """
    TCPATRUN
    TCPATRUNCFG
    SMSATWL

    pg 381
  """
class EvMoni(object):
  """
  """

class SMSATRUN(object):
  """
    pg 380
    enable/disable
    list of context configs
    whitelist
    SMSATRUN
     mode = 1/0 enables[default]/disable the service
     Eval incoming SMS as AT.

    SMSATRUNCFG
      instance - "AT instance" used range 2-3, default 3
      urcmode  - 0/1 disable/enable[default] feature
      timeout  - in minutes.  module reboots if timeout expires before
                 commands finish.  default 5. 1..60
      AT instance refers to :mod:`EvMoni` service.
      See ENAEVMONICFG
      
    SMSATWL
      How SMSATRUN messages are processed are controlled by the SMS whitelist.
      The list contains a list of elements representing either passwords or
      phone number.  There can be a max of 2 numbers, with a total of 8
      elements total, numbered 1 - 8.

      An incoming text must have a special PDU format containing the password
      in the PDU header, or the sender number must match a number on the
      whitelist.

      The query syntax returns a list of (entryType, string) tuples.

      * action - 0..2
        0 - Add an element
        1 - Delete an element
        2 - Print an element
      * index - 1..8
      * entryType - 0 - Phone number, 1 - password
        [max of two password types]
      * string - either a phone number or a password

    The feature is divided into two modes, Simple and Digest
    Incoming text beginning with "AT" or "HAT" is evaled.


    Simple
    ~~~~~~
    Originating SMS address matches a number in the whitelist
    SMS coding alphabet may be 7 bit or 8 bit

    Digest
    ~~~~~~
    The SMS User Data segment must contain a header containing the MD5 digest
    of the message text using a password matching a password element in the
    whitelist.
    SMS coding alphabet must be 8 bit
    
    +--------+------+----------+--------------------+
    | Offset | Size |    Value | Description        |
    +========+======+==========+====================+
    |      0 |    3 | 0xD0D0D0 | RunAT SMS Code     |
    +--------+------+----------+--------------------+
    |      3 |    1 |        0 | Transaction ID     |
    +--------+------+----------+--------------------+
    |      4 |    1 |     0x11 | Segment 1 of 1     |
    +--------+------+----------+--------------------+
    |      5 |    1 |          | Session ID         |
    +--------+------+----------+--------------------+
    |      6 |   24 |          | Digest: B64(MD5(   |
    |        |      |          | B64(MD5(PWD)):     |
    |        |      |          | B64(MD5(MSG))))    |
    +--------+------+----------+--------------------+
    |     30 |      |          | Useful Text        |
    +--------+------+----------+--------------------+

    pg 378
  """

class PDP(object):
  def __init__(self, link, ):
    pass

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
