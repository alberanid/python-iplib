#!/usr/bin/env python
#
# IPConv
# Convert among ip address notations.
#
# Copyright 2001-2010 Davide Alberani <da@erlug.linux.it>
#
# This code is released under the BSD license.
#

import iplib, sys, getopt, os


CALL_NAME = os.path.basename(sys.argv[0])
APP_NAME='IPConv'
VERSION='0.6'
MYEMAIL='Davide Alberani <da@erlug.linux.it>'
HELP = """
%s Version: %s
Usage: %s [OPTIONS] ip_address
Options:
    -o  output only in the specified notation (e.g.: dot|hex|bin|dec|oct).
    -i  the input is in the given notation (otherwise it's autodetected).

Send bug reports to %s
""" % (APP_NAME, VERSION, CALL_NAME, MYEMAIL)


try:
    optlist, args = getopt.getopt(sys.argv[1:],
                        'ho:i:', ['help', 'output=', 'input='])
except getopt.error:
    print HELP
    sys.exit(1)

if len(args) != 1:
    sys.stderr.write('Only one argument is required.\n')
    print HELP
    sys.exit(2)

outp = ''
inp = ''

for opt in optlist:
    if opt[0] == '-h' or opt[0] == '--help':
        print HELP
        sys.exit(0)
    elif opt[0] == '-o' or opt[0] == '--output':
        outp = opt[1]
    elif opt[0] == '-i' or opt[0] == '--input':
        inp = opt[1]

ip = args[0]

if not inp:
    inp = iplib.detect(ip)
    if not outp and inp:
        print '  notation autodetected as: "%s"' % iplib.p_notation(inp)

if inp == iplib.IP_UNKNOWN:
    sys.stderr.write('unable to autodetect the notation of "%s"' % ip)
    print HELP
    sys.exit(4)

try:
    myip = iplib.IPv4Address(ip, notation=inp)
except ValueError:
    sys.stderr.write('%s address is not in notation %s.\n' %
                        (ip, iplib.p_notation(inp)))
    print HELP
    sys.exit(4)

if outp == 'dot':
    print myip.get_dot()
elif outp == 'hex':
    print myip.get_hex()
elif outp == 'bin':
    print myip.get_bin()
elif outp == 'dec':
    print myip.get_dec()
elif outp == 'oct':
    print myip.get_oct()
elif not outp:
    print 'Dotted decimal :', myip.get_dot()
    print 'Hexdecimal     :', myip.get_hex()
    print 'Octal          :', myip.get_oct()
    print 'Binary         :', myip.get_bin()
    print 'Decimal        :', myip.get_dec()
else:
    sys.stderr.write('%s: invalid notation.\n' % outp)
    print HELP
    sys.exit(5)

sys.exit(0)

