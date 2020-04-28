import os
import glob
import random

# WORD_PATH = '../wordlists'
WORD_PATH = '/Github/wordlists'

ALIASES = {
    'a': 'adjectives',
    'n': 'nouns',
    'v': 'verbs',
    'nm': 'names',
    'ip': 'ipsum',
    # longer, clearer abbreviations
    'adj': 'adjectives',
    'nn': 'nouns',
    'vb': 'verbs',
}

def choose(l):
    '''Choose one item from a list.'''
    return random.choice(as_multiple(l))

def as_multiple(x):
    '''Ensure a list or tuple.'''
    x = x if isinstance(x, (list, tuple)) else [x]
    return [si for s in (str(s) for s in x) for si in s.split(',')]

def prefix(pre, xs):
    '''Prefix all items with a path prefix.'''
    return [os.path.join(pre, x) for x in as_multiple(xs)]

def load(fname):
    '''Load words from file.'''
    path = os.path.join(WORD_PATH, os.path.abspath('/' + fname).lstrip('/') + '.txt')
    with open(path, 'r') as f:
        return [
            l for l in (l.strip() for l in f.readlines())
            if l and l[0] not in ';#']

def resolve_fname(fname):
    '''Detect if fname is a path or is a literal word. Replace any path shortcuts.'''
    if '/' in fname:
        for k, v in ALIASES.items():
            fname = fname.replace(k + '/', v + '/')
        return load(fname)
    return [fname]

def get_groups_list(fnames):
    '''Get word lists from multiple word groups.'''
    return [x for f in as_multiple(fnames) for x in resolve_fname(f)]


def getallcategories(d):
    '''Get all categories (subdirectories) from a word class (adjectives, nouns, etc.)'''
    return [
        os.path.relpath(os.path.splitext(f)[0], os.path.join(WORD_PATH, d))
        for f in glob.glob(os.path.join(WORD_PATH, d, '**/*.txt'), recursive=True)]
