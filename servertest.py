import unittest
from server import EchoServer

class Servertest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testRed(self):
        self.assertEqual(False,True, msg='Absolutely Not.')
        self.assertAlmostEqual(10,10.5,msg="This is not Equal.")

    def testGreen(self):
        self.assertNotEqual(True,False)

if __name__ == '__main__':
    unittest.main()