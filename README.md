# karma_manager

Karma Manager is an anagram maker, as well as an angram in its own right.  This is based on hazy memories of the algorithm used by
an identically named and functional program for the Mac in the late 80's and early 90's.  The original program is still available on
the [Internet Archive](https://archive.org/details/MacintoshSharewareGamesK) if you've got an emulator (or better yet, a Mac IIci
running MacOS 7.5!)

This implementation is written in python (3, who uses 2 any more?) and is strictly a command line interface or library.  It doesn't come
with a dictionary of words to use (for licensing reasons.)  I've provided a script called `make_dict.sh` to fetch one from the internet,
though how long it hangs around is anybody's guess.  You can also provide your own, with one word per line.  It should be noted that
this implementation is very rooted in the Ascii character set, and therefore standard english/latin characters.  Attempts to use this
with unicode text will likely produce strange results.

## Usage
The command line options are:
```
$ ./karma_manager.py --help
usage: karma_manager [-h] [--dictionary DICTIONARY] [--debug] words [words ...]

anagram maker

positional arguments:
  words                 words to create anagrams from

optional arguments:
  -h, --help            show this help message and exit
  --dictionary DICTIONARY
                        dictionary to use
  --debug               enable debugging output on stderr
```

And the output looks something like:
```
$ ./karma_manager.py --dictionary testdict Mitch Patenaude
Pneumatic hated
Pneumatic death
INFO:root:2 total anagrams found
```
