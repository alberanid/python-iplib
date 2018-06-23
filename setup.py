#!/usr/bin/env python

import setuptools


long_desc = """You can use this Python module to convert amongst many
different notations and to manage couples of address/netmask
in the CIDR notation.
"""

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: No Input/Output (Daemon)
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Networking
Topic :: Internet
Topic :: Utilities
"""

params = {
    'name': 'iplib',
    'version': '1.2.1',
    'description': 'convert amongst many different IPv4 notations',
    'long_description': long_desc,
    'author': 'Davide Alberani',
    'author_email': 'da@erlug.linux.it',
    'maintainer': 'Davide Alberani',
    'maintainer_email': 'da@erlug.linux.it',
    'url': 'https://github.com/alberanid/python-iplib',
    'license': 'BSD',
    'py_modules': ['iplib'],
    'scripts': ['./bin/cidrinfo', './bin/ipconv', './bin/nmconv'],
    'keywords': ['ip', 'address', 'quad', 'dot', 'notation',
                 'binary', 'octal', 'hexadecimal', 'netmask', 'cidr', 'internet'],
    'platforms': 'any',
    'download_url': 'http://erlug.linux.it/~da/soft/iplib/',
    'classifiers': filter(None, classifiers.split("\n"))
}

setuptools.setup(**params)
