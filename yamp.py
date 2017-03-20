#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yamp.py
Yet another memorization program.

A program to assist in memorizing Bible verses.
"""

import sys
import argparse
import json

import passage
import getch

class Yamp:
    def __init__(self):
        self.passages = []
        self._miss_limit = 3
        self._mastery_threshold = 1.5

    @property
    def miss_limit(self):
        return self._miss_limit

    @miss_limit.setter
    def miss_limit(self, value):
        if value < 1:
            value = 1
        self._miss_limit = value

    @property
    def mastery_threshold(self):
        return self._mastery_threshold

    @mastery_threshold.setter
    def mastery_threshold(self, value):
        if value < 1.0:
            value = 1.0
        self._mastery_threshold = value

    @classmethod
    def from_json_dict(cls, d):
        yamp = cls()

        yamp.miss_limit = d['miss_limit']
        yamp.mastery_threshold = d['mastery_threshold']
        for passage_dict in d['passages']:
            yamp.add_passage(passage.Passage.from_json_dict(passage_dict))

        return yamp

    def add_passage(self, new_passage):
        if isinstance(new_passage, passage.Passage):
            p = new_passage
        else:
            p = passage.Passage()
            p.parse(new_passage)

        self.passages.append(p)

    def passage_list(self):
        passage_names = []
        for p in self.passages:
            passage_names.append(p.passage_name())

        return passage_names

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self, f, cls=YampEncoder)

    @staticmethod
    def load(filename):
        with open(filename, 'r') as f:
            y = json.load(f, cls=YampDecoder)

        return y


class YampEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Yamp):
            d = {'miss_limit': o.miss_limit,
                 'mastery_threshold': o.mastery_threshold,
                 'passages': []}

            passage_encoder = passage.PassageEncoder()
            for p in o.passages:
                d['passages'].append(passage_encoder.default(p))

            return d

        # Wrong object. Let base class raise error
        return json.JSONEncoder.default(self, o)


class YampDecoder(json.JSONDecoder):
    def decode(self, s, *kwargs):
        d = json.JSONDecoder.decode(self, s, *kwargs)

        return Yamp.from_json_dict(d)


def cl_verse_check(book, chapter, verse, miss_limit):
    print('{} {}:{}'.format(book, chapter, verse.num))

    for word in verse.words:
        done = False
        count = 0

        first_letter = word.text[0].lower()

        while not done:
            c = getch.getch()

            if c in 'abcdefghijklmnopqrstuvwxyz':
                count = count + 1

                if c == first_letter or count >= miss_limit:
                    print(word.text + ' ')
                    word.add_try(count)
                    done = True

    print('')


def main(args):
    """Entry point when yamp.py is run from command line"""

    # Load from yamp.json, otherwise start with new.
    try:
        cli_yamp = Yamp.load('yamp.json')
    except FileNotFoundError:
        cli_yamp = Yamp()

    if args.new:
        cli_yamp.add_passage(args.new.read())

    if args.misses:
        cli_yamp.miss_limit = args.misses

    if args.mastery:
        cli_yamp.mastery_threshold = args.mastery

    print('Miss limit: {}'.format(cli_yamp.miss_limit))
    print('Mastery threshold: {}'.format(cli_yamp.mastery_threshold))
    print(cli_yamp.passage_list())

    selected_passage = cli_yamp.passages[0]

    sequence = selected_passage.generate_review_verses()

    done = False

    while not done:
        cl_verse_check(selected_passage.book, selected_passage.chapter, next(sequence), cli_yamp.miss_limit)

        print('Q to quit, anything else to continue')

        if getch.getch() == 'Q':
            done = True

    cli_yamp.save('yamp.json')

    return 0

if __name__ == '__main__':
    # Handle arguments when run on command line
    formatter_class = argparse.ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter_class)

    parser.add_argument('--new',
                        help="Add new passage from text file",
                        type=argparse.FileType('r'))
    parser.add_argument('--misses',
                        help='New value for number of misses allowed before word is revealed (this is saved by yamp)',
                        type=int)
    parser.add_argument('--mastery',
                        help='New verse mastery threshold (attempts per word - this is saved by yamp)',
                        type=float)
    parser.add_argument('--passage',
                        help='Specify passage to review',
                        type=str)
    parser.add_argument('--mode',
                        help='Review mode (learn or review)',
                        type=str,
                        default='learn')

    cl_args = parser.parse_args(sys.argv[1:])

    print(cl_args)

    # Call main() with parsed args
    sys.exit(main(cl_args))
