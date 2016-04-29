#!/usr/bin/env python
#
# NMConv
# Convert among netmask notations.
#
# Copyright 2001-2010 Davide Alberani <da@erlug.linux.it>
#
# This code is released under the BSD license.
#

import iplib, sys, getopt, os


CALL_NAME = os.path.basename(sys.argv[0])
APP_NAME='NMConv'
VERSION='0.6'
MYEMAIL='Davide Alberani <da@erlug.linux.it>'
HELP = """
%s Version: %s
Usage: %s [OPTIONS] netmask
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

nm = args[0]
if nm and nm[0] == '/':
    nm = nm[1:]

if not inp:
    inp = iplib.detect_nm(nm)
    if not outp and inp:
        print '  notation autodetected as: "%s"' % iplib.p_notation(inp)

if inp == iplib.IP_UNKNOWN:
    sys.stderr.write('unable to autodetect the notation of "%s"' % nm)
    print HELP
    sys.exit(4)

if outp:
    try:
        print iplib.convert_nm(nm, notation=outp, inotation=inp)
    except ValueError:
        sys.stderr.write(nm + ' netmask is not in ' + iplib.p_notation(inp) + \
                            ' notation or cannot be converted to ' + \
                            str(outp) + '.\n')
        print HELP
        sys.exit(4)

else:
    for notation in iplib.NOTATION_MAP.keys():
        if notation == iplib.NM_UNKNOWN:
            continue
        try:
            print iplib.NOTATION_MAP[notation][0] + ':  ' + \
                    iplib.convert_nm(nm, notation=notation, inotation=inp)
        except ValueError:
            sys.stderr.write('%s: invalid netmask.\n' % nm)
            print HELP
            sys.exit(4)

sys.exit(0)

