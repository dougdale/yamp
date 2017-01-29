import unittest
import yamp

class YampTest(unittest.TestCase):
    def test_yamp_init(self):
        y = yamp.Yamp()
        self.assertEqual([], y.passages)

    def test_yamp_add_passage(self):
        y = yamp.Yamp()
        passage_text = 'Romans 6:1 What shall we say then? Are we to continue in sin that grace may abound?'
        y.add_passage(passage_text)
        self.assertEqual(passage_text, str(y.passages[0]))
        self.assertEqual(['Romans 6:1'], y.passage_list())
