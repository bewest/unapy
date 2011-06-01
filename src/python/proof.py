from pprint import pprint, pformat


class Simple(object):
  """
    >>> Simple().a
    'S'
  """
  a = 'S'
  target = 'target'
  
class Custom(Simple):
  """
    >>> Custom().a
    'S'
    >>> Custom().target
    'custom'
  """
  target = 'custom'


class Rich(Simple):
  """
    >>> Rich().a
    'rich'
    >>> Rich().target
    'target'
    >>> # Rich().rich().a
    'rich'
    >>> # Rich().rich().target
    'custom'
  """
  a = 'rich'
    
  __rich__ = Custom

class ProxyRich(Rich):
  """
  There is a way to do this using straight inheritance, but it doesn't feel
  as nice.

  It requires intantiating an object, and then creating a new class
  dynamically.

    >>> ProxyRich().rich().a
    'rich'
    >>> ProxyRich().rich().target
    'custom'

    >>> class Foo(ProxyRich):
    ...   a = 'foo'

    >>> Foo().a
    'foo'
    >>> Foo().rich().a
    'foo'
  """
  def __init__(self):
    # Produces a new class every time it's called, by every instance.
    clname = '.'.join([self.__class__.__name__, self.a])
    self.rich = type(clname, (self.__rich__, ), {'a':self.a})




class RenamingType(type):
  """
    Using a metaclass allows us to customize the creation of this class when
    python starts and first loads this module.

    Subclassing types means our instances are classes.
    This is the only advisable way to call both __new__ and __init__
  """
  def __new__(meta, name, bases, dct):
    """Mind there is no inheritance yet since python is in the process of
    constructing our graphs.
      * meta - AKA called clss or klass elsewhere, is this class itself as an
        instance of type.
        Usually class methods are bound to the class as an object, but calling
        methods on meta won't result in any of python's usual implicit
        argument passing.
      * name - name of the new class (variable it is being bound to?)
      * bases - a tuple of base classes (mostly just one)
      * dct - the __dict__ of our about to be created type's __dict__.  If you
        could access the uppermost __dict__ of the class without any
        inheritance in place, this is the result.
    """
    newdict = dct.copy()
    newdict['a'] = name
    t = type.__new__(meta, name, bases, newdict)
    pprint(['__new__', 'meta', meta, 'name', name,
            'bases', bases, 'newdict', newdict])
    """
    """
    return t

  def __init__(clss, name, bases, dct):
    """clss - an instance of a type, The class we've already created, which we
    may now customize as a class object.
    Since it's a class object, python's inheritence makes all of it's
    inherited member's available for tweaking now.

    dct is a copy of it's __dict__.

    """
    newdict = dct.copy()
    newdict['a'] = name
    clss.a = name
    clname = '.'.join([clss.__class__.__name__, name])
    clss.rich = type(clname, (clss.__rich__, ), {'a':name})
    print "XXX", clss.test('METACLASS CALL')
    super(RenamingType, clss).__init__(name, bases, newdict)
    pprint(['__init__', 'clss', clss, 'name', name,
            'bases', bases, 'newdict', newdict])
    """
    """


class MyRenamedAttr(Simple):
  """
    >>> MyRenamedAttr().a
    'MyRenamedAttr'
    >>> MyRenamedAttr().target
    'target'
  """
  __metaclass__ = RenamingType
  class __rich__(Custom): pass

  @classmethod
  def test(klass, arg):
    return 'CLASSMETHOD %s ' % arg




class MyRenAttr(MyRenamedAttr):
  """
    >>> MyRenAttr().a
    'MyRenAttr'
    >>> MyRenAttr().target
    'target'

    >>> MyRenAttr.rich().a
    'MyRenAttr'
    >>> MyRenAttr.rich().target
    'custom'
  """

class MyRenAttrII(MyRenamedAttr):
  """
    >>> MyRenAttrII().a
    'MyRenAttrII'
    >>> MyRenAttrII().target
    'target'

    >>> MyRenAttrII.rich().a
    'MyRenAttrII'
    >>> MyRenAttrII.rich().target
    'SUCCESS'

    >>> MyRenAttrII().rich().a
    'MyRenAttrII'
    >>> MyRenAttrII().rich().target
    'SUCCESS'

    >>> MyRenAttrII().rich.a
    'MyRenAttrII'
    >>> MyRenAttrII().rich.target
    'SUCCESS'

    >>> MyRenAttrII.rich.a
    'MyRenAttrII'
    >>> MyRenAttrII.rich.target
    'SUCCESS'
  """
  class __rich__(Simple):
    target = "SUCCESS"

  @classmethod
  def test(klass, arg):
    return 'SPECIAL CLASSMETHOD %s ' % arg


class NullMeta(type):
  def __new__(meta, name, bases, dct):
    newdict = dct.copy()
    t = type.__new__(meta, name, bases, newdict)
    return t

  def __init__(clss, name, bases, dct):
    newdict = dct.copy()
    super(AttrMeta, clss).__init__(name, bases, newdict)



if __name__ == '__main__':
  import doctest
  doctest.testmod()

