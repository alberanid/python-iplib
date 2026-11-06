#!/usr/bin/env python3
#
# NMConv
# Convert among netmask notations.
#
# Copyright 2001-2026 Davide Alberani <da@mimante.net>
#
# This code is released under the BSD license.
#

from __future__ import annotations

import argparse
import sys
import iplib

APP_NAME = "NMConv"
VERSION = "0.7"
MYEMAIL = "Davide Alberani <da@mimante.net>"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} v{VERSION} - Convert among netmask notations.",
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
        help="output only in specified notation (dot|hex|bin|dec|oct|bits|wildcard)",
    )
    parser.add_argument("netmask", help="netmask to convert")
    args = parser.parse_args()

    inp = args.inotation
    outp = args.notation
    nm = args.netmask

    if nm.startswith("/"):
        nm = nm[1:]

    if not inp:
        inp_notation = iplib.detect_nm(nm)
        if not outp and inp_notation != iplib.NM_UNKNOWN:
            print(f'  notation autodetected as: "{iplib.p_notation(inp_notation)}"')
        inp = inp_notation

    if inp == iplib.NM_UNKNOWN:
        sys.stderr.write(f'unable to autodetect the notation of "{nm}"\n')
        sys.exit(4)

    if outp:
        try:
            print(iplib.convert_nm(nm, notation=outp, inotation=inp))
        except ValueError:
            sys.stderr.write(
                f"{nm} netmask is not in {iplib.p_notation(inp)} notation or cannot be converted to {outp}.\n"
            )
            sys.exit(4)
    else:
        for notation in iplib.NOTATION_MAP:
            if notation == iplib.NM_UNKNOWN:
                continue
            try:
                converted = iplib.convert_nm(nm, notation=notation, inotation=inp)
                print(f"{iplib.NOTATION_MAP[notation][0]}:  {converted}")
            except ValueError:
                sys.stderr.write(f"{nm}: invalid netmask.\n")
                sys.exit(4)


if __name__ == "__main__":
    main()
