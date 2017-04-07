import unittest


class TestTransaction(unittest.TestCase):
    def test_basic1(self):
        a = 1
        self.assertEqual(1, a)
