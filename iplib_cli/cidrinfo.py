#!/usr/bin/env python3
#
# CIDRInfo
# Shows information about a CIDR address.
#
# Copyright 2001-2026 Davide Alberani <da@mimante.net>
#
# This code is released under the BSD license.
#

from __future__ import annotations

import argparse
import sys
import iplib

APP_NAME = "CIDRInfo"
VERSION = "0.3"
MYEMAIL = "Davide Alberani <da@mimante.net>"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} v{VERSION} - Shows information about a CIDR address.",
        epilog=f"Send bug reports to {MYEMAIL}",
    )
    parser.add_argument("address", help="IP address / netmask in CIDR notation (e.g. 192.168.1.1/24)")
    args = parser.parse_args()

    try:
        cidr = iplib.CIDR(args.address)
    except ValueError:
        sys.stderr.write(f"{args.address}: invalid CIDR address.\n")
        sys.exit(3)

    print(f"CIDR:{cidr}")
    print(f"first usable IP address:{cidr.get_first_ip()}")
    print(f"last usable IP address:{cidr.get_last_ip()}")
    print(f"number of usable IP addresses:{cidr.get_ip_number()}")
    print(f"network address:{cidr.get_network_ip()}")
    print(f"broadcast address:{cidr.get_broadcast_ip()}")


if __name__ == "__main__":
    main()
