import re


class Word:
    def __init__(self, text):
        self.tries = 0
        self.text = text


class Verse:
    def __init__(self, num):
        self.num = num
        self.words = []

    def add_word(self, word):
        self.words.append(Word(word))

    def __str__(self):
        versestr = str(self.num)

        for word in self.words:
            versestr = versestr + ' ' + word.text

        return versestr


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

        self.chapter = m.group('chapter')

        # Create a verse object using the first verse number
        verse = Verse(int(m.group('verse')))

        # Loop thorugh every 'word' in the passage
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

    def __str__(self):
        passagestr = '{} {}:'.format(self.book, self.chapter)

        for verse in self.verses:
            passagestr = passagestr + verse.__str__() + ' '


if __name__ == '__main__':
    passage = Passage()

    with open("romans6.txt") as f:
        passage.parse(f.read())

    print('Passage:')
    print(passage)
