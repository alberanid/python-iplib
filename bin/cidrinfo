#!/usr/bin/env python
#
# CIDRInfo
# Shows informations about a CIDR address.
#
# Copyright 2001-2010 Davide Alberani <da@erlug.linux.it>
#
# This code is released under the BSD license.
#

import iplib, sys, os

CALL_NAME = os.path.basename(sys.argv[0])
APP_NAME='CIDRInfo'
VERSION='0.2'
MYEMAIL='Davide Alberani <da@erlug.linux.it>'
HELP = """
%s Version: %s
Usage: %s ip_address/netmask

Send bug reports to %s
""" % (APP_NAME, VERSION, CALL_NAME, MYEMAIL)


if len(sys.argv[1:]) != 1:
    sys.stderr.write('Only one argument is required.\n')
    print HELP
    sys.exit(2)

address = sys.argv[1]

try:
    cidr = iplib.CIDR(address)
except ValueError:
    sys.stderr.write('%s: invalid CIDR address.\n' % address)
    print HELP
    sys.exit(3)

print 'CIDR:', str(cidr)
print 'first usable IP address:', str(cidr.get_first_ip())
print 'last usable IP address:', str(cidr.get_last_ip())
print 'number of usable IP addresses:', str(cidr.get_ip_number())
print 'network address:', str(cidr.get_network_ip())
print 'broadcast address:', str(cidr.get_broadcast_ip())


