#!/usr/bin/env python

from distutils.core import setup

setup(
  name             = 'pbmodem',
  version          = '0.01',
  description      = 'AT 3gpp commands',
  author           = 'Ben West',
  author_email     = 'bewest@gmail.com',
  packages         = ['pbmodem',],
  install_requires = [ 'pyserial', 'gevent', 'python-messaging'
  ]
)



