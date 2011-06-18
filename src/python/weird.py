#!/usr/bin/python
"""
Why does Store's test fail while Market's test passes?

Why does the error read:
**********************************************************************
File "weird.py", line 28, in __main__.Store
Failed example:
    o = Store( )
Exception raised:
    Traceback (most recent call last):
      File "/usr/lib/python2.6/doctest.py", line 1248, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.Store[0]>", line 1, in <module>
        o = Store( )
      File "weird.py", line 32, in __init__
        one = buyer.buy(Orange( ) )
      File "weird.py", line 24, in buy
        return fruit.__ex_ok
    AttributeError: 'Orange' object has no attribute '_Buyer__ex_ok'
**********************************************************************
1 items had failures:
   1 of   1 in __main__.Store
***Test Failed*** 1 failures.

What is _Buyer__ex_ok?

Answer:
http://docs.python.org/release/1.5/tut/node67.html

Don't use __ as a prefix.

"""

import doctest

class Fruit(object):
  desc = "Silly"

class Orange(Fruit):
  __ex_ok = 'This is an example.'

class Buyer(object):
  """
    
  """
  def inspect(self, fruit):
    return fruit.desc

  def buy(self, fruit):
    return fruit.__ex_ok

class Store(object):
  """
    >>> o = Store( )
  """
  def __init__( self ):
    buyer = Buyer( )
    one = buyer.buy(Orange( ) )
  
class Market(object):
  """
    >>> h = Market( )
  """
  def __init__( self ):
    buyer = Buyer( )
    one = buyer.inspect(Orange( ) )


if __name__ == '__main__':
  doctest.testmod( )

  

#####
# EOF
