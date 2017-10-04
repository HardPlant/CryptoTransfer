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
        pass

    def tearDown(self):
        pass

    def test(self):
        pass


if __name__ == '__main__':
    unittest.main()