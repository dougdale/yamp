#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yamp.py
Yet another memorization program.

A program to assist in memorizing Bible verses.
"""

import sys
import argparse

import passage

class Yamp:
    def __init__(self):
        self.passages = []

    def add_passage(self, text):
        p = passage.Passage()
        p.parse(text)
        self.passages.append(p)

    def passage_list(self):
        passage_names = []
        for passage in self.passages:
            passage_names.append(passage.passage_name())

        return passage_names

def main(args):
    '''Entry point when yamp.py is run from command line'''

    cli_yamp = Yamp()

    if args.new:
        cli_yamp.add_passage(args.new.read())
        print(cli_yamp.passage_list())

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
