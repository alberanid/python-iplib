#!/usr/bin/env python

import sys, random, unittest
import iplib

# Functions and values to test.
#   funct_name: (funct, [list of valid values], [list of invalid values])
FUNCTIONS = {
    'is_dot': (iplib.is_dot,
                ['1.2.3.4', '0.0.0.0', '255.255.255.255'],
                ['1.2.3', '1.2.3.4.5', '-1.2.3.4', '256.0.0.0', '0.0.0.256'
                    '10', '', 'a', '...', 'a.b.c.d', '1.2.3.']),
    'is_hex': (iplib.is_hex,
                ['0', '0x0', '0x000000', '0xffffffff', '0', '123'],
                ['', '0x100000000L', '-1', '0xefg', '0x']),
    'is_bin': (iplib.is_bin,
                ['00000000000000000000000000000000',
                    '11111111111111111111111111111111',
                    '01111111111111111111111111111111'],
                ['', '0000000000000000000000000000000', '1',
                    '111111111111111111111111111111111',
                    '00000000000000000000000000000002']),
    'is_oct': (iplib.is_oct,
                ['0', '037777777777', '007777777777', '7777777', '7777777L'],
                ['', 'a', '040000000000', '040000000000L', '-1']),
    'is_dec': (iplib.is_dec,
                ['0', '4294967295', '4294967295L', '294967295', '294967295L'],
                ['', 'a', '4294967296', '4294967296L', '-1']),
    'is_dot_nm': (iplib.is_dot_nm,
                ['0.0.0.0', '255.255.255.255', '255.0.0.0', '255.255.255.0'],
                ['', '0.0.0.0.0', '255.255.256.255', '0.255.0.0', 'a', '...',
                    '0.255.255.255']),
    'is_hex_nm': (iplib.is_hex_nm,
                ['0x0', '0xFFFFFFFF', '0xFFFFFFFFL','0xFF000000', '0xFFFFFF00'],
                ['', '0xFF000001', '0xFEEEEEEE']),
    'is_bin_nm': (iplib.is_bin_nm,
                ['00000000000000000000000000000000',
                    '11111111111111111111111111111111',
                    '11111111000000000000000000000000'],
                ['', '0', '0000000000000000000000000000000',
                    '00000000000000000000000000000002']),
    'is_oct_nm': (iplib.is_oct_nm,
                ['0', '00', '037777777777', '037700000000', '037777777400'],
                ['', '-1', '037777777775', '037700000001']),
    'is_dec_nm': (iplib.is_dec_nm,
                ['0', '4294967040', '4294967295', '4294967040'],
                ['', 'a', '4294967039', '4294967293', '4294967296']),
    'is_bits_nm': (iplib.is_bits_nm,
                [str(x) for x in xrange(0, 33)],
                ['', '-1', '33', 'a']),
    'is_wildcard_nm': (iplib.is_wildcard_nm,
                ['255.255.255.255', '0.0.0.0', '0.255.255.255'],
                ['', '...', 'a.b.c.d', '0.0.0.0.0', '0.255.255.254',
                    '255.0.255.255', '0.255.255.256']),
}


class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        errtxt = 'FAILURE (function %s): %s ' % \
                    (test.functName, test.currentValue)
        if test.shouldBevalid: errtxt += 'should NOT be VALID!'
        else: errtxt += 'should be VALID!'
        errtxt += '\n'
        sys.stderr.write(errtxt)
        unittest.TestResult.addFailure(self, test, err)

mytestres = MyTestResult()


class NotationsTest(unittest.TestCase):
    """Test functions used to check if an IP is in a given notation."""
    currentValue = None
    shouldBevalid = None

    def defaultTestResult(self): return mytestres


def runNotationsTest():
    for key in FUNCTIONS:
        print 'TESTING %s... ' % key
        funct, valid, invalid = FUNCTIONS[key]
        def runTest(self):
            self.shouldBevalid = True
            self.functName = key
            for valid_val in valid:
                self.currentValue = valid_val
                self.failUnless(funct(valid_val))
            self.shouldBevalid = False
            for invalid_val in invalid:
                self.currentValue = invalid_val
                self.failIf(funct(invalid_val))
        setattr(NotationsTest, 'runTest', runTest)
        test = NotationsTest()
        test.run()


class TestConvert(unittest.TestCase):
    """Test conversion amongst different notations."""
    def test_ip(self):
        """Generate a number of random decimal IP; convert every IP in
        other notations and back, checking for differences."""
        testDecIPs = ['0', '4294967295']
        while len(testDecIPs) < 10000:
            randIP = str(random.randrange(4294967296L))
            if randIP not in testDecIPs: testDecIPs.append(randIP)
        for ip in testDecIPs:
            for notation in ('hex', 'bin', 'oct', 'dec'):
                converted = iplib.convert(ip, notation=notation,
                                            inotation=iplib.IP_DEC, check=0)
                reverted = iplib.convert(converted, notation=iplib.IP_DEC,
                                            inotation=notation, check=0)
                self.failIf(ip != reverted)

    def test_nm(self):
        """convert every valid decimal NM in other notations and back,
        checking for differences."""
        testBitNMs = [str(x) for x in iplib.VALID_NETMASKS.keys()]
        notations = [x[0] for x in iplib.NOTATION_MAP.values()]
        notations.remove('unknown')
        for nm in testBitNMs:
            for notation in notations:
                converted = iplib.convert_nm(nm, notation=notation,
                                            inotation=iplib.NM_BITS, check=0)
                reverted = iplib.convert_nm(converted, notation=iplib.NM_BITS,
                                            inotation=notation, check=0)
                self.failIf(nm != reverted)


class TestIPv4Address(unittest.TestCase):
    def test_ip1(self):
        ip = iplib.IPv4Address('127.0.0.1')
        self.failIf(ip != '127.0.0.1')
        self.failIf(ip >= '127.0.0.2')
        self.failIf(ip <= '127.0.0.0')
        self.failUnless(ip == '127.0.0.1')
        self.failUnless(ip == iplib.IPv4Address('127.0.0.1'))

    def test_ip2(self):
        ip = iplib.IPv4Address('127.0.0.1')
        self.failUnless(ip.get_dot() == '127.0.0.1')
        self.failUnless(ip.get_hex() == '0x7F000001')
        self.failUnless(hex(ip) == '0x7F000001')
        self.failUnless(ip.get_bin() == '01111111000000000000000000000001')
        self.failUnless(ip.get_dec() == '2130706433')
        self.failUnless(int(ip) == 2130706433)
        self.failUnless(ip.get_oct() == '017700000001')
        self.failUnless(oct(ip) == '017700000001')

    def test_ip3(self):
        ip = iplib.IPv4Address('127.0.0.1')
        self.failUnless(ip + 0 == ip)
        self.failUnless(ip - 0 == ip)

    def test_ip4(self):
        ip1 = iplib.IPv4Address('127.0.0.1')
        ip2 = iplib.IPv4Address('127.0.0.1')
        self.failIf(ip1 is ip2)
        self.failIf(ip1 != ip2)
        self.failIf(ip1 is ip1 + 0)
        self.failIf(ip1 is ip1 - 0)
        self.failIf(ip1 + 1 != iplib.IPv4Address('127.0.0.2'))
        self.failIf(ip1 - 1 != iplib.IPv4Address('127.0.0.0'))
        self.failIf(1 + ip1 != iplib.IPv4Address('127.0.0.2'))
        self.failIf(1 - ip1 != iplib.IPv4Address('127.0.0.0'))
        _idip1 = id(ip1)
        ip1 += 0
        self.failIf(id(ip1) != _idip1)
        ip1 += 1
        self.failIf(id(ip1) != _idip1)
        ip1 -= 1
        self.failIf(id(ip1) != _idip1)
        ip1 -= 0
        self.failIf(id(ip1) != _idip1)


class TestIPv4NetMask(unittest.TestCase):
    def test_nm1(self):
        nm = iplib.IPv4NetMask('255.0.0.0')
        self.failUnless(nm == '255.0.0.0')
        self.failUnless(nm == '037700000000')
        self.failUnless(nm == '4278190080')
        self.failUnless(nm == '8')

    def test_nm2(self):
        nm = iplib.IPv4NetMask('255.0.0.0')
        self.failUnless(nm.get_bits() == '8')
        self.failUnless(nm.get_wildcard() == '0.255.255.255')

class TestCIDR(unittest.TestCase):
    def test_cidr1(self):
        cidr1 = iplib.CIDR('127.0.0.1/28')
        cidr2 = iplib.CIDR('127.0.0.1', '28')
        self.failIf(cidr1 != cidr2)

    def test_cidr2(self):
        cidr1 = iplib.CIDR('127.0.0.1/28')
        cidr2 = iplib.CIDR('0x7F000001', '037777777760')
        self.failIf(cidr1 != cidr2)

    def test_cidr3(self):
        cidr1 = iplib.CIDR('127.0.0.1/28')
        cidr2 = iplib.CIDR('127.0.0.1/8')
        self.failIf(cidr1 >= cidr2)

    def test_cidr4(self):
        cidr1 = iplib.CIDR('127.0.0.1/26')
        cidr2 = iplib.CIDR('127.0.0.2/26')
        self.failIf(cidr1 >= cidr2)

    def test_cidr5(self):
        cidr = iplib.CIDR('127.0.0.1/10')
        ip1 = iplib.IPv4Address('127.0.0.1')
        ip2 = iplib.IPv4Address('127.0.0.2')
        ip3 = iplib.IPv4Address('127.20.10.5')
        ip4 = iplib.IPv4Address('127.63.255.254')
        ipN = iplib.IPv4Address('127.0.0.0')
        ipB = iplib.IPv4Address('127.63.255.255')
        self.failUnless(ip1 in cidr)
        self.failUnless(ip2 in cidr)
        self.failUnless(ip3 in cidr)
        self.failUnless(ip4 in cidr)
        self.failIf(ipN in cidr)
        self.failIf(ipB in cidr)

    def test_cidr6(self):
        cidr = iplib.CIDR('127.0.0.1/31')
        ip1 = iplib.IPv4Address('127.0.0.0')
        ip2 = iplib.IPv4Address('127.0.0.1')
        self.failUnless(ip1 in cidr)
        self.failUnless(ip2 in cidr)
        self.failIf(iplib.IPv4Address('126.255.255.255') in cidr)
        self.failIf(iplib.IPv4Address('127.0.0.2') in cidr)

    def test_cidr7(self):
        cidr = iplib.CIDR('127.0.0.1/32')
        ip1 = iplib.IPv4Address('127.0.0.1')
        self.failUnless(ip1 in cidr)
        self.failIf(iplib.IPv4Address('127.0.0.0') in cidr)
        self.failIf(iplib.IPv4Address('127.0.0.2') in cidr)

    def test_cidr8(self):
        cidrBIG = iplib.CIDR('192.0.0.0/8')
        cidrSMALL = iplib.CIDR('192.0.0.0/30')
        cidrFUNNY = iplib.CIDR('192.0.0.0/31')
        self.failIf(cidrBIG in cidrSMALL)
        self.failUnless(cidrSMALL in cidrBIG)
        self.failUnless(cidrBIG in cidrBIG)
        self.failUnless(cidrSMALL in cidrSMALL)
        self.failIf(cidrSMALL in cidrFUNNY)
        self.failUnless(cidrFUNNY in cidrSMALL)

    def test_cidr_len(self):
        cidr = iplib.CIDR('127.0.0.1/28')
        self.failIf(len(cidr.get_all_valid_ip()) != 14)



if __name__ == '__main__':
    runNotationsTest()
    print 'TESTING conversion... '
    unittest.main()


