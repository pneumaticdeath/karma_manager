#!/usr/bin/env python3
# vim:sw=4,ai,expandtab

import logging


class CharCounter(object):
    def __init__(self):
        self._map = {}

    def count(self, c):
        if c in self._map:
            self._map[c] += 1
        else:
            self._map[c] = 1

    def remove(self, other):
        retval = CharCounter()
        remaining = 0
        for c, cnt in self._map.items():
            if c in other._map:
                newtot = cnt - other._map[c]
                if newtot < 0:
                    raise ValueError('Other CharCounter not subset',)
                elif newtot > 0:
                    retval._map[c] = newtot
                remaining += newtot
            else:
                retval._map[c] = cnt
                remaining += cnt
        if remaining > 0:
            return retval
        else:
            return None

    def __le__(self, other):
        for c in self._map.keys():
            if self._map[c] > 0:
                if not (c in other._map and self._map[c] <= other._map[c]):
                    return False
        return True

    def __str__(self):
        s = ''
        chars = list(self._map.keys())
        chars.sort()
        for c in chars:
            if self._map[c] > 0:
                s += c * self._map[c]
        return s
        

class KarmaManager(object):
    def __init__(self, dictionary_file):
        self.dictionary = {}
        with open(dictionary_file, 'r') as f:
            self.readDictionary(f)

    def readDictionary(self, f):
        for word in f.readlines():
            self.addDictionaryWord(word)

    def addDictionaryWord(self, word):
        word = self.smash(word)
        if word not in self.dictionary:
            self.dictionary[word] = self.parseWord(word)
        else:
            logging.warning('Attempted to add duplicate word {} to the dictionary'.format(word))

    def parseWord(self, word):
        retval = CharCounter()
        for c in word:
            if c.isalpha():
                retval.count(c.lower())
        return retval

    def smash(self, word):
        return word.lower().translate(word.maketrans('','','\t\n\r'))

    def makeAnagrams(self, words):
        word = ' '.join(words)
        source = self.parseWord(word)
        logging.debug('Starting with phrase "{}" and source set {}'.format(word, str(source)))

        # This will find only those dictionary words that are a subset of the characters in the
        # input phrase/word.  If the input doesn't have a 'z', then there's no point in including
        # words with 'z' in them.
        working_pool = self._findSubsets(source, self.dictionary.keys())

        # This is a hackish optimization.  It's sorts the words first by length then alphabetically
        # if the same length.  Since _fineCompleteSubsets works backwards through the pool it will
        # start with the longest words first, and work its way backward through the alphabet
        # This will mean that it will find matches with longer words first, which is means quicker
        # results for first match, and that the words it finds will be more interesting.  There
        # is probbably a better optimization out there.
        working_pool.sort(key=lambda x: (len(x), x))

        logging.debug('Starting with {} words total'.format(len(working_pool)))

        return self._findCompleteSubsets(source, working_pool)

    def _findSubsets(self, target, words):
        subsets = []
        for word in words:
            if self.dictionary[word] <= target:
                subsets.append(word)
        return subsets

    def _findCompleteSubsets(self, source, pool, depth=0):

        if not pool:
            return

        while len(pool) > 0:
            word = pool[-1]
            remainder = source.remove(self.dictionary[word])
            logging.debug('{}Find subsets with word {} with pool of {} and remainder {}'.format(' ' * depth, word, len(pool), str(remainder)))
            if remainder is None:
                yield [word,]
            else:
                for subset in self._findCompleteSubsets(remainder, self._findSubsets(remainder, pool), depth+1):
                    yield [word,] + subset
            pool.pop()


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser('karma_manager', description='anagram maker')
    parser.add_argument('--dictionary', default='dict.txt', help='dictionary to use')
    parser.add_argument('--debug', action='store_true', help='enable debugging output on stderr')
    parser.add_argument('words', type=str, nargs='+', help='words to create anagrams from')

    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)

    km = KarmaManager(args.dictionary)

    anagrams = km.makeAnagrams(args.words)
    counter = 0
    for anagram in anagrams:
        print(' '.join(anagram).capitalize())
        counter += 1;
    logging.info("{} total anagrams found".format(counter))
    if counter > 0:
        sys.exit(0)
    else:
        print('Unable to find anything')
        sys.exit(1)

if __name__ == '__main__':
    main()
