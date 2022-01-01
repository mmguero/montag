# Montag

[![Latest Version](https://img.shields.io/pypi/v/montag-cleaner)](https://pypi.python.org/pypi/montag-cleaner/) [![Docker Image](https://github.com/mmguero/montag/workflows/montag-build-push-ghcr/badge.svg)](https://github.com/mmguero/montag/pkgs/container/montag) [![Docker Image (arm32v7)](https://github.com/mmguero/montag/workflows/montag-build-push-arm32v7-ghcr/badge.svg)](https://github.com/mmguero/montag/pkgs/container/montag)

*"Didn't firemen prevent fires rather than stoke them up and get them going?"*

**montag** is a utility which reads an e-book file (in any format supported by [Calibre's ebook-convert](https://manual.calibre-ebook.com/generated/en/ebook-convert.html)) and scrubs it of profanity (or words from any other list you can provide).

There are all sorts of arguments to be had about obscenity filters, censorship, etc. That's okay! I'm not really interested in having those arguments. My 13 year-old daughter asked me if I could take some swear words out of a young adult novel she was reading so I wrote this for her. If it's useful to you, great. If not, carry on my wayward son.

**montag** is part of a family of projects with similar goals:

* 📼 [cleanvid](https://github.com/mmguero/cleanvid) for video files
* 🎤 [monkeyplug](https://github.com/mmguero/monkeyplug) for audio files
* 📕 [montag](https://github.com/mmguero/montag) for ebooks

## Installation

Using `pip`, to install the latest [release from PyPI](https://pypi.org/project/montag-cleaner/):

```
python3 -m pip install -U montag-cleaner
```

Or to install directly from GitHub:


```
python3 -m pip install -U 'git+https://github.com/mmguero/montag'
```

## Prerequisites

### Python Prerequisites

[Montag](montag.py) requires Python 3 and the [EbookLib](https://github.com/aerkalov/ebooklib) and [python-magic](https://github.com/ahupp/python-magic) libraries. It also uses some utilities from the [Calibre](https://calibre-ebook.com/) project.

On a Debian-based Linux distribution, these requirements could be installed with:
```
$ sudo apt-get install libmagic1 imagemagick calibre-bin python3 python3-magic python3-ebooklib
```

On Windows, you'll need DLLs for `libmagic`. One option for installing these libraries is [`python-magic-bin`](https://pypi.org/project/python-magic-bin/):

```
python3 -m pip install python-magic-bin
```

The Python dependencies *should* be installed automatically if you are using `pip` to install montag.

### Docker

Alternately, a [Dockerfile](./docker/Dockerfile) is provided to allow you to run Montag in Docker. You can build the `ghcr.io/mmguero/montag:latest` Docker image with [`build_docker.sh`](./docker/build_docker.sh), then use [`montag-docker.sh`](./docker/montag-docker.sh) to process your e-book files.

## Usage

Montag is easy to use. Specify the input and output e-book filenames, and, optionally, the file containing the words to be censored (one per line) and the text encoding.
```
$ ./montag.py 
usage: montag.py [options]

e-book profanity scrubber

required arguments:
  -i <STR>, --input <STR>
                        Input file
  -o <STR>, --output <STR>
                        Output file
  -w <STR>, --word-list <STR>
                        Profanity list text file (default: swears.txt)
  -e <STR>, --encoding <STR>
                        Text encoding (default: utf-8)
```

So, using Andy Weir's "The Martian" as an example:
```
$ ./montag.py -i "The Martian - Andy Weir.mobi" -o "The Martian - Andy Weir (scrubbed).mobi"
Processing "The Martian - Andy Weir.mobi" of type "Mobipocket E-book "The Martian", 775003 bytes uncompressed, version 6, codepage 65001"
Extracting metadata...
Converting to EPUB...
Processing book contents...
Generating output...
Converting...
Restoring metadata...
```

Upon opening the book, you will find the text reads something like this:
> CHAPTER 1
> 
> LOG ENTRY: SOL 6
> 
> I’m pretty much ******.
> 
> That’s my considered opinion.
> 
> ******.
> 
> Six days into what should be the greatest two months of my life, and it’s turned into a nightmare.
> 
> ...

Alternately, if you are using the Docker method described above, use [`montag-docker.sh`](./docker/montag-docker.sh) rather than [`montag.py`](./src/montag_cleaner/montag.py) directly.

## Known Limitations

Montag is not smart enough to do any in-depth language analysis or deep filtering. For a while I was trying to use the [rominf/profanity-filter](https://github.com/rominf/profanity-filter) library for the word detection and filtering, but I ran into issues and ended up just going with a simpler method that works but presents a few limitations:

* Only whole words are matched and censored. In other words, if the word `frick` is in your list of profanity, `Frick you!` will be censored, but `Absofrickenlutely` will not. As such if you wish to catch all of the variations of the word `frick`, you'd have to list them individually in your `swears.txt` word list.
* Having phrases (eg., multiple space-separated words) in your `swears.txt` word list won't do you any good.
* Montag can't tell the difference between different meanings of the same word. For example, if the word `ass` is in your list, both "And he said unto his sons, Saddle me the ass. So they saddled him the ass: and he rode thereon" (from the KJV of *The Bible*) and "Then the high king carefully turned the golden screw. Once: Nothing. Twice: Nothing. Then he turned it the third time, and the boy’s ass fell off" (from Patrick Rothfuss' *The Wise Man's Fear*) will be censored.

## Contributing

If you'd like to help improve Montag, pull requests will be welcomed!

## Authors

* **Seth Grover** - *Initial work* - [mmguero](https://github.com/mmguero)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to:
* [Calibre](https://calibre-ebook.com/about) developer Kovid Goyal and contributors
* the contributors to [EbookLib](https://github.com/aerkalov/ebooklib/blob/master/AUTHORS.txt)
* [python-magic](https://github.com/ahupp/python-magic) developer Adam Hupp and contributors
