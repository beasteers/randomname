import os
import functools
from .lists import *
from . import util


DEFAULT_WORDLIST = os.getenv("RANDOMNAME_WORDLIST") or 'imsky'
GLOBAL_BLACKLIST = os.getenv("RANDOMNAME_GLOBAL_WORDLIST") or '~/.randomname/blacklist'
LOCAL_BLACKLIST = os.getenv("RANDOMNAME_LOCAL_WORDLIST") or '.randomname.blacklist'


WORDLISTS = {}
def get_wordlist(name, **kw):
    '''Gets a wordlist by name. This lets you use word lists like a singleton.
    '''
    if name is None:
        return wordlists
    if isinstance(name, WordList):
        return name
    if name in WORDLISTS:
        return WORDLISTS[name]
    WORDLISTS[name] = wl = WordList.as_wordlist(name, **kw)
    wl -= get_blacklist()
    return wl

def set_wordlist(name):
    '''Sets the word list as default.
    
    .. code-block:: python

        import randomname
        randomname.set_wordlist('wordnet')
    '''
    global wordlists
    if name is not None:
        wordlists = get_wordlist(name)
    return wordlists

def get_blacklist(*blacklists):
    '''Get the blacklist wordlist. This can be subtracted from another wordlist.'''
    return WordLists([
        WordListFile(f)
        for f in (GLOBAL_BLACKLIST, LOCAL_BLACKLIST) + blacklists
        if os.path.isfile(f)
    ], 'blacklist')


# define the wordlist
wordlists = get_wordlist(DEFAULT_WORDLIST)


# import uuid as _uuid
# def uuid(n=None):
#     return str(_uuid.uuid4())[:n and int(n)]
# wordlists.add(uuid)

# Sampling functions
#######################

# sample a single word/phrase


def generate(*groups, sep='-', spaces=None, **kw):
    '''Generate words from a sequence of word class/categories.
    
    .. code-block:: python

        phrase = randomname.generate()  # default is equivalent to `randomname.get()`

        # the difference is you can specify your own part of speech structure.
        phrase = randomname.generate('v/music', 'a/colors', 'n/cats')
        # yodel-sienna-bobtail

        # and you can even mix and match word literals.
        phrase = randomname.generate('underwater,land-bound', 'n/cats', 'cat', 'loves', 'a/', 'n/')

    '''
    return util.join_words((
        sample_word(x, **kw) for x in groups or ('adj/', 'n/')
    ), sep=sep, spaces=spaces).lower()

def get(adj='*', noun='*', sep='-', **kw):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.
    
    .. code-block:: python

        # sample from all adjectives/nouns
        phrase = randomname.get()

        # sample from specific adjectives/nouns
        phrase = randomname.get('colors', 'cats')
    '''
    return generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep, **kw)

def sample_word(*groups, n=None, list=None):
    '''Get a random word from a subset of the categories.
    
    .. code-block:: python

        # sample a word from either n/chemistry or n/cheese
        word = randomname.sample_word('n/chemistry', 'n/cheese')
        assert isinstance(word, str)
        words = randomname.sample_word('n/chemistry', 'n/cheese', n=5)
        assert len(words) == 5
    '''
    # l = wordlists.filter_lists(*groups, accept_literals=True)
    # print(l, len(l), l[0])
    # print(len(l.lists[1]), list(l.lists[1]))
    return get_wordlist(list).filter_lists(*groups, accept_literals=True).sample(n)


get_name = get


# sample multiple words/phrases


def sample(*groups, n=10, sep='-', **kw):
    '''Get a random phrase using categories you provide.
    
    .. code-block:: python

        randomname.sample('a/colors', 'n/cats', 'v/music')
        # champagne-siamese-compose
        # green-javanese-listen
        # tan-longhair-carol
        # corn-longhair-vocalize
        # rust-himalayan-vocalize
        # plum-marmalade-tune
        # bordeaux-javanese-improvise
        # denim-burmese-fiddle
        # ash-javanese-compose
        # cream-marmalade-yodel
    '''
    return util.sample_unique(generate, n, *groups, sep=sep, **kw)

def sample_names(n=10, adj='*', noun='*', sep='-'):
    '''Sample random adjective-nouns using the categories in `adj` and `noun`.
    
    .. code-block:: python

        randomname.sample_names(10, 'colors', 'cats')
        # champagne-siamese-compose
        # green-javanese-listen
        # tan-longhair-carol
        # corn-longhair-vocalize
        # rust-himalayan-vocalize
        # plum-marmalade-tune
        # bordeaux-javanese-improvise
        # denim-burmese-fiddle
        # ash-javanese-compose
        # cream-marmalade-yodel
    '''
    return util.sample_unique(get, n, adj, noun, sep=sep)


# Helpers

def available(*ks, list=None):
    '''Show available categories for a word class.'''
    return get_wordlist(list).filter_lists(*ks)


def search(term, filter=None, list=None):
    '''Search the wordlist for a word / pattern.

    .. code-block:: python

        # search for a word
        matched = randomname.search("someth*")
        assert 'something' in matched

        matched = randomname.search("*ark")
        assert 'park' in matched
        assert all(w.endswith('ark') for w in matched)
    '''
    return get_wordlist(list).filter_lists(filter or '*').search(term)


# CLI
##########


def main():
    import fire
    fire.Fire({
        'get': _prints(get_name), 'generate': _prints(generate),
        'available': available, 'sample': _prints(sample), 'util': util,
        'sample_word': sample_word, 'sample_names': sample_names,
        'sample_words': lambda *a, n=10, **kw: sample_word(*a, n=n, **kw),
        'search': _prints(search),
    })


def _prints(func):
    # need to wrap funcs so they go to stdout - idk whats going on
    @functools.wraps(func)
    def inner(*a, **kw):
        x = func(*a, **kw)
        if isinstance(x, (list, tuple, set)):
            for i in x:
                print(i)
        elif isinstance(x, dict):
            for k, v in x.items():
                print('{}: {}'.format(k, v))
        else:
            print(x)
    return inner


'''

StackOverflow: https://stackoverflow.com/questions/2288953/separate-word-lists-for-nouns-verbs-adjectives-etc

Wordnet Dictionary: https://wordnet.princeton.edu/download/current-version

egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adj | cut -d ' ' -f 5 > conv.data.adj
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adv | cut -d ' ' -f 5 > conv.data.adv
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.noun | cut -d ' ' -f 5 > conv.data.noun
egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.verb | cut -d ' ' -f 5 > conv.data.verb

'''