
import unittest
import doctest
#from ge865 import command, link

import link, commands, models


if __name__ == '__main__':
  MODS = [ link, commands, models ]
  suite  = unittest.TestSuite( )
  for mod in MODS:
    suite.addTest(doctest.DocTestSuite(mod))
  runner = unittest.TextTestRunner( )
  runner.run(suite)

#####
# EOF
