class CharCounter {
    constructor() {
        this.counters = new Map();
    }

    countChar(c) {
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
        var retval = new CharCounter();
        this.counters.forEach(function(value,key){
            var newval = value - other.get(key);
            if ( newval < 0 ) {
                alert("Tried to remove more than was there in CharCounter");
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
    constructor(dict) {
        this.dictionary = new Map();
        this.readDictionary(dict);
    }

    readDictionary(dict) {
        for ( let word of dict ) {
            this.dictionary.set(word, this.parseWord(word.toLowerCase()));
        } 
    }

    parseWord(word) {
        let cntr = new CharCounter();
        let new_word = word.toLowerCase();
        for (let index = 0; index < new_word.length; index++ ) {
            var c = new_word[index];
            if ( c != ' '  && c >= 'a' && c <= 'z') {
                cntr.countChar(new_word[index]);
            }
        }
        return cntr;
    }

    makeAnagrams(words) {
        let target = this.parseWord(words.join(""));
        let pool = findSubsets(target, this.dictionary.keys(), this.dictionary);
        pool.sort(function(a,b){return a.length-b.length || a>b})

        return findCompleteSubsets(target, pool, this.dictionary);
    }
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

function* findCompleteSubsets(target, pool, dictionary, depth=0) {
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
