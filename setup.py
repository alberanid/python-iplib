#!/usr/bin/env python

import sys
from distutils.core import setup


long_desc = """You can use this Python module to convert amongst many
different notations and to manage couples of address/netmask
in the CIDR notation.
"""

classifiers = """\
Development Status :: 4 - Beta
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: No Input/Output (Daemon)
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
License :: OSI Approved :: BSD
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Networking
Topic :: Internet
Topic :: Utilities
"""

params = {'name': 'iplib',
    'version': '1.1',
    'description': 'convert amongst many different IPv4 notations',
    'long_description': long_desc,
    'author': 'Davide Alberani',
    'author_email': 'da@erlug.linux.it',
    'maintainer': 'Davide Alberani',
    'maintainer_email': 'da@erlug.linux.it',
    'url': 'http://erlug.linux.it/~da/soft/iplib/',
    'license': 'BSD',
    'py_modules': ['iplib'],
    'scripts': ['./bin/cidrinfo', './bin/ipconv', './bin/nmconv']}


if sys.version_info >= (2, 1):
    params['keywords'] = ['ip', 'address', 'quad', 'dot', 'notation',
                'binary', 'octal', 'hexadecimal', 'netmask', 'cidr', 'internet']
    params['platforms'] = 'any'

if sys.version_info >= (2, 3):
    params['download_url'] = 'http://erlug.linux.it/~da/soft/iplib/'
    params['classifiers'] = filter(None, classifiers.split("\n"))


setup(**params)


