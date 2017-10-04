import unittest
from unittest import mock
import requests
import CustomCrypto.LEA as LEA
from server import EchoServer
from client import EchoClient

def get_data(url):
    resp = requests.get(url)
    return resp

class Servertest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEncrypted(self):
        pass




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
        print(encrypted)

        decrypted = self.encryptor.decrypt(encrypted)
        self.assertEqual(type(decrypted), type(bytearray()))
        print(decrypted)

        p = decrypted.decode('utf-8')
        print(p)

    def testCBC(self):
        tool = LEA.ECB(True, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        plain = 'Hello World With lesser guyes and What are you saying bitch!?'
        encrypt = tool.encrypt(plain)
        print(len(tool.buffer))
        encryptfinal = tool.final()
        print(encrypt+encryptfinal)

        tool = LEA.ECB(False, bytes('A',encoding='utf-8')*32,PKCS5Padding=True)
        decrypt = tool.decrypt(encrypt+encryptfinal)
        decryptfinal = tool.final()
        print(decrypt.decode() + decryptfinal.decode())

    def request_recv_send_test(self):
        pass



if __name__ == '__main__':
    unittest.main()