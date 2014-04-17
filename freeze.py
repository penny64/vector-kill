from distutils.core import setup

import py2exe

setup(windows=[{'script': 'vectorkill.py'}],
               options = {"py2exe": {"packages": []}})