from distutils.core import setup

import py2exe

setup(windows=[{'script': 'vectorkill.py'}],
               options={"py2exe": {"packages": [],
                                   "optimize": 2,
                                   "excludes": ['doctest', 'pdb', '_ssl',  'pyreadline', 'doctest', 'locale', 
                                                'optparse', 'pickle', 'calendar']}},
               zipfile=None)