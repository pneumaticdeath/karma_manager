#!/usr/bin/env python3
# vim:sw=4,ai,expandtab

import logging


class NoCompleteSubsets(Exception):
    pass


class CharCounter(object):
    def __init__(self):
        self._map = {}

    def count(self,c):
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
        with open(dictionary_file, 'r') as f:
            self.dictionary = self.readDictionary(f)

    def readDictionary(self, f):
        dictionary = {}
        for word in f.readlines():
            word = self.smash(word)
            if word not in dictionary:
                dictionary[word] = self.parseWord(word)
            else:
                logging.warning('Word {} appears more than once in the dictionary'.format(word))
        return dictionary

    def parseWord(self, word):
        retval = CharCounter()
        for c in word:
            retval.count(c)
        return retval

    def smash(self, word):
        return word.lower().translate(word.maketrans('','',' \t\n\r'))

    def makeAnagrams(self, words):
        word = ''
        for w in words:
            word += self.smash(w)
        source = self.parseWord(word)
        logging.debug('Starting with source set {}'.format(str(source)))

        working_pool = self._findSubsets(source, self.dictionary.keys())
        working_pool.sort(key=lambda x: (len(x), x))
        logging.debug('Starting with {} words total'.format(len(working_pool)))

        try:
            solution = self._findCompleteSubsets(source, working_pool)
            return solution
        except NoCompleteSubsets:
            return None


    def _findSubsets(self, target, words):
        subsets = []
        for word in words:
            if self.dictionary[word] <= target:
                subsets.append(word)
        return subsets

    def _findCompleteSubsets(self, source, pool):

        if source and not pool:
            raise NoCompleteSubsets

        word = pool.pop()
        while len(pool) > 0:
            logging.debug('Starting to find subsets with word {} with pool of {}'.format(word,len(pool)))
            remainder = source.remove(self.dictionary[word])
            logging.debug('Remainder is {}'.format(str(remainder)))
            if remainder is None:
                yield [word,]
            else:
                try:
                    for subset in self._findCompleteSubsets(remainder, self._findSubsets(remainder, pool.copy())):
                        yield [word,] + subset
                except NoCompleteSubsets:
                    pass
            word = pool.pop()
        remainder = source.remove(self.dictionary[word])
        if remainder is None:
            yield [word,]


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
    if anagrams is not None:
        for anagram in anagrams:
            print(' '.join(anagram).capitalize())
        sys.exit(0)
    else:
        print('Unable to find anything')
        sys.exit(1)

if __name__ == '__main__':
    main()

