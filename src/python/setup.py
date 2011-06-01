#!/usr/bin/env python

from distutils.core import setup

setup(name='ge865',
      version='0.01',
      description='AT 3gpp commands',
      author='Ben West',
      author_email='bewest@gmail.com',
      packages=['ge865',],
      install_requires=['pyserial']
     )



