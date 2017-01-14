import unittest
import passage


class WordTest(unittest.TestCase):
    def test_word_init(self):
        w = passage.Word('test')
        self.assertEqual('test', w.text)