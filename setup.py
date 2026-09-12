#!/usr/bin/env python3

import setuptools

long_desc = """You can use this Python module to convert amongst many
different notations and to manage couples of address/netmask
in the CIDR notation.
"""

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: No Input/Output (Daemon)",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Programming Language :: Python :: 3.15",
    "Programming Language :: Python :: 3.16",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Networking",
    "Topic :: Internet",
    "Topic :: Utilities",
]

params = {
    "name": "iplib",
    "version": "1.2.2",
    "description": "convert amongst many different IPv4 notations",
    "long_description": long_desc,
    "author": "Davide Alberani",
    "author_email": "da@mimante.net",
    "maintainer": "Davide Alberani",
    "maintainer_email": "da@mimante.net",
    "url": "https://github.com/alberanid/python-iplib",
    "license": "BSD",
    "py_modules": ["iplib"],
    "scripts": ["./bin/cidrinfo", "./bin/ipconv", "./bin/nmconv"],
    "keywords": [
        "ip",
        "address",
        "quad",
        "dot",
        "notation",
        "binary",
        "octal",
        "hexadecimal",
        "netmask",
        "cidr",
        "internet",
    ],
    "platforms": "any",
    "download_url": "https://github.com/alberanid/python-iplib",
    "python_requires": ">=3.10",
    "classifiers": classifiers,
}

setuptools.setup(**params)
