#!/usr/bin/env python

from setuptools import setup

setup(
  name             = 'unapy',
  version          = '0.01',
  description      = 'AT 3gpp commands',
  author           = 'Ben West',
  author_email     = 'bewest@gmail.com',
  license          = 'MIT',
  packages         = ['unapy',],
  install_requires = [ 'pyserial', 'gevent', 'python-messaging'
  ]
)



