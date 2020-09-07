from . import util
from .util import (
    ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM, ALL_CATEGORIES, AVAILABLE)

def generate(*groups, sep='-'):
    '''Generate words from a sequence of word class/categories.'''
    return sep.join(
        util.choose(util.get_groups_list(x)).replace(' ', sep)
        for x in groups)

def get_name(adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    return generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep)


def sample(*groups, n=10, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    if not groups:
        return [get_name(sep=sep) for _ in range(n)]
    return [generate(*groups, sep=sep) for _ in range(n)]


def sample_words(*groups, n=10):
    '''Get a random sample of a category.'''
    l = util.get_groups_list(groups)
    util.random.shuffle(l)
    return l[:n]


def sample_names(n=10, adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Sample random adjective-nouns using the categories in `adj` and `noun`.'''
    return [
        generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep)
        for _ in range(n)
    ]


def available(k=None):
    '''Show available categories for a word class.'''
    return ALL_CATEGORIES[util.doalias(k)] if k else AVAILABLE
