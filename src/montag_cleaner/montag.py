#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import subprocess
import re
import tempfile

import magic
import ebooklib

from ebooklib import epub
from tempfile import gettempdir

textSplitRegex = re.compile(r'\w+|\W+', re.DOTALL | re.MULTILINE | re.U)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def tagTokenizer(s):  # yields (returns) strNeedsCensoring, str
    inTag = False
    lastChar = None
    tokenPosStart = 0
    lastYieldEnd = -1
    for i, char in enumerate(s):
        if inTag and (char == '>') and (lastChar != '\\'):
            # we are in an HTML tag, no need to censor anything
            inTag = False
            if i >= tokenPosStart:
                # eprint(f"TAG: {s[tokenPosStart:i+1]}")
                yield False, s[tokenPosStart : i + 1]
                lastYieldEnd = i
            tokenPosStart = i + 1
        elif (not inTag) and (char == '<') and (lastChar != '\\'):
            # we are not in an HTML tag, split up words/non-words and
            # only censor the words
            inTag = True
            if i > tokenPosStart:
                for textToken in re.findall(textSplitRegex, s[tokenPosStart:i]):
                    # eprint(f"TXT: {textToken}")
                    yield ((len(textToken) > 2) and textToken[:1].isalpha()), textToken
                lastYieldEnd = i - 1
            tokenPosStart = i
        lastChar = char

    if len(s) > lastYieldEnd:
        if inTag:
            yield False, s[lastYieldEnd + 1 : len(s)]
        else:
            for textToken in re.findall(textSplitRegex, s[lastYieldEnd + 1 : len(s)]):
                yield ((len(textToken) > 2) and textToken[:1].isalpha()), textToken


def RunMontag():
    devnull = open(os.devnull, 'w')

    parser = argparse.ArgumentParser(
        description='e-book profanity scrubber', add_help=False, usage=f'{os.path.basename(__file__)} [options]'
    )
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        '-i', '--input', required=True, dest='input', metavar='<STR>', type=str, default='', help='Input file'
    )
    requiredNamed.add_argument(
        '-o', '--output', required=True, dest='output', metavar='<STR>', type=str, default='', help='Output file'
    )
    requiredNamed.add_argument(
        '-w',
        '--word-list',
        dest='swears',
        metavar='<STR>',
        type=str,
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'swears.txt'),
        help='Profanity list text file (default: swears.txt)',
    )
    requiredNamed.add_argument(
        '-e',
        '--encoding',
        dest='encoding',
        metavar='<STR>',
        type=str,
        default='utf-8',
        help='Text encoding (default: utf-8)',
    )
    try:
        parser.error = parser.exit
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit(2)

    # initialize the set of profanity
    swears = set(map(lambda x: x.lower(), [line.strip() for line in open(args.swears, 'r', encoding=args.encoding)]))

    # determine the type of the ebook
    bookMagic = magic.from_file(args.input, mime=True)

    eprint(f'Processing "{args.input}" of type "{"".join(bookMagic)}"')

    with tempfile.TemporaryDirectory() as tmpDirName:
        metadataFileSpec = os.path.join(tmpDirName, 'metadata.opf')

        # save off the metadata to be restored after conversion
        eprint("Extracting metadata...")
        metadataExitCode = subprocess.call(
            ["ebook-meta", args.input, "--to-opf=" + metadataFileSpec], stdout=devnull, stderr=devnull
        )
        if metadataExitCode != 0:
            raise subprocess.CalledProcessError(
                metadataExitCode, f"ebook-meta {args.input} --to-opf={metadataFileSpec}"
            )

        # convert the book from whatever format it is into epub for conversion
        if "epub" in bookMagic.lower():
            epubFileSpec = args.input
            wasEpub = True
            toEpubExitCode = 0
        else:
            wasEpub = False
            epubFileSpec = os.path.join(tmpDirName, 'ebook.epub')
            eprint("Converting to EPUB...")
            toEpubExitCode = subprocess.call(
                ["ebook-convert", args.input, epubFileSpec], stdout=devnull, stderr=devnull
            )
            if toEpubExitCode != 0:
                raise subprocess.CalledProcessError(toEpubExitCode, f"ebook-convert {args.input} {epubFileSpec}")

        # todo: somehow links/TOCs tend to get messed up

        eprint("Processing book contents...")
        book = epub.read_epub(epubFileSpec)
        newBook = epub.EpubBook()
        newBook.spine = ['nav']
        documentNumber = 0
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                documentNumber += 1
                cleanTokens = []
                for tokenNeedsCensoring, token in tagTokenizer(item.get_content().decode(args.encoding)):
                    if tokenNeedsCensoring and (token.lower() in swears):
                        # print(f"censoring:→{token}←")
                        cleanTokens.append("*" * len(token))
                    else:
                        # print(f"including:→{token}←")
                        cleanTokens.append(token)
                    # if (len(cleanTokens) % 100 == 0):
                    #   eprint(f"Processed {len(cleanTokens)} tokens from section {documentNumber}...")
                item.set_content(''.join(cleanTokens).encode(args.encoding))
                newBook.spine.append(item)
                newBook.add_item(item)
            else:
                newBook.add_item(item)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # write epub (either final or intermediate)
        eprint("Generating output...")
        if args.output.lower().endswith('.epub'):
            epub.write_epub(args.output, newBook)
        else:
            cleanEpubFileSpec = os.path.join(tmpDirName, 'ebook_cleaned.epub')
            epub.write_epub(cleanEpubFileSpec, newBook)
            eprint("Converting...")
            fromEpubExitCode = subprocess.call(
                ["ebook-convert", cleanEpubFileSpec, args.output], stdout=devnull, stderr=devnull
            )
            if fromEpubExitCode != 0:
                raise subprocess.CalledProcessError(toEpubExitCode, f"ebook-convert {cleanEpubFileSpec} {args.output}")

        # restore metadata
        eprint("Restoring metadata...")
        metadataExitCode = subprocess.call(
            ["ebook-meta", args.output, "--from-opf=" + metadataFileSpec], stdout=devnull, stderr=devnull
        )
        if metadataExitCode != 0:
            raise subprocess.CalledProcessError(
                metadataExitCode, f"ebook-meta {args.output} --from-opf={metadataFileSpec}"
            )


if __name__ == '__main__':
    RunMontag()
