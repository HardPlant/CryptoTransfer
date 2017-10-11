import unittest
from unittest import mock
import requests
import CustomCrypto.LEA as LEA
import server
import client


class Servertest(unittest.TestCase):
    def setUp(self):
        self.encrypt = LEA.ECB(True, bytes('A', encoding='utf-8') * 32, PKCS5Padding=True)
        self.decrypt = LEA.ECB(False, bytes('A', encoding='utf-8') * 32, PKCS5Padding=True)
        self.plain = "BUY IBM STOCK AND BIT COINS, THEN YOU WILL GAIN SOME MONEY"
        self.enc = self.encrypt.final()
        self.dec = self.decrypt.final()

    def tearDown(self):
        pass


class CryptoTest(unittest.TestCase):
    def setUp(self):
        self.encryptor = LEA.LEA(bytes(1) * 32)
        print()

    def tearDown(self):
        pass

    def testLEA(self):
        plain = bytes("Hello World" + " "*5, 'utf-8')
        self.assertEqual(type(plain), type(bytes()))

        encrypted = self.encryptor.encrypt(plain)
        self.assertEqual(type(encrypted), type(bytearray()))

        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(type(decrypted), type(bytearray()))
        self.assertEqual(plain,decrypted)

    def testECB(self):
        tool = LEA.ECB(True, bytes('A', encoding='utf-8') * 32, PKCS5Padding=True)
        plain = 'Hello World With lesser guyes and What are you saying bitch!?'
        encrypt = tool.encrypt(plain)
        encryptfinal = tool.final()

        tool = LEA.ECB(False, bytes('A', encoding='utf-8') * 32, PKCS5Padding=True)
        decrypt = tool.decrypt(encrypt+encryptfinal)
        decryptfinal = tool.final()
        self.assertEqual(plain, (decrypt+decryptfinal).decode())


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.server = server.EchoServer()
        self.server.start()
        self.client = client.Client()


    def tearDown(self):
        self.server.stop()
        print("tearDown returns")

    def testInit(self):
        data = self.client.send("Hi!")
        print("Hi! returns")
        self.assertEqual(data.decode(), "Hi!")
        data = self.client.send("Hello!")
        print("Hello! returns")
        self.assertEqual(data.decode(), "Hello!")
        data = self.client.send("Toure")
        self.assertEqual(data.decode(), "Toure")
        print("Tour! returns")
        connector = self.server.get_connector()
        print("Last connector : ")
        print(connector)

class CTRTest(unittest.TestCase):
    def setUp(self):
        self.server = server.EchoServer(mode='CTR')
        self.server.start()
        self.client = client.Client(mode='CTR')

    def tearDown(self):
        self.server.stop()

    def testInit(self):
        data = self.client.send("Hi!")
        print("Hi! returns")
        self.assertEqual(data.decode(), "Hi!")
        data = self.client.send("Hello!")
        print("Hello! returns")
        self.assertEqual(data.decode(), "Hello!")
        data = self.client.send("Toure")
        self.assertEqual(data.decode(), "Toure")
        print("Tour! returns")
        long_word = "LongWord"*75
        data = self.client.send(long_word)
        self.assertEqual(data.decode(), long_word)
        connector = self.server.get_connector()
        print("Last connector : ")
        print(connector)


if __name__ == '__main__':
    unittest.main()