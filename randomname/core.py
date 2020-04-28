from . import util

WORD_CLASSES = ['adjectives', 'nouns', 'verbs', 'names', 'ipsum']

# get all available word classes and categories.
_available = {k: util.getallcategories(k) for k in WORD_CLASSES}

# expand
ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM = [
    _available[k] for k in WORD_CLASSES]


def generate(*groups, sep='-'):
    '''Generate words from a sequence of word class/categories.'''
    return sep.join(
        util.choose(util.get_groups_list(x)).replace(' ', sep)
        for x in groups)

def get_name(adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    return generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep)

def sample(*groups, n=10):
    '''Get a random sample of a category.'''
    l = util.get_groups_list(groups)
    util.random.shuffle(l)
    return l[:n]

def available(k=None):
    '''Show available categories for a word class.'''
    return _available[util.doalias(k)] if k else _available
