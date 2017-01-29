import re
import json


class Word:
    def __init__(self, text, tries=0):
        self.tries = tries
        self.text = text


class WordEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Word):
            return o.__dict__

        # Wrong object. Let base class raise error
        return json.JSONEncoder.default(self, o)


class WordDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)
        return Word(d['text'], tries=d['tries'])


class Verse:
    def __init__(self, num, words=None):
        self.num = num
        if words:
            self.words = words
        else:
            self.words = []

    def add_word(self, word):
        if not isinstance(word, Word):
            word = Word(word)

        self.words.append(word)

    def word_list(self):
        return [w.text for w in self.words]

    def __str__(self):
        return '{} {}'.format(self.num, ' '.join(self.word_list()))


class VerseEncoder(json.JSONEncoder):
    def default(self, o):
        d = {'num': o.num, 'words': []}
        word_encoder = WordEncoder()
        for w in o.words:
            d['words'].append(word_encoder.default(w))

        return d


class VerseDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)

        v = Verse(d['num'])

        for word_info in d['words']:
            v.add_word(Word(word_info['text'], word_info['tries']))
            
        return v


class PassageParseError(Exception):
    pass


class Passage:
    def __init__(self):
        self.verses = []
        self.book = None
        self.chapter = 0

    def parse(self, text):
        items = text.split()

        # Get the book
        self.book = items.pop(0)

        # Check for a case like '1 Corinthians'
        if self.book.isdigit():
            self.book = self.book + ' ' + items.pop(0)

        # Get the chapter and first verse number
        m = re.match(r'(?P<chapter>\d+):(?P<verse>\d+)', items.pop(0))

        if not m:
            raise PassageParseError('Passage does not start with chapter:verse')

        self.chapter = int(m.group('chapter'))

        # Create a verse object using the first verse number
        verse = Verse(int(m.group('verse')))

        # Loop through every 'word' in the passage
        for item in items:
            # If the item is all digits, assume a verse number
            if item.isdigit():
                # Save the current verse
                self.verses.append(verse)

                # Create a new verse object with the current number
                verse = Verse(int(item))
            else:
                verse.add_word(item)

        self.verses.append(verse)

    def passage_name(self):
        s = '{} {}:{}'.format(self.book, self.chapter, self.verses[0].num)
        if len(self.verses) > 1:
            s = s + '-{}'.format(self.verses[-1].num)

        return s

    def __str__(self):
        s = '{} {}:'.format(self.book, self.chapter)
        for v in self.verses:
            s = s + str(v) + ' '

        return s.rstrip()

