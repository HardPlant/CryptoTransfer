import unittest
import struct

class testLea(unittest.TestCase):
    def testbyte(self):
        string = "aHello WorldaHello World"
        ba = bytearray(string,'UTF-8')
        for item in ba:
            print(item)
        print(ba[:8])
        b = bytes(string,'UTF-8')
        assert(ba[:8] == b[:8])
        print(struct.unpack('<LLLL',ba[:16]))




if __name__ == '__main__':
    unittest.main()