import unittest
import unittest.mock
import requests

from CustomCrypto.LEA import LEA
from server import EchoServer
from client import EchoClient

def get_data(url):
    resp = requests.get(url)
    return resp

class Servertest(unittest.TestCase):
    def setUp(self):
        pass
#        self.server = EchoServer()
#        self.client = EchoClient()
#        self.server.start()

    def tearDown(self):
        pass
#        self.client.close()
#        self.server.stop()

    def passtestecho(self):
        pass
#        data = self.client.send()
#        self.assertEqual(data, "Hello, world", "data not equal.")

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

    def request_recv_send_test(self):
        pass



if __name__ == '__main__':
    unittest.main()