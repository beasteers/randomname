from . import util
from .util import (
    ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM, ALL_CATEGORIES, AVAILABLE)

def generate(*groups, sep='-'):
    '''Generate words from a sequence of word class/categories.'''
    return sep.join(
        util.choose(util.get_groups_list(x)).replace(' ', sep)
        for x in groups or ('adj/', 'n/'))

def get_name(adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    return generate(util.prefix('a', adj), util.prefix('n', noun), sep=sep)


def sample(*groups, n=10, sep='-'):
    '''Get a random adjective-noun using the categories in `adj` and `noun`.'''
    return util.sample_unique(generate if groups else get_name, n, *groups, sep=sep)


def sample_words(*groups, n=10):
    '''Get a random sample of a category.'''
    return util.random.sample(util.get_groups_list(groups), n)


def sample_names(n=10, adj=ADJECTIVES, noun=NOUNS, sep='-'):
    '''Sample random adjective-nouns using the categories in `adj` and `noun`.'''
    return util.sample_unique(get_name, n, adj, noun, sep=sep)


def available(k=None):
    '''Show available categories for a word class.'''
    return AVAILABLE[util.doalias(k)] if k else AVAILABLE


import os
import json
class SavedList:
    ROOT_DIR = os.path.expanduser('~/.randomname')
    def __init__(self, name='default', groups=None, n=100, overwrite=False):
        super().__init__()
        self.name = name
        self.file = os.path.join(self.ROOT_DIR, name)
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        self.groups = util.as_multiple(groups or [])
        self.words = []
        if overwrite:
            self.remove()
        self.read()
        self.atlen(n)

    def __str__(self):
        return '({} ::: {})'.format(self.name, ' | '.join(self.words) or '--')

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return iter(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def get(self, index):
        return self[index]

    @property
    def exists(self):
        return os.path.isfile(self.file)

    def read(self):
        if self.exists:
            with open(self.file, 'r') as f:
                self.__dict__.update(json.load(f))
            return True
        return False

    def save(self):
        with open(self.file, 'w') as f:
            json.dump({'words': self.words, 'groups': self.groups}, f)
        return self

    def dump(self, index=True):
        return '\n'.join(
            ('\t'.join(map(str, w)) for w in enumerate(self.words))
            if index else self.words)

    def clear(self):
        self.words.clear()
        self.save()
        return self

    def remove(self):
        self.words.clear()
        if self.exists:
            os.remove(self.file)
        return self

    def sample(self, n=100, **kw):
        self.words.clear()
        return self.more(n, **kw)

    def more(self, n=100, **kw):
        self.words.extend(sample(*self.groups, n=n, **kw))
        self.save()
        return self

    def atlen(self, n=100, **kw):
        if n is not None:
            self.more(max(0, n - len(self)), **kw)
            self.words = self.words[:n]
