# The iplib module

The iplib module contains many functions, classes and constants useful to manage IP addresses and netmasks.

You can use this Python module (and the scripts 'ipconv', 'nmconv' and 'cidrinfo') to convert amongst many different notations and to manage couples of address/netmask in the CIDR notation.

iplib was written a long time ago and the code shows its age.
In June 2018, with the release of version 1.2, it was converted to support both Python 2 and Python 3 (without any other refactoring).


# Functions

## Format check

These functions always return True or False (never raise exceptions) and can be called with any kind of arguments (integers, strings and objects with a __str__() method which returns a suitable string):

* is_dot(ip): Return True if the IP address is in dotted decimal notation.
* is_hex(ip): Return True if the IP address is in hexadecimal notation.
* is_bin(ip): Return True if the IP address is in binary notation.
* is_oct(ip): Return True if the IP address is in octal notation.
* is_dec(ip): Return True if the IP address is in decimal notation.
* is_dot_nm(nm): Return True if the netmask is in dotted decimal notatation.
* is_hex_nm(nm): Return True if the netmask is in hexadecimal notatation.
* is_bin_nm(nm): Return True if the netmask is in binary notatation.
* is_oct_nm(nm): Return True if the netmask is in octal notatation.
* is_dec_nm(nm): Return True if the netmask is in decimal notatation.
* is_bits_nm(nm): Return True if the netmask is in bits notatation.
* is_wildcard_nm(nm): Return True if the netmask is in wildcard bits notatation.

## Format detection

Functions to detect IP/netmask notation; return IP_UNKNOWN/NM_UNKNOWN if the IP/netmask notation is not detected:

* detect(ip): Try to detect the notation of an IP address.
* detect_nm(nm): Try to detect the notation of a netmask.
* p_detect(ip) and p_detect_nm(nm): detect the notation of an IP address (or netmask) and return a nice string ('unknown' if it's not detected).
* is_notation(ip, notation) and is_notation_nm(nm, notation): return True if the given IP address  (or netmask) is in the specified notation.

## Conversions

Function to convert IP/netmask; can raise a ValueError exception:

* convert(ip, notation=IP_DOT, inotation=IP_UNKNOWN) and convert_nm(nm, notation=IP_DOT, inotation=IP_UNKNOWN): Convert the given IP address (or netmask) to the given notation; the 'notation' argument set the notation of the output; the 'inotation' argument force the input to be considered as an address in the specified notation. When the IP address (or netmask) is an integer, the inotation argument is assumed to be IP_DEC (if not set otherwise).


#  Classes

## IPv4Address

* IPv4Address(ip, notation=IP_UNKNOWN): This class represents an IPv4 Internet address.

An IPv4Address object can be used to sum or subtract two IP address; the second argument can also be an integer, so that, if you want to know what's the 1000th IP address after 127.0.0.1, you can:

  >>> import iplib
  >>> ip = iplib.IPv4Address('127.0.0.1')
  >>> ip + 1000
  <IPv4 address 127.0.3.233>

It's also possible to compare two IP addresses (the same is true for netmasks); e.g.:

  >>> iplib.IPv4Address('127.0.0.1') < iplib.IPv4Address('127.0.0.4')
  True

For both IPv4Address and IPv4NetMask object you can force the notation with the 'notation' option; e.g.:

  >>> iplib.IPv4Address('24323', iplib.IP_OCT)
  # that's equivalent to:
  >>> iplib.IPv4Address('24323', 'oct')
  # and:
  >>> iplib.IPv4Address('24323', 'octal')


## IPv4NetMask

* IPv4NetMask(nm, notation=IP_UNKNOWN): This class represents an IPv4 Internet netmask.


## CIDR

* CIDR(ip, netmask=None): The representation of a Classless Inter-Domain Routing (CIDR) address.

From objects instance of this class, you can retrieve informations about the number of usable IP addresses, the first and the last usable address, the broadcast and the netword address.
The netmask can be omitted, if the ip argument is a string 'ip/nm'; e.g.:

  >>> cidr = iplib.CIDR('127.0.0.1', '8')
  # is equivalent to:
  >>> cidr = iplib.CIDR('127.0.0.1/8')

Using the is_valid_ip(self, ip) method you can guess if the provided IP address is amongst the usable addresses; e.g.:

  >>> cidr = iplib.CIDR('127.0.0.1/8')
  >>> cidr.is_valid_ip('127.4.5.6')
  True

#  Constants

The following constants are used to define IP/netmask notations:

* IP_DOT and NM_DOT: an IP address (or netmask) in dotted decimal notation (e.g.: 192.168.0.42).
* IP_HEX and NM_HEX: hexadecimal notation (0xC0A8002A). 
* IP_BIN and NM_BIN: binary notation (11000000101010000000000000101010).
* IP_OCT and NM_OCT: octal notation (030052000052).
* IP_DEC and NM_DEC: decimal notation (3232235562).
* NM_BITS: netmask in bits notation (24).
* NM_WILDCARD: netmask in wildcard bits notation (0.0.0.255).
* IP_UNKNOWN and NM_UNKNOWN: an IP address (or netmask) in a unknown notation.
* NOTATION_MAP: a dictionary that maps notations with a list of strings that can be used instead of the IP_* and NM_* constants.
* VALID_NETMASKS: a dictionary that maps valid netmask in bits notation with their values in decimal notation.

E.g.: you can call the convert() function in these two equivalent ways:

* iplib.convert('192.168.0.42', notation=iplib.IP_HEX)
* iplib.convert('192.168.0.42', 'hex')

The following strings can be used instead of constants:

* 'binary', 'bin': IP_BIN/NM_BIN
* 'octal', 'oct': IP_OCT/NM_OCT
* 'decimal', 'dec': IP_DEC/NM_DEC
* 'bits', 'bit', 'cidr': NM_BITS
* 'wildcard bits', 'wildcard': NM_WILDCARD
* 'unknown', 'unk': IP_UNKNOWN/NM_UNKNOWN

# License

This code is release under the BSD license.

# Copyright

Copyright 2005-2018 Davide Alberani <da@erlug.linux.it>

