import unittest
from server import *


class TestServer(unittest.TestCase):
    def test_build_to_int(self):
        self.assertEqual(build_to_int('01.02.2017'), 20170201)
        self.assertEqual(build_to_int('11.12.2035'), 20351211)

if __name__ == '__main__':
    unittest.main()

