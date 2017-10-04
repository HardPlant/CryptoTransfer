import unittest
from unittest import mock
import requests
import CustomCrypto.LEA as LEA
import server
import client


class Servertest(unittest.TestCase):
    def setUp(self):
        self.encrypt = LEA.ECB(True, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        self.decrypt = LEA.ECB(False, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        self.plain = "BUY IBM STOCK AND BIT COINS, THEN YOU WILL GAIN SOME MONEY"
        self.enc = self.encrypt.encrypt(self.plain) + self.encrypt.final()
        self.dec = self.decrypt.decrypt(self.enc) + self.decrypt.final()

    def tearDown(self):
        pass

    def testEncrypted(self):
        enc = server.response("BUY IBM STOCK AND BIT COINS, THEN YOU WILL GAIN SOME MONEY")
        self.assertEqual(enc, self.enc)


def get_data(url):
    resp = requests.get(url)
    return resp

class GetDataTest(unittest.TestCase):
    def test_get_data(self):
        with unittest.mock.patch.object(requests,'get') as get_mock:
            get_mock.return_value = mock_response = unittest.mock.Mock()
            mock_response.status_code = 200
            mock_response.content = {'Help!' : 'Hello'}
            resp = get_data("http://hello.com")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content['Help!'], 'Hello')

class CryptoTest(unittest.TestCase):
    def setUp(self):
        self.encryptor = LEA.LEA(bytes(1)*32)
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

        p = decrypted.decode('utf-8')

    def testCBC(self):
        tool = LEA.ECB(True, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        plain = 'Hello World With lesser guyes and What are you saying bitch!?'
        encrypt = tool.encrypt(plain)
        encryptfinal = tool.final()

        tool = LEA.ECB(False, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        decrypt = tool.decrypt(encrypt+encryptfinal)
        decryptfinal = tool.final()

def get_input(text):
    return input(text)

def answer():
    ans = get_input('enter yes or no')

class InputTest(unittest.TestCase):
    def test_answer_yes(self, input):
        self.assertEqual(answer(), 'you entered yes')



if __name__ == '__main__':
    unittest.main()