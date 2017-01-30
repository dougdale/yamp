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

class Yamp:
    def __init__(self):
        self.passages = []

    @classmethod
    def from_json_dict(cls, d):
        yamp = cls()

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
        for passage in self.passages:
            passage_names.append(passage.passage_name())

        return passage_names

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self, f, cls=YampEncoder)


class YampEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Yamp):
            d = {'passages': []}

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

def main(args):
    '''Entry point when yamp.py is run from command line'''

    cli_yamp = Yamp()

    if args.new:
        cli_yamp.add_passage(args.new.read())
        print(cli_yamp.passage_list())

    cli_yamp.save('yamp.json')

    return 0

if __name__ == '__main__':
    # Handle arguments when run on command line
    formatter_class = argparse.ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter_class)

    parser.add_argument('--new', help="Add new passage from text file",
                        type=argparse.FileType('r'))

    args = parser.parse_args(sys.argv[1:])

    print(args)

    # Call main() with parsed args
    sys.exit(main(args))
