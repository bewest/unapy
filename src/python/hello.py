

import logging
import sys
import ge865
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
  logging.info('hello world')
  logging.debug('hello world')
  ge865.test('/dev/ttyUSB0')

#####
# EOF
