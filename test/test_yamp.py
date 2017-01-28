import unittest
import yamp

class YampTest(unittest.TestCase):
    def test_yamp_init(self):
        y = yamp.Yamp()
        self.assertEqual([], y.passages)