import unittest
import json

import passage


class WordTest(unittest.TestCase):
    def test_word_init(self):
        w = passage.Word('test')
        self.assertEqual('test', w.text)

    def test_add_try(self):
        w = passage.Word('test')
        w.add_try(1)
        w.add_try(2)
        w.add_try(3)
        w.add_try(4)
        w.add_try(5)
        w.add_try(6)
        w.add_try(7)
        w.add_try(8)
        w.add_try(9)
        w.add_try(10)
        w.add_try(11)
        self.assertEqual([2, 3, 4, 5, 6, 7, 8, 9, 10, 11], w.tries)

    def test_try_average(self):
        w = passage.Word('test')
        self.assertEqual(None, w.try_average())
        w.add_try(2)
        self.assertEqual(2, w.try_average())
        w.add_try(4)
        self.assertEqual(3, w.try_average())

    def test_word_json(self):
        out_word = passage.Word('test')
        out_word.tries = 2
        s = json.dumps(out_word, cls=passage.WordEncoder)
        in_word = json.loads(s, cls=passage.WordDecoder)

        self.assertEqual(2, in_word.tries)
        self.assertEqual('test', in_word.text)


class VerseTest(unittest.TestCase):
    def test_verse_init(self):
        v = passage.Verse(1)
        self.assertEqual(1, v.num)
        self.assertEqual([], v.words)

    def test_verse_add_word(self):
        v = passage.Verse(1)
        v.add_word('one')
        v.add_word('two')
        v.add_word('three')
        self.assertEqual(['one', 'two', 'three'], v.word_list())

    def test_verse_json(self):
        out_verse = passage.Verse(1)
        out_verse.add_word('test')
        s = json.dumps(out_verse, cls=passage.VerseEncoder)
        in_verse = json.loads(s, cls=passage.VerseDecoder)

        self.assertEqual(1, in_verse.num)
        self.assertEqual(['test'], in_verse.word_list())


class PassageTest(unittest.TestCase):
    def setUp(self):
        self.passage_text = '2 Corinthians 4:7 But we have this treasure in jars of clay, ' + \
            'to show that the surpassing power belongs to God and not to us. ' + \
            '8 We are afflicted in every way, but not crushed; perplexed, ' + \
            'but not driven to despair; 9 persecuted, but not forsaken; ' + \
            'struck down, but not destroyed; 10 always carrying in the body the death of Jesus, ' + \
            'so that the life of Jesus may also be manifested in our bodies.'

    def test_passage_init(self):
        p = passage.Passage()
        self.assertEqual([], p.verses)
        self.assertIsNone(p.book)
        self.assertEqual(0, p.chapter)

    def test_passage_bad_parse(self):
        p = passage.Passage()
        self.assertRaises(passage.PassageParseError, p.parse, 'Romans no chapter verse')

    def test_passage_parse(self):
        p = passage.Passage()
        p.parse('Romans 6:1 What shall we say then? Are we to continue in sin that grace may abound?')
        self.assertEqual('Romans', p.book)
        self.assertEqual(6, p.chapter)
        self.assertEqual(1, len(p.verses))
        self.assertEqual(1, p.verses[0].num)
        self.assertEqual('1 What shall we say then? Are we to continue in sin that grace may abound?',
                         str(p.verses[0]))
        self.assertEqual('Romans 6:1', p.passage_name())

    def test_passage_parse2(self):
        p = passage.Passage()

        p.parse(self.passage_text)
        self.assertEqual('2 Corinthians', p.book)
        self.assertEqual(4, p.chapter)
        self.assertEqual(4, len(p.verses))

        self.assertEqual(self.passage_text, str(p))
        self.assertEqual('2 Corinthians 4:7-10', p.passage_name())

    def test_passage_json(self):
        out_passage = passage.Passage()

        out_passage.parse(self.passage_text)
        s = json.dumps(out_passage, cls=passage.PassageEncoder)
        in_passage = json.loads(s, cls=passage.PassageDecoder)

        self.assertEqual(self.passage_text, str(in_passage))
