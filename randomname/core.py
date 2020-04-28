from . import util

WORD_CLASSES = ['adjectives', 'nouns', 'verbs', 'names', 'ipsum']

# get all available word classes and categories.
available = {k: util.getallcategories(k) for k in WORD_CLASSES}

# expand
ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM = [
    available[k] for k in WORD_CLASSES]



def generate(*groups, sep='-'):
    '''Generate words from a sequence of word class/categories.'''
    return sep.join(
        util.choose(util.get_groups_list(x)).replace(' ', sep)
        for x in groups)

def get_name(adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    return generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep)

def sample(*groups, n=10):
    l = util.get_groups_list(groups)
    util.random.shuffle(l)
    return l[:n]
