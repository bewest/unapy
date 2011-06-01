

import logging
import sys
import ge865
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ge865.logger.setLevel(logging.DEBUG)
from ge865.commands import at

def check_sim(link):
  command = link.process(at.QSS.query())
  print command.response.getData()

def random(link):
  command = link.process(at.CMEE.assign(2))
  command = link.process(at.GCAP())
  command = link.process(at.SS())



if __name__ == '__main__':
  logging.info('hello world')
  logging.debug('hello world')
  #ge865.test('/dev/ttyUSB0')

  link = ge865.Link('/dev/ttyUSB1')
  check_sim(link)

#####
# EOF
