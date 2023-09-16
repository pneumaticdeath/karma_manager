class StringCounter {
    constructor() {
        this.counters = new Map();
    }

    countString(c) {
        if ( this.counters.has(c) ) {
            this.counters.set(c, this.counters.get(c) + 1);
        } else {
            this.counters.set(c, 1);
        }
    }

    get(c) {
        if ( this.counters.has(c) ) {
            return this.counters.get(c);
        } else {
            return 0;
        }
    }

    remove(other) {
        var retval = new StringCounter();
        this.counters.forEach(function(value,key){
            var newval = value - other.get(key);
            if ( newval < 0 ) {
                console.log("Tried to remove more than was there in StringCounter");
            } else if ( newval > 0 ) {
                retval.counters.set(key, newval);
            }
        });
        return retval;
    }

    empty() {
        for ( let c of this.counters.keys() ) {
            if ( this.counters.get(c) > 0 ) {
                return false;
            }
        }
        return true;
    }

    subsetOf(other) {
        for ( let key of this.counters.keys() ) {
            if ( other.get(key) < this.get(key) ) {
                return false;
            }
        }
        return true;
    }
}

class KarmaManager {
    constructor() {
        this.dictionary = new Map();
        this.exclusionSet = new Set();
        this.seedSet = [];
        this.pool = [];
    }

    readDictionary(dict) {
        for ( let word of dict ) {
            this.dictionary.set(word, parseWord(word.toLowerCase()));
        } 
    }

    setExclusionSet(ex_set) {
        for ( let word of ex_set ) {
            this.exclusionSet.add(word);
        }
    }
    
    setSeedSet(seed_phrase) {
        this.seedSet.push(seed_phrase);
    }

    clearSeedSet() {
        this.seedSet = [];
    }

    clearExclusionSet() {
        this.exclusionSet.clear();
    }

    processExclusionSet() {
        this.pool = this.pool.filter((word) => { return !this.exclusionSet.has(word) });
    }

    parseTarget(words) {
        this.target = parseWord(words.join(""));
        return this.target;
    }

    findWordPool() {
        this.pool = findSubsets(this.target, this.dictionary.keys(), this.dictionary);
        this.pool.sort(function(a,b){return a.length-b.length || (a>=b?1:-1)})

        return this.pool;
    }

    makeAnagrams(words) {
        this.parseTarget(words);

        this.findWordPool();

        this.processExclusionSet();

        return findCompleteSubsets(this.target, [...this.pool], this.dictionary, this.seedSet);
    }
}

function parseWord(word) {
    let cntr = new StringCounter();
    let new_word = word.toLowerCase();
    for (let index = 0; index < new_word.length; index++ ) {
        var c = new_word[index];
        if ( c >= 'a' && c <= 'z') {
            cntr.countString(c);
        }
    }
    return cntr;
}

let findSubsets = function(target, pool, dictionary) {
    let retval = [];
    for ( let word of pool ) {
        if ( dictionary.get(word).subsetOf(target) ) {
            retval.push(word);
        }
    }
    return retval;
};

function* findCompleteSubsets(target, pool, dictionary, seedset=[], depth=0) {
    if ( seedset.length > 0) {
        for ( let seed of seedset ) {
            newtarget = target.remove(parseWord(seed.join("")));
            if ( newtarget.empty() ) {
                yield seed;
            } else {
                newpool = findSubsets(newtarget, pool, dictionary);
                for ( let subset of findCompleteSubsets(newtarget, newpool, dictionary, [], depth+1) ) {
                    yield seed.concat(subset);
                }
            }
        }
    } else {
        while ( pool.length > 0 ) {
            let word = pool[pool.length - 1];
            // console.log(depth);
            // console.log(word);
            let remainder = target.remove(dictionary.get(word));
            // console.log(remainder.counters);
            if ( remainder.empty() ) {
                yield [word];
            } else {
                for ( let subset of findCompleteSubsets(remainder, findSubsets(remainder, pool, dictionary), dictionary, depth+1) ) {
                    yield [word].concat(subset);
                }
            }
            pool.pop()
        }
    }
}
