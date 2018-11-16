#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import pprint
import subprocess
import magic
import ebooklib
from ebooklib import epub
from profanity_filter import ProfanityFilter

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def tagTokenizer(s):
  inTag = False
  lastChar = None
  tokenPosStart = 0
  lastYieldEnd = -1
  for i, char in enumerate(s):
    if inTag and (char == '>') and (lastChar != '\\'):
      inTag = False
      if (i >= tokenPosStart):
        # print(f"TAG: {s[tokenPosStart:i+1]}")
        yield s[tokenPosStart:i+1]
        lastYieldEnd = i
      tokenPosStart = i+1
    elif (not inTag) and (char == '<') and (lastChar != '\\'):
      inTag = True
      if (i > tokenPosStart):
        # print(f"TXT: {s[tokenPosStart:i]}")
        yield s[tokenPosStart:i]
        lastYieldEnd = i-1
      tokenPosStart = i
    lastChar = char

  if (len(s) > lastYieldEnd):
    # print(f"END: [{s[lastYieldEnd+1:len(s)]}]")
    yield s[lastYieldEnd+1:len(s)]

METADATA_FILESPEC = "/tmp/metadata.opf"
def main():
  devnull = open(os.devnull, 'w')

  parser = argparse.ArgumentParser(description='e-book profanity scrubber', add_help=False, usage='montag.py [options]')
  requiredNamed = parser.add_argument_group('required arguments')
  requiredNamed.add_argument('-i', '--input', required=True, dest='input', metavar='<STR>', type=str, default='', help='Input file')
  requiredNamed.add_argument('-o', '--output', required=True, dest='output', metavar='<STR>', type=str, default='', help='Output file')
  parser.add_argument('-l', '--languages', dest='languages', metavar='<STR>', type=str, default='en', help='Test for profanity using specified languages (comma separated, default: en)')
  parser.add_argument('-w', '--whole-words', dest='censor_whole_words', action='store_true', help='Censor whole words (default: false)')
  parser.add_argument('-d', '--deep', dest='deep_analysis', action='store_true', help='Deep analysis (default: false, may cause some issues depending on word list)')
  try:
    parser.error = parser.exit
    args = parser.parse_args()
  except SystemExit:
    parser.print_help()
    exit(2)

  # initialize the profanity filter
  pf = ProfanityFilter(languages=args.languages.split(','), censor_whole_words=args.censor_whole_words, deep_analysis=args.deep_analysis)

  # determine the type of the ebook
  bookMagic = "application/octet-stream"
  with magic.Magic() as m:
    bookMagic = m.id_filename(args.input)

  eprint(f"Processing \"{args.input}\" of type \"{''.join(bookMagic)}\"")

  # save off the metadata to be restored after conversion
  eprint(f"Extracting metadata...")
  metadataExitCode = subprocess.call(["/usr/bin/ebook-meta", args.input, "--to-opf="+METADATA_FILESPEC], stdout=devnull, stderr=devnull)
  if (metadataExitCode != 0):
    raise subprocess.CalledProcessError(metadataExitCode, f"/usr/bin/ebook-meta {args.input} --to-opf={METADATA_FILESPEC}")

  # convert the book from whatever format it is into epub for conversion
  if "epub" in bookMagic.lower():
    epubFileSpec = args.input
    wasEpub = True
  else:
    wasEpub = False
    epubFileSpec = "/tmp/ebook.epub"
    eprint(f"Converting to EPUB...")
    toEpubExitCode = subprocess.call(["/usr/bin/ebook-convert", args.input, epubFileSpec], stdout=devnull, stderr=devnull)
    if (toEpubExitCode != 0):
      raise subprocess.CalledProcessError(toEpubExitCode, f"/usr/bin/ebook-convert {args.input} {epubFileSpec}")

  # todo: somehow links/TOCs tend to get messed up

  eprint(f"Processing book contents...")
  book = epub.read_epub(epubFileSpec)
  newBook = epub.EpubBook()
  newBook.spine = ['nav']
  documentNumber = 0
  for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
      documentNumber += 1
      cleanTokens = []
      for token in tagTokenizer(item.get_content().decode("latin-1")):
        trimmedToken = token.strip()
        if (len(trimmedToken) <= 2) or (trimmedToken.startswith('<') and trimmedToken.endswith('>')):
          # print(f"including: {token}")
          cleanTokens.append(token)
        else:
          # print(f"censoring: {token}")
          cleanTokens.append(pf.censor(token))
        #if (len(cleanTokens) % 100 == 0):
          #eprint(f"Processed {len(cleanTokens)} tokens from section {documentNumber}...")
      item.set_content(''.join(cleanTokens).encode("latin-1"))
      newBook.spine.append(item)
      newBook.add_item(item)
    else:
      newBook.add_item(item)
  book.add_item(epub.EpubNcx())
  book.add_item(epub.EpubNav())

  # write epub (either final or intermediate)
  eprint(f"Generating output...")
  if args.output.lower().endswith('.epub'):
    epub.write_epub(args.output, newBook)
  else:
    cleanEpubFileSpec = "/tmp/ebook_cleaned.epub"
    epub.write_epub(cleanEpubFileSpec, newBook)
    eprint(f"Converting...")
    fromEpubExitCode = subprocess.call(["/usr/bin/ebook-convert", cleanEpubFileSpec, args.output], stdout=devnull, stderr=devnull)
    if (fromEpubExitCode != 0):
      raise subprocess.CalledProcessError(toEpubExitCode, f"/usr/bin/ebook-convert {cleanEpubFileSpec} {args.output}")

  # restore metadata
  eprint(f"Restoring metadata...")
  metadataExitCode = subprocess.call(["/usr/bin/ebook-meta", args.output, "--from-opf="+METADATA_FILESPEC], stdout=devnull, stderr=devnull)
  if (metadataExitCode != 0):
    raise subprocess.CalledProcessError(metadataExitCode, f"/usr/bin/ebook-meta {args.output} --from-opf={METADATA_FILESPEC}")

if __name__ == '__main__': main()
