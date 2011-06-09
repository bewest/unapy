
"""

The AT Reference guide provides Telit's implementation of the 3GPP TS27
series.  It applies to the GE865-QUAD series.

"""

from core import *
import at

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  import core
  doctest.testmod(core)
  doctest.testmod(at)

#####
# EOF
