import unittest
from CustomCrypto.LEA import LEA
from unittest.mock import patch
from server import EchoServer
from client import EchoClient


@patch('server.EchoServer')
@patch('client.EchoClient')
class Servertest(unittest.TestCase):
    def setUp(self):
        self.server = EchoServer()
        self.client = EchoClient()
        self.server.start()

    def tearDown(self):
        self.client.close()
        self.server.stop()

    def passtestecho(self):
        data = self.client.send()
        self.assertEqual(data, "Hello, world", "data not equal.")


class CryptoTest(unittest.TestCase):
    def setUp(self):
        self.encryptor = LEA(bytes(1)*32)
        print()

    def tearDown(self):
        pass

    def testLEA(self):
        plain = bytes("Hello World" + " "*5, 'utf-8')
        self.assertEqual(type(plain), type(bytes()))

        encrypted = self.encryptor.encrypt(plain)
        self.assertEqual(type(encrypted), type(bytearray()))
        print(encrypted)

        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(type(decrypted), type(bytearray()))
        print(decrypted)

        p = decrypted.decode('utf-8')
        print(p)


if __name__ == '__main__':
    unittest.main()