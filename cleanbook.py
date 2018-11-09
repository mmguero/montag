#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import signal
import struct
import re
import argparse
import pprint
from profanity_filter import ProfanityFilter

def main():

  parser = argparse.ArgumentParser(description='e-book profanity scrubber', add_help=False, usage='cleanbook.py [options]')
  requiredNamed = parser.add_argument_group('required arguments')
  requiredNamed.add_argument('-i', '--input', required=True, dest='input', metavar='<STR>', type=str, default='', help='Input file')
  parser.add_argument('-l', '--languages', dest='languages', metavar='<STR>', type=str, default='en', help='Test for profanity using specified languages (comma separated, default: en)')
  parser.add_argument('-w', '--whole-words', dest='censor_whole_words', action='store_true', help='Censor whole words (default: false)')
  try:
    parser.error = parser.exit
    args = parser.parse_args()
  except SystemExit:
    parser.print_help()
    exit(2)

  pf = ProfanityFilter(languages=args.languages.split(','), censor_whole_words=args.censor_whole_words)

  bookLinesCleaned = []
  with open(args.input, "r", encoding="latin-1") as f:
    for line in f.readlines():
      bookLinesCleaned.append(pf.censor(line))

  pprint.pprint(bookLinesCleaned)

if __name__ == '__main__': main()
