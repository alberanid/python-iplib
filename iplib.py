"""iplib module.

The representation of IPv4 addresses and netmasks.
You can use this module to convert amongst many different notations
and to manage couples of address/netmask in the CIDR notation.

  Copyright 2001-2026 Davide Alberani <da@mimante.net>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

__version__ = "1.3.0"


# Notation types (with an example in the comment).
# You can use these constants when you have to specify a notation style.
IP_UNKNOWN = NM_UNKNOWN = 0
IP_DOT = NM_DOT = 1  # 192.168.0.42
IP_HEX = NM_HEX = 2  # 0xC0A8002A
IP_BIN = NM_BIN = 3  # 0o30052000052
IP_OCT = NM_OCT = 4  # 11000000101010000000000000101010
IP_DEC = NM_DEC = 5  # 3232235562
NM_BITS = 6  # 26
NM_WILDCARD = 7  # 0.0.0.63

# Map notations with one or more strings.
# You can use these constant strings when you have to specify a notation
# style, instead of using numeric values.
NOTATION_MAP: dict[int, tuple[str, ...]] = {
    IP_DOT: ("dotted decimal", "dotted", "quad", "dot", "dotted quad"),
    IP_HEX: ("hexadecimal", "hex"),
    IP_BIN: ("binary", "bin"),
    IP_OCT: ("octal", "oct"),
    IP_DEC: ("decimal", "dec"),
    NM_BITS: ("bits", "bit", "cidr"),
    NM_WILDCARD: ("wildcard bits", "wildcard"),
    IP_UNKNOWN: ("unknown", "unk"),
}

_NOTATION_KEYS: dict[int | str, int] = {key: key for key in NOTATION_MAP}
for key, values in NOTATION_MAP.items():
    for value in values:
        _NOTATION_KEYS[value] = key


def _get_notation(notation: Any) -> int | None:
    """Given a numeric value or string value, returns one in IP_DOT, IP_HEX,
    IP_BIN, etc., or None if unable to convert to the internally
    used numeric convention."""
    return _NOTATION_KEYS.get(notation, None)


def p_notation(notation: Any) -> str:
    """Return a string representing the given notation."""
    not_val = _get_notation(notation)
    key = not_val if not_val is not None else IP_UNKNOWN
    return NOTATION_MAP[key][0]


# This dictionary maps NM_BITS to NM_DEC values.
# NOTE: /31 is a valid netmask; see RFC3021 (courtesy of Lars Erik Gullerud).
VALID_NETMASKS: dict[int, int] = {
    0: 0,
    1: 2147483648,
    2: 3221225472,
    3: 3758096384,
    4: 4026531840,
    5: 4160749568,
    6: 4227858432,
    7: 4261412864,
    8: 4278190080,
    9: 4286578688,
    10: 4290772992,
    11: 4292870144,
    12: 4293918720,
    13: 4294443008,
    14: 4294705152,
    15: 4294836224,
    16: 4294901760,
    17: 4294934528,
    18: 4294950912,
    19: 4294959104,
    20: 4294963200,
    21: 4294965248,
    22: 4294966272,
    23: 4294966784,
    24: 4294967040,
    25: 4294967168,
    26: 4294967232,
    27: 4294967264,
    28: 4294967280,
    29: 4294967288,
    30: 4294967292,
    31: 4294967294,
    32: 4294967295,
}
_NETMASKS_VALUES = list(VALID_NETMASKS.values())
_NETMASKS_INV = {value: key for key, value in VALID_NETMASKS.items()}


# - Functions used to check if an address or a netmask is in a given notation.


def is_dot(ip: Any) -> bool:
    """Return true if the IP address is in dotted decimal notation."""
    octets = str(ip).split(".")
    if len(octets) != 4:
        return False
    for octet in octets:
        try:
            val = int(octet)
        except ValueError:
            return False
        if not (0 <= val <= 255):
            return False
    return True


def is_hex(ip: Any) -> bool:
    """Return true if the IP address is in hexadecimal notation."""
    try:
        dec = int(str(ip), 16)
    except (TypeError, ValueError):
        return False
    return 0 <= dec <= 0xFFFFFFFF


def is_bin(ip: Any) -> bool:
    """Return true if the IP address is in binary notation."""
    try:
        s = str(ip)
        if len(s) != 32:
            return False
        dec = int(s, 2)
    except (TypeError, ValueError):
        return False
    return 0 <= dec <= 4294967295


def is_oct(ip: Any) -> bool:
    """Return true if the IP address is in octal notation."""
    try:
        dec = int(str(ip), 8)
    except (TypeError, ValueError):
        return False
    return 0 <= dec <= 0o37777777777


def is_dec(ip: Any) -> bool:
    """Return true if the IP address is in decimal notation."""
    try:
        dec = int(str(ip))
    except (TypeError, ValueError):
        return False
    return 0 <= dec <= 4294967295


def _check_nm(nm: Any, notation: int) -> bool:
    """Function internally used to check if the given netmask
    is of the specified notation."""
    _NM_CHECK_FUNCT = {
        NM_DOT: _dot_to_dec,
        NM_HEX: _hex_to_dec,
        NM_BIN: _bin_to_dec,
        NM_OCT: _oct_to_dec,
        NM_DEC: _dec_to_dec_long,
    }
    try:
        dec = _NM_CHECK_FUNCT[notation](nm, check=True)
    except (ValueError, KeyError):
        return False
    return dec in _NETMASKS_VALUES


def is_dot_nm(nm: Any) -> bool:
    """Return true if the netmask is in dotted decimal notation."""
    return _check_nm(nm, NM_DOT)


def is_hex_nm(nm: Any) -> bool:
    """Return true if the netmask is in hexadecimal notation."""
    return _check_nm(nm, NM_HEX)


def is_bin_nm(nm: Any) -> bool:
    """Return true if the netmask is in binary notation."""
    return _check_nm(nm, NM_BIN)


def is_oct_nm(nm: Any) -> bool:
    """Return true if the netmask is in octal notation."""
    return _check_nm(nm, NM_OCT)


def is_dec_nm(nm: Any) -> bool:
    """Return true if the netmask is in decimal notation."""
    return _check_nm(nm, NM_DEC)


def is_bits_nm(nm: Any) -> bool:
    """Return true if the netmask is in bits notation."""
    try:
        bits = int(str(nm))
    except (TypeError, ValueError):
        return False
    return 0 <= bits <= 32


def is_wildcard_nm(nm: Any) -> bool:
    """Return true if the netmask is in wildcard bits notation."""
    try:
        dec = 0xFFFFFFFF - _dot_to_dec(nm, check=True)
    except ValueError:
        return False
    return dec in _NETMASKS_VALUES


# - Functions used to convert various notations to/from decimal notation.


def _dot_to_dec(ip: Any, check: bool = True) -> int:
    """Dotted decimal notation to decimal conversion."""
    if check and not is_dot(ip):
        raise ValueError(f'_dot_to_dec: invalid IP: "{ip}"')
    octets = str(ip).split(".")
    return (int(octets[0]) << 24) | (int(octets[1]) << 16) | (int(octets[2]) << 8) | int(octets[3])


def _dec_to_dot(ip: int) -> str:
    """Decimal to dotted decimal notation conversion."""
    return f"{(ip >> 24) & 255}.{(ip >> 16) & 255}.{(ip >> 8) & 255}.{ip & 255}"


def _hex_to_dec(ip: Any, check: bool = True) -> int:
    """Hexadecimal to decimal conversion."""
    if check and not is_hex(ip):
        raise ValueError(f'_hex_to_dec: invalid IP: "{ip}"')
    if isinstance(ip, int):
        ip = hex(ip)
    return int(str(ip), 16)


def _dec_to_hex(ip: int) -> str:
    """Decimal to hexadecimal conversion."""
    return hex(ip)


def _oct_to_dec(ip: Any, check: bool = True) -> int:
    """Octal to decimal conversion."""
    if check and not is_oct(ip):
        raise ValueError(f'_oct_to_dec: invalid IP: "{ip}"')
    if isinstance(ip, int):
        ip = oct(ip)
    return int(str(ip), 8)


def _dec_to_oct(ip: int) -> str:
    """Decimal to octal conversion."""
    return oct(ip)


def _bin_to_dec(ip: Any, check: bool = True) -> int:
    """Binary to decimal conversion."""
    if check and not is_bin(ip):
        raise ValueError(f'_bin_to_dec: invalid IP: "{ip}"')
    return int(str(ip), 2)


def _dec_to_bin(ip: int) -> str:
    """Decimal to binary conversion."""
    return f"{ip:032b}"


def _dec_to_dec_long(ip: Any, check: bool = True) -> int:
    """Decimal to decimal (long) conversion."""
    if check and not is_dec(ip):
        raise ValueError(f'_dec_to_dec: invalid IP: "{ip}"')
    return int(str(ip))


def _dec_to_dec_str(ip: int) -> str:
    """Decimal to decimal (string) conversion."""
    return str(ip)


def _bits_to_dec(nm: Any, check: bool = True) -> int:
    """Bits to decimal conversion."""
    if check and not is_bits_nm(nm):
        raise ValueError(f'_bits_to_dec: invalid netmask: "{nm}"')
    bits = int(str(nm))
    return VALID_NETMASKS[bits]


def _dec_to_bits(nm: int) -> str:
    """Decimal to bits conversion."""
    return str(_NETMASKS_INV[nm])


def _wildcard_to_dec(nm: Any, check: bool = False) -> int:
    """Wildcard bits to decimal conversion."""
    if check and not is_wildcard_nm(nm):
        raise ValueError(f'_wildcard_to_dec: invalid netmask: "{nm}"')
    return 0xFFFFFFFF - _dot_to_dec(nm, check=False)


def _dec_to_wildcard(nm: int) -> str:
    """Decimal to wildcard bits conversion."""
    return _dec_to_dot(0xFFFFFFFF - nm)


# - Functions used to detect the notation of an IP address or netmask.

_CHECK_FUNCT = {
    IP_DOT: (is_dot, is_dot_nm),
    IP_HEX: (is_hex, is_hex_nm),
    IP_BIN: (is_bin, is_bin_nm),
    IP_OCT: (is_oct, is_oct_nm),
    IP_DEC: (is_dec, is_dec_nm),
    NM_BITS: (lambda ip: False, is_bits_nm),
    NM_WILDCARD: (lambda ip: False, is_wildcard_nm),
}


def _is_notation(ip: Any, notation: Any, _isnm: bool) -> bool:
    """Internally used to check if an IP/netmask is in the given notation."""
    notation_orig = notation
    notation_key = _get_notation(notation)
    if notation_key not in _CHECK_FUNCT:
        raise ValueError(f'_is_notation: unknown notation: "{notation_orig}"')
    return _CHECK_FUNCT[notation_key][_isnm](ip)


def is_notation(ip: Any, notation: Any) -> bool:
    """Return true if the given address is in the given notation."""
    return _is_notation(ip, notation, _isnm=False)


def is_notation_nm(nm: Any, notation: Any) -> bool:
    """Return true if the given netmask is in the given notation."""
    return _is_notation(nm, notation, _isnm=True)


def _detect(ip: Any, _isnm: bool) -> int:
    """Function internally used to detect the notation of the
    given IP or netmask."""
    ip_str = str(ip)
    if len(ip_str) > 1:
        if ip_str.startswith("0x"):
            if _CHECK_FUNCT[IP_HEX][_isnm](ip_str):
                return IP_HEX
        elif ip_str.startswith("0"):
            if _CHECK_FUNCT[IP_OCT][_isnm](ip_str):
                return IP_OCT
    if _CHECK_FUNCT[IP_DOT][_isnm](ip_str):
        return IP_DOT
    if _isnm and _CHECK_FUNCT[NM_BITS][_isnm](ip_str):
        return NM_BITS
    if _CHECK_FUNCT[IP_DEC][_isnm](ip_str):
        return IP_DEC
    if _isnm and _CHECK_FUNCT[NM_WILDCARD][_isnm](ip_str):
        return NM_WILDCARD
    if _CHECK_FUNCT[IP_BIN][_isnm](ip_str):
        return IP_BIN
    return IP_UNKNOWN


def detect(ip: Any) -> int:
    """Detect the notation of an IP address."""
    return _detect(ip, _isnm=False)


def detect_nm(nm: Any) -> int:
    """Detect the notation of a netmask."""
    return _detect(nm, _isnm=True)


def p_detect(ip: Any) -> str:
    """Return the notation of an IP address (string)."""
    return NOTATION_MAP[detect(ip)][0]


def p_detect_nm(nm: Any) -> str:
    """Return the notation of a netmask (string)."""
    return NOTATION_MAP[detect_nm(nm)][0]


def _convert(
    ip: Any, notation: Any, inotation: Any, _check: bool | None, _isnm: bool
) -> str | int:
    """Internally used to convert IPs and netmasks to other notations."""
    inotation_orig = inotation
    notation_orig = notation
    inotation_key = _get_notation(inotation)
    notation_key = _get_notation(notation)

    if inotation_key is None:
        raise ValueError(f'_convert: unknown input notation: "{inotation_orig}"')
    if notation_key is None:
        raise ValueError(f'_convert: unknown output notation: "{notation_orig}"')

    docheck = _check if _check is not None else False
    if inotation_key == IP_UNKNOWN:
        inotation_key = _detect(ip, _isnm)
        if inotation_key == IP_UNKNOWN:
            raise ValueError("_convert: unable to guess input notation or invalid value")
        if _check is None:
            docheck = True

    if _isnm:
        docheck = False

    if inotation_key == IP_DOT:
        dec = _dot_to_dec(ip, docheck)
    elif inotation_key == IP_HEX:
        dec = _hex_to_dec(ip, docheck)
    elif inotation_key == IP_BIN:
        dec = _bin_to_dec(ip, docheck)
    elif inotation_key == IP_OCT:
        dec = _oct_to_dec(ip, docheck)
    elif inotation_key == IP_DEC:
        dec = _dec_to_dec_long(ip, docheck)
    elif _isnm and inotation_key == NM_BITS:
        dec = _bits_to_dec(ip, docheck)
    elif _isnm and inotation_key == NM_WILDCARD:
        dec = _wildcard_to_dec(ip, docheck)
    else:
        raise ValueError(f'_convert: unknown IP/netmask notation: "{inotation_orig}"')

    if _isnm and dec not in _NETMASKS_VALUES:
        raise ValueError(f'_convert: invalid netmask: "{ip}"')

    if notation_key == IP_DOT:
        return _dec_to_dot(dec)
    if notation_key == IP_HEX:
        return _dec_to_hex(dec)
    if notation_key == IP_BIN:
        return _dec_to_bin(dec)
    if notation_key == IP_OCT:
        return _dec_to_oct(dec)
    if notation_key == IP_DEC:
        return _dec_to_dec_str(dec)
    if _isnm and notation_key == NM_BITS:
        return _dec_to_bits(dec)
    if _isnm and notation_key == NM_WILDCARD:
        return _dec_to_wildcard(dec)
    raise ValueError(f'convert: unknown notation: "{notation_orig}"')


def convert(
    ip: Any, notation: Any = IP_DOT, inotation: Any = IP_UNKNOWN, check: bool | None = True
) -> str | int:
    """Convert among IP address notations."""
    return _convert(ip, notation, inotation, _check=check, _isnm=False)


def convert_nm(
    nm: Any, notation: Any = IP_DOT, inotation: Any = IP_UNKNOWN, check: bool | None = True
) -> str | int:
    """Convert a netmask to another notation."""
    return _convert(nm, notation, inotation, _check=check, _isnm=True)


# - Classes used to manage IP addresses, netmasks and the CIDR notation.


class _IPv4Base:
    """Base class for IP addresses and netmasks."""

    _isnm = False  # Set to True when representing a netmask.

    def __init__(self, ip: Any, notation: Any = IP_UNKNOWN) -> None:
        """Initialize the object."""
        self.set(ip, notation)

    def set(self, ip: Any, notation: Any = IP_UNKNOWN) -> None:
        """Set the IP address/netmask."""
        self._ip_dec = int(
            _convert(ip, notation=IP_DEC, inotation=notation, _check=True, _isnm=self._isnm)
        )
        self._ip = str(
            _convert(self._ip_dec, notation=IP_DOT, inotation=IP_DEC, _check=False, _isnm=self._isnm)
        )

    def get(self) -> str:
        """Return the address/netmask."""
        return self.get_dot()

    def get_dot(self) -> str:
        """Return the dotted decimal notation of the address/netmask."""
        return self._ip

    def get_hex(self) -> str:
        """Return the hexadecimal notation of the address/netmask."""
        return str(
            _convert(self._ip_dec, notation=IP_HEX, inotation=IP_DEC, _check=False, _isnm=self._isnm)
        )

    def get_bin(self) -> str:
        """Return the binary notation of the address/netmask."""
        return str(
            _convert(self._ip_dec, notation=IP_BIN, inotation=IP_DEC, _check=False, _isnm=self._isnm)
        )

    def get_dec(self) -> str:
        """Return the decimal notation of the address/netmask."""
        return str(self._ip_dec)

    def get_oct(self) -> str:
        """Return the octal notation of the address/netmask."""
        return str(
            _convert(self._ip_dec, notation=IP_OCT, inotation=IP_DEC, _check=False, _isnm=self._isnm)
        )

    def __str__(self) -> str:
        """Print this address/netmask."""
        return self.get()

    def _cmp_prepare(self, other: Any) -> int:
        """Prepare the item to be compared with this address/netmask."""
        if isinstance(other, self.__class__):
            return other._ip_dec
        if isinstance(other, int):
            return other
        return self.__class__(other)._ip_dec

    def __lt__(self, other: Any) -> bool:
        ret = self._ip_dec < self._cmp_prepare(other)
        return not ret if self._isnm else ret

    def __le__(self, other: Any) -> bool:
        ret = self._ip_dec <= self._cmp_prepare(other)
        return not ret if self._isnm else ret

    def __gt__(self, other: Any) -> bool:
        ret = self._ip_dec > self._cmp_prepare(other)
        return not ret if self._isnm else ret

    def __ge__(self, other: Any) -> bool:
        ret = self._ip_dec >= self._cmp_prepare(other)
        return not ret if self._isnm else ret

    def __eq__(self, other: Any) -> bool:
        return self._ip_dec == self._cmp_prepare(other)

    def __ne__(self, other: Any) -> bool:
        return self._ip_dec != self._cmp_prepare(other)

    def __hash__(self) -> int:
        """Hash consistent with __eq__ (which compares only the decimal value,
        ignoring subclass), so instances work as dict keys/set members."""
        return hash(self._ip_dec)

    def __int__(self) -> int:
        """Return the decimal representation of the address/netmask."""
        return self._ip_dec

    def __index__(self) -> int:
        return self._ip_dec


class IPv4Address(_IPv4Base):
    """An IPv4 Internet address."""

    ip = address = property(_IPv4Base.get, _IPv4Base.set, doc="The represented IP.")

    def __repr__(self) -> str:
        """The representation string for this address."""
        return f"<IPv4 address {self.get()}>"

    def _add(self, other: Any) -> int:
        """Sum two IP addresses."""
        if isinstance(other, self.__class__):
            return self._ip_dec + other._ip_dec
        if isinstance(other, int):
            return self._ip_dec + other
        return self._ip_dec + self.__class__(other)._ip_dec

    def __add__(self, other: Any) -> IPv4Address:
        """Sum two IP addresses."""
        return IPv4Address(self._add(other), notation=IP_DEC)

    __radd__ = __add__

    def __iadd__(self, other: Any) -> IPv4Address:
        """Augmented arithmetic sum."""
        self.set(self._add(other), notation=IP_DEC)
        return self

    def _sub(self, other: Any) -> int:
        """Subtract two IP addresses."""
        if isinstance(other, self.__class__):
            return self._ip_dec - other._ip_dec
        if isinstance(other, int):
            return self._ip_dec - other
        return self._ip_dec - self.__class__(other)._ip_dec

    def __sub__(self, other: Any) -> IPv4Address:
        """Subtract two IP addresses."""
        return IPv4Address(self._sub(other), notation=IP_DEC)

    __rsub__ = __sub__

    def __isub__(self, other: Any) -> IPv4Address:
        """Augmented arithmetic subtraction."""
        self.set(self._sub(other), notation=IP_DEC)
        return self


class IPv4NetMask(_IPv4Base):
    """An IPv4 Internet netmask."""

    _isnm = True
    nm = netmask = property(_IPv4Base.get, _IPv4Base.set, doc="The represented netmask.")

    def get_bits(self) -> str:
        """Return the bits notation of the netmask."""
        return str(
            _convert(self._ip, notation=NM_BITS, inotation=IP_DOT, _check=False, _isnm=self._isnm)
        )

    def get_wildcard(self) -> str:
        """Return the wildcard bits notation of the netmask."""
        return str(
            _convert(self._ip, notation=NM_WILDCARD, inotation=IP_DOT, _check=False, _isnm=self._isnm)
        )

    def __repr__(self) -> str:
        """The representation string for this netmask."""
        return f"<IPv4 netmask {self.get()}>"


class CIDR:
    """A CIDR address.

    The representation of a Classless Inter-Domain Routing (CIDR) address."""

    MAX_LIST_ADDRESSES = 65536

    def __init__(self, ip: Any, netmask: Any = None) -> None:
        self.set(ip, netmask)

    def _ensure_iterable_size(self) -> None:
        """Reject materializing very large address ranges as a list to avoid memory exhaustion."""
        ip_count = self.get_ip_number()
        if ip_count > self.MAX_LIST_ADDRESSES:
            raise ValueError(
                f"CIDR {self} contains {ip_count} usable addresses; "
                f"get_all_valid_ip() is limited to {self.MAX_LIST_ADDRESSES}. "
                "Use iter(cidr) to iterate lazily instead."
            )

    def set(self, ip: Any, netmask: Any = None) -> None:
        """Set the IP address and the netmask."""
        if isinstance(ip, str) and netmask is None:
            ipnm = ip.split("/")
            if len(ipnm) != 2:
                raise ValueError(f'set: invalid CIDR: "{ip}"')
            ip, netmask = ipnm[0], ipnm[1]
        self._ip = ip if isinstance(ip, IPv4Address) else IPv4Address(ip)
        self._nm = netmask if isinstance(netmask, IPv4NetMask) else IPv4NetMask(netmask)

        ipl = int(self._ip)
        nml = int(self._nm)
        base_add = ipl & nml
        self._ip_num = 0xFFFFFFFF - 1 - nml

        if self._ip_num in (-1, 0):
            self._ip_num = 1 if self._ip_num == -1 else 2
            self._net_ip = None
            self._bc_ip = None
            self._first_ip_dec = base_add
            self._first_ip = IPv4Address(self._first_ip_dec, notation=IP_DEC)
            last_ip_dec = self._first_ip_dec if self._ip_num == 1 else self._first_ip_dec + 1
            self._last_ip = IPv4Address(last_ip_dec, notation=IP_DEC)
            return

        self._net_ip = IPv4Address(base_add, notation=IP_DEC)
        self._bc_ip = IPv4Address(base_add + self._ip_num + 1, notation=IP_DEC)
        self._first_ip_dec = base_add + 1
        self._first_ip = IPv4Address(self._first_ip_dec, notation=IP_DEC)
        self._last_ip = IPv4Address(base_add + self._ip_num, notation=IP_DEC)

    def get(self) -> str:
        """Print this CIDR address."""
        return f"{self._ip}/{self._nm}"

    def set_ip(self, ip: Any) -> None:
        """Change the current IP."""
        self.set(ip=ip, netmask=self._nm)

    def get_ip(self) -> IPv4Address:
        """Return the given address."""
        return self._ip

    def set_netmask(self, netmask: Any) -> None:
        """Change the current netmask."""
        self.set(ip=self._ip, netmask=netmask)

    def get_netmask(self) -> IPv4NetMask:
        """Return the netmask."""
        return self._nm

    def get_first_ip(self) -> IPv4Address:
        """Return the first usable IP address."""
        return self._first_ip

    def get_last_ip(self) -> IPv4Address:
        """Return the last usable IP address."""
        return self._last_ip

    def get_network_ip(self) -> IPv4Address | None:
        """Return the network address."""
        return self._net_ip

    def get_broadcast_ip(self) -> IPv4Address | None:
        """Return the broadcast address."""
        return self._bc_ip

    def get_ip_number(self) -> int:
        """Return the number of usable IP addresses."""
        return self._ip_num

    def get_all_valid_ip(self) -> list[IPv4Address]:
        """Return a list of IPv4Address objects, one for every usable IP.

        Raises ValueError if the range is too large to materialize as a
        list in memory; use `iter(cidr)` to lazily iterate instead."""
        self._ensure_iterable_size()
        return list(self)

    def is_valid_ip(self, ip: Any) -> bool:
        """Return true if the given address is amongst usable addresses,
        or if the given CIDR is contained in this one."""
        if not isinstance(ip, (IPv4Address, CIDR)):
            if "/" not in str(ip):
                ip = IPv4Address(ip)
            else:
                ip = CIDR(ip)
        if isinstance(ip, IPv4Address):
            if ip < self._first_ip or ip > self._last_ip:
                return False
        elif isinstance(ip, CIDR):
            if ip._nm._ip_dec == 0xFFFFFFFE and self._nm._ip_dec != 0xFFFFFFFE:
                compare_to_first = (
                    self._net_ip._ip_dec if self._net_ip is not None else self._first_ip._ip_dec
                )
                compare_to_last = (
                    self._bc_ip._ip_dec if self._bc_ip is not None else self._last_ip._ip_dec
                )
            else:
                compare_to_first = self._first_ip._ip_dec
                compare_to_last = self._last_ip._ip_dec
            if ip._first_ip._ip_dec < compare_to_first or ip._last_ip._ip_dec > compare_to_last:
                return False
        return True

    def __str__(self) -> str:
        """Print this CIDR address."""
        return self.get()

    def __repr__(self) -> str:
        """The representation string for this netmask."""
        return f"<{self.get_ip()}/{self.get_netmask()} CIDR>"

    def __len__(self) -> int:
        """Return the number of usable IP address."""
        return self.get_ip_number()

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm < other._nm

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm <= other._nm

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm > other._nm

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm >= other._nm

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm == other._nm

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return self._nm != other._nm

    def __hash__(self) -> int:
        """Hash consistent with __eq__, which compares only the netmask."""
        return hash(self._nm)

    def __contains__(self, item: Any) -> bool:
        """Return true if the given address in amongst the usable addresses,
        or if the given CIDR is contained in this one."""
        return self.is_valid_ip(item)

    def __iter__(self) -> Iterator[IPv4Address]:
        """Iterate over IPv4Address objects, one for every usable IP.

        This is a lazy generator, so iterating even very large ranges
        (e.g. 0.0.0.0/0) does not exhaust memory."""
        for i in range(self._ip_num):
            yield IPv4Address(self._first_ip_dec + i, notation=IP_DEC)

    cidr = property(get, set, doc="The represented CIDR.")
    ip = address = property(get_ip, set_ip, doc="The IP of this CIDR.")
    nm = netmask = property(get_netmask, set_netmask, doc="The netmask of this CIDR.")
    first_ip = property(get_first_ip)
    last_ip = property(get_last_ip)
    network_ip = property(get_network_ip)
    broadcast_ip = property(get_broadcast_ip)
    ip_number = property(get_ip_number)
