

import logging
import sys
import ge865
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)




if __name__ == '__main__':
  logging.info('hello world')
  logging.debug('hello world')
  #ge865.test('/dev/ttyUSB0')

  link = ge865.Link('/dev/ttyUSB0')
  command = link.process(ge865.commands.at.CMEE.assign(2))
  command = link.process(ge865.commands.at.GCAP())
  command = link.process(ge865.commands.at.SS())
  logging.info(command)

#####
# EOF
