# The iplib module

The `iplib` module contains functions, classes, and constants useful for managing IPv4 addresses and netmasks.

You can use this Python module (and the included scripts `ipconv`, `nmconv`, and `cidrinfo`) to convert amongst many different notations and to manage address/netmask pairs in CIDR notation.

`iplib` supports Python 3.10 through Python 3.16+ and includes complete type annotations.


# Functions

## Format check

These functions always return `True` or `False` (never raise exceptions) and can be called with any kind of arguments (integers, strings, and objects with a `__str__()` method which returns a suitable string):

* `is_dot(ip)`: Return `True` if the IP address is in dotted decimal notation.
* `is_hex(ip)`: Return `True` if the IP address is in hexadecimal notation.
* `is_bin(ip)`: Return `True` if the IP address is in binary notation.
* `is_oct(ip)`: Return `True` if the IP address is in octal notation.
* `is_dec(ip)`: Return `True` if the IP address is in decimal notation.
* `is_dot_nm(nm)`: Return `True` if the netmask is in dotted decimal notation.
* `is_hex_nm(nm)`: Return `True` if the netmask is in hexadecimal notation.
* `is_bin_nm(nm)`: Return `True` if the netmask is in binary notation.
* `is_oct_nm(nm)`: Return `True` if the netmask is in octal notation.
* `is_dec_nm(nm)`: Return `True` if the netmask is in decimal notation.
* `is_bits_nm(nm)`: Return `True` if the netmask is in bits notation.
* `is_wildcard_nm(nm)`: Return `True` if the netmask is in wildcard bits notation.

## Format detection

Functions to detect IP/netmask notation; return `IP_UNKNOWN`/`NM_UNKNOWN` if the IP/netmask notation is not detected:

* `detect(ip)`: Try to detect the notation of an IP address.
* `detect_nm(nm)`: Try to detect the notation of a netmask.
* `p_detect(ip)` and `p_detect_nm(nm)`: detect the notation of an IP address (or netmask) and return a nice string ('unknown' if it's not detected).
* `is_notation(ip, notation)` and `is_notation_nm(nm, notation)`: return `True` if the given IP address (or netmask) is in the specified notation.

## Conversions

Functions to convert IP/netmask; can raise a `ValueError` exception:

* `convert(ip, notation=IP_DOT, inotation=IP_UNKNOWN)` and `convert_nm(nm, notation=IP_DOT, inotation=IP_UNKNOWN)`: Convert the given IP address (or netmask) to the given notation; the `notation` argument sets the notation of the output; the `inotation` argument forces the input to be considered as an address in the specified notation. When the IP address (or netmask) is an integer, the `inotation` argument is assumed to be `IP_DEC` (if not set otherwise).


# Classes

## IPv4Address

* `IPv4Address(ip, notation=IP_UNKNOWN)`: This class represents an IPv4 Internet address.

An `IPv4Address` object can be used to sum or subtract two IP addresses or an integer offset:

```python
>>> import iplib
>>> ip = iplib.IPv4Address('127.0.0.1')
>>> ip + 1000
<IPv4 address 127.0.3.233>
```

It's also possible to compare two IP addresses:

```python
>>> iplib.IPv4Address('127.0.0.1') < iplib.IPv4Address('127.0.0.4')
True
```

For both `IPv4Address` and `IPv4NetMask` objects you can specify the notation:

```python
>>> iplib.IPv4Address('24323', iplib.IP_OCT)
>>> iplib.IPv4Address('24323', 'oct')
>>> iplib.IPv4Address('24323', 'octal')
```


## IPv4NetMask

* `IPv4NetMask(nm, notation=IP_UNKNOWN)`: This class represents an IPv4 Internet netmask.


## CIDR

* `CIDR(ip, netmask=None)`: The representation of a Classless Inter-Domain Routing (CIDR) address.

From instances of this class, you can retrieve information about usable IP addresses, broadcast, and network address:

```python
>>> cidr = iplib.CIDR('127.0.0.1/8')
>>> cidr.is_valid_ip('127.4.5.6')
True
```


# Constants

The following constants are used to define IP/netmask notations:

* `IP_DOT` and `NM_DOT`: dotted decimal notation (e.g.: `192.168.0.42`).
* `IP_HEX` and `NM_HEX`: hexadecimal notation (`0xC0A8002A`). 
* `IP_BIN` and `NM_BIN`: binary notation (`11000000101010000000000000101010`).
* `IP_OCT` and `NM_OCT`: octal notation (`0o30052000052`).
* `IP_DEC` and `NM_DEC`: decimal notation (`3232235562`).
* `NM_BITS`: netmask in bits notation (`24`).
* `NM_WILDCARD`: netmask in wildcard bits notation (`0.0.0.255`).
* `IP_UNKNOWN` and `NM_UNKNOWN`: unknown notation.
* `NOTATION_MAP`: a dictionary mapping notations to valid string identifiers.
* `VALID_NETMASKS`: a dictionary mapping valid netmask bit lengths to decimal values.


# License

This code is released under the BSD license.

# Copyright

Copyright 2001-2026 Davide Alberani <da@mimante.net>
