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

  # extract arguments from the command line
  # print (sys.argv[1:]);
  parser = argparse.ArgumentParser(description='e-book profanity scrubber', add_help=False, usage='cleanbook.py [options]')
  requiredNamed = parser.add_argument_group('required arguments')
  requiredNamed.add_argument('-i', '--input', required=True, dest='input', metavar='<STR>', type=str, nargs=1, default='', help='Input file')
  parser.add_argument('-l', '--languages', dest='languages', metavar='<STR>', type=str, nargs=1, default='en', help='Test for profanity using specified languages (comma separated, default: en)')
  try:
    parser.error = parser.exit
    args = parser.parse_args()
  except SystemExit:
    parser.print_help()
    exit(2)

  pf = ProfanityFilter(languages=args.languages.split(','))

if __name__ == '__main__': main()
