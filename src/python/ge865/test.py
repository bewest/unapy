
import unittest
import doctest
import sys

import link, commands, models


if __name__ == '__main__':
  MODS = [ link, commands.core, commands.at, models ]
  suite  = unittest.TestSuite( )
  for mod in MODS:
    doctest.testmod(mod)
    #suite.addTest(doctest.DocTestSuite(mod))
  # runner = unittest.TextTestRunner( )
  #runner.run(suite)
  #unittest.defaultTestLoader.loadTestsFromTestCase(suite)
  #unittest.main(argv=sys.argv, )

#####
# EOF
