#!/usr/bin/env python3
#
# IPConv
# Convert among IP address notations.
#
# Copyright 2001-2026 Davide Alberani <da@mimante.net>
#
# This code is released under the BSD license.
#

from __future__ import annotations

import argparse
import sys
import iplib

APP_NAME = "IPConv"
VERSION = "0.7"
MYEMAIL = "Davide Alberani <da@mimante.net>"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} v{VERSION} - Convert among IP address notations.",
        epilog=f"Send bug reports to {MYEMAIL}",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="inotation",
        default="",
        help="input notation (otherwise autodetected)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="notation",
        default="",
        help="output only in the specified notation (dot|hex|bin|dec|oct)",
    )
    parser.add_argument("ip", help="IP address to convert")
    args = parser.parse_args()

    inp = args.inotation
    outp = args.notation
    ip = args.ip

    if not inp:
        inp_notation = iplib.detect(ip)
        if not outp and inp_notation != iplib.IP_UNKNOWN:
            print(f'  notation autodetected as: "{iplib.p_notation(inp_notation)}"')
        inp = inp_notation

    if inp == iplib.IP_UNKNOWN:
        sys.stderr.write(f'unable to autodetect the notation of "{ip}"\n')
        sys.exit(4)

    try:
        myip = iplib.IPv4Address(ip, notation=inp)
    except ValueError:
        sys.stderr.write(f"{ip} address is not in notation {iplib.p_notation(inp)}.\n")
        sys.exit(4)

    if outp == "dot":
        print(myip.get_dot())
    elif outp == "hex":
        print(myip.get_hex())
    elif outp == "bin":
        print(myip.get_bin())
    elif outp == "dec":
        print(myip.get_dec())
    elif outp == "oct":
        print(myip.get_oct())
    elif not outp:
        print(f"Dotted decimal :{myip.get_dot()}")
        print(f"Hexdecimal     :{myip.get_hex()}")
        print(f"Octal          :{myip.get_oct()}")
        print(f"Binary         :{myip.get_bin()}")
        print(f"Decimal        :{myip.get_dec()}")
    else:
        sys.stderr.write(f"{outp}: invalid notation.\n")
        sys.exit(5)


if __name__ == "__main__":
    main()
