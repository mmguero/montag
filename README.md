# Montag

*"Didn't firemen prevent fires rather than stoke them up and get them going?"*

Montag is a utility which reads e-book files (in any formats supported by [Calibre's ebook-convert](https://manual.calibre-ebook.com/generated/en/ebook-convert.html)) and scrubs them of profanity (or words from any other list you can provide).

There are all sorts of arguments to be had about obscenity filters, censorship, etc. That's okay! I'm not really interested in having those arguments. My 13 year-old daughter asked me if I could take some swear words out of a book she was reading so I wrote this for her. If it's useful to you, great. If not, carry on my wayward son.

## Prerequisites

### Python Prerequisites

[Montag](montag.py) requires Python 3 and the [EbookLib](https://github.com/aerkalov/ebooklib) and [filemagic](https://github.com/aliles/filemagic) libraries. It also uses some utilities from the [Calibre](https://calibre-ebook.com/) project.

On a Debian-based Linux distribution, these requirements could be installed with:
```
$ sudo apt-get install libmagic1 imagemagick calibre python3 python3-pip
```

After which the Python libraries could be installed:
```
$ pip3 install -U filemagic ebooklib
```

### Docker

Alternately, a [Dockerfile](Dockerfile) is provided to allow you to run Montag in Docker. You can build the `montag:latest` Docker image with [`build_docker.sh`](build_docker.sh), then use [`montag_docker.sh`](montag_docker.sh) to process your e-book files.

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

Alternately, if you are using the Docker method described above, use [`montag_docker.sh`](montag_docker.sh) rather than [`montag.py`](montag.py) directly.

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

This project is licensed under the Apache License, v2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to:
* [Calibre](https://calibre-ebook.com/about) developer Kovid Goyal and contributors
* the contributors to [EbookLib](https://github.com/aerkalov/ebooklib/blob/master/AUTHORS.txt)
* [filemagic](https://github.com/aliles/filemagic) developer Aaron Iles and contributors

## Disclaimers

By using Montag you understand and agree that its author(s) are in no way responsible for your actions. If Montag borks your system, or if you download a "pirated" e-book and SWAT team of the copyright office of your respective nation busts down your door with a flash-bang grenade, or if Montag censors too much or too little and your feelings get hurt, or whatever, well, that's on you, dog.
