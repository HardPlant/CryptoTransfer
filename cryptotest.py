import unittest

from CustomCrypto.LEA import CBC
from CustomCrypto.LEA.MAC import getMAC


class testLea(unittest.TestCase):
    def testMAC(self):
        key = 'AAAAAAAAAAAAAAAA'
        plaintext = 'Hello World, All of these days. who knows? let me show!'
        tool = CBC(True, key, plaintext[0:8],PKCS5Padding=True)
        crypt = tool.encrypt(plaintext)
        crypt += tool.final()
        print(crypt[:-16])
        print(getMAC(plaintext, key))




if __name__ == '__main__':
    unittest.main()