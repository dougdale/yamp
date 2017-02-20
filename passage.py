import re
import json


class Word:
    def __init__(self, text):
        self.tries = []
        self.text = text

    @classmethod
    def from_json_dict(cls, d):
        word = cls(d['text'])
        word.tries = d['tries']

        return word

    def add_try(self, count):
        self.tries.append(count)

        # Make sure list never exceeds 10 items
        if len(self.tries) > 10:
            self.tries = self.tries[-10:]

    def try_average(self):
        length = len(self.tries)

        if length:
            average = float(sum(self.tries))/length
        else:
            # Return None if no attempts
            average = None

        return average


class WordEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Word):
            return o.__dict__

        # Wrong object. Let base class raise error
        return json.JSONEncoder.default(self, o)


class WordDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)
        return Word.from_json_dict(d)


class Verse:
    def __init__(self, num):
        self.num = num
        self.words = []

    @classmethod
    def from_json_dict(cls, d):
        verse = cls(d['num'])

        for word_dict in d['words']:
            verse.add_word(Word.from_json_dict(word_dict))

        return verse

    def add_word(self, word):
        if not isinstance(word, Word):
            word = Word(word)

        self.words.append(word)

    def word_list(self):
        return [w.text for w in self.words]

    def mastery_score(self):
        sum = 0
        count = 0

        for word in words:
            average = word.try_average()

            if not average:
                return None
            else:
                sum += average
                count = count + 1

        return sum/float(count)

    def __str__(self):
        return '{} {}'.format(self.num, ' '.join(self.word_list()))


class VerseEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Verse):
            d = {'num': o.num, 'words': []}
            word_encoder = WordEncoder()
            for w in o.words:
                d['words'].append(word_encoder.default(w))

            return d

        # Wrong object. Let base class raise error
        return json.JSONEncoder.default(self, o)


class VerseDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)

        return Verse.from_json_dict(d)


class PassageParseError(Exception):
    pass


class Passage:
    def __init__(self):
        self.verses = []
        self.book = None
        self.chapter = 0

        # Iteration info
        self.iter_mode = None
        self.iter_index = 0

    @classmethod
    def from_json_dict(cls, d):
        passage = cls()

        passage.book = d['book']
        passage.chapter = d['chapter']

        for verse_dict in d['verses']:
            passage.add_verse(Verse.from_json_dict(verse_dict))

        return passage

    def add_verse(self, verse):
        self.verses.append(verse)

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

        self.add_verse(verse)

    def passage_name(self):
        s = '{} {}:{}'.format(self.book, self.chapter, self.verses[0].num)
        if len(self.verses) > 1:
            s += '-{}'.format(self.verses[-1].num)

        return s

    def __str__(self):
        s = '{} {}:'.format(self.book, self.chapter)
        for v in self.verses:
            s = s + str(v) + ' '

        return s.rstrip()

    def generate_learn_verses(self):
        max = 0
        max_verse = None

        for verse in self.verses:
            score = verse.mastery_score()

            # If we find a verse that has not been attempted, immediately return
            # its index. Otherwise, look for the maximum mastery score.
            if not score:
                yield verse
            else:
                if score > max:
                    max = score
                    max_verse = verse

        # Yield the index of the maximum mastery score.
        # Note that this generator never ends!!!
        yield max_verse

    def generate_review_verses(self):
        for verse in self.verses:
            yield verse

        raise StopIteration


class PassageEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Passage):
            d = {'book': o.book, 'chapter': o.chapter, 'verses': []}
            verse_encoder = VerseEncoder()
            for v in o.verses:
                d['verses'].append(verse_encoder.default(v))

            return d

        # Wrong object. Let base class raise error
        return json.JSONEncoder.default(self, o)


class PassageDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)

        return Passage.from_json_dict(d)
