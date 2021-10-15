'''
get_groups_list
    resolve_fname
        load
            load_file
                as_valid_path
            get_matched_categories
                close_matches
                    as_valid_path
getallcategories

'''
import os
import glob
import fnmatch
import functools
import random
import difflib


WORD_CLASSES = ['adjectives', 'nouns', 'verbs', 'names', 'ipsum']

# WORD_PATH = '../wordlists'
WORD_PATH = os.path.join(os.path.dirname(__file__), 'wordlists')

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
    'u': 'uuid',
    'uu': 'uuid',
}

import uuid
def uuid_(n=None):
    return str(uuid.uuid4())[:n and int(n)]
WORD_FUNCS = {
    'uuid': uuid_,
}


def get_groups_list(fnames):
    '''Get word lists from multiple word groups.'''
    return [x for f in as_multiple(fnames) for x in resolve_fname(f)]


def resolve_fname(fname):
    '''Detect if fname is a path or is a literal word. Replace any path
    shortcuts.'''
    return load(fname) if '/' in fname else [fname]


def load(name):
    '''Load a list of words from file. Can use glob matching to load
    multiple files.

    Examples:
    >>> load('n/music') == ['arrange', 'carol', 'compose', ... 'yodel']
    '''
    return [w for f in get_matched_categories(name) for w in load_file(f)]


@functools.lru_cache(128)
def load_file(name):
    '''Load a wordlist. Does not do any name conversion.'''
    parts = name.split('/')
    if parts[0] in WORD_FUNCS:
        return [functools.partial(WORD_FUNCS[parts[0]], *(p for p in parts[1:] if p != '*'))]

    with open(as_valid_path(name, required=True), 'r') as f:
        return [
            l for l in (l.strip() for l in f.readlines())
            if l and l[0] not in ';#']


@functools.lru_cache(128)
def get_matched_categories(name, *a, **kw):
    '''Resolve a fuzzy-matched category. Throw an error if it doesn't
    match anything.'''
    name = doalias(name)
    # glob matching
    if name.endswith('/'):
        name += '*'
    matches = [f for f in ALL_CATEGORIES if fnmatch.fnmatch(f, name)]
    if matches:
        return matches

    parts = name.split('/', 1)
    matches = ['/'.join((f, parts[1])) for f in WORD_FUNCS if fnmatch.fnmatch(f, parts[0])]
    if matches:
        return matches

    # no matches. throw nice error
    matches = close_matches(name, *a, **kw)
    raise ValueError("No matching wordlist '{}'. {}".format(
        name, 'Did you mean {}?'.format(_or_fmt(matches)) if matches else
        'No close matches found.'))


def close_matches(name, cutoff=0.65):
    '''Find close matching wordlist names.'''
    # they entered a underspecified category
    name = doalias(name)
    matches = [cat for cat in ALL_CATEGORIES if name == cat.split('/', 1)[1]]
    all_sub_categories = [c.split('/', 1)[-1] for c in ALL_CATEGORIES]

    if '/' in name:
        part0, part1 = name.split('/', 1)
        if not part0:
            part0 = '*'
        # they spelled the first part correctly
        if part0 in WORD_CLASSES:
            _ms = _get_matches(part1, AVAILABLE[part0], cutoff=cutoff)
            matches += [f for f in ('{}/{}'.format(part0, m) for m in _ms) if as_valid_path(f)]
        # they entered a misspelled category
        elif part1 in all_sub_categories:
            _ms = _get_matches(part0, [k for k in AVAILABLE if part1 in AVAILABLE[k]], cutoff=cutoff)
            matches += [f for f in ('{}/{}'.format(m, part1) for m in _ms) if as_valid_path(f)]
        # they entered a misspelled category and misspelled group
        else:
            matches += _get_matches(name, ALL_CATEGORIES, cutoff=cutoff)
        _ms = _get_matches(part0, list(WORD_FUNCS), cutoff=cutoff)
        matches += ['{}/{}'.format(m, part1) for m in _ms]
    else:
        # get sub matches
        _ms = _get_matches(name, all_sub_categories, cutoff=cutoff)
        matches += [
            '{}/{}'.format(pos, cat)
            for cat in _ms for pos in find_parts_of_speech(cat)]

    # remove duplicates
    return _ordered_unique(matches)


def _get_matches(pattern, available, **kw):
    return (
        difflib.get_close_matches(pattern, available, **kw) +
        [m for m in available if m.startswith(pattern) or fnmatch.fnmatch(m, pattern)]
    )


def _or_fmt(fnames):
    return ' or '.join("'{}'".format(f) for f in fnames)


def _ordered_unique(xs):
    unique = []
    for x in xs:
        if x not in unique:
            unique.append(x)
    return unique


def _groupby(items, func):
    groups = {}
    for x in items:
        k = func(x)
        if k not in groups:
            groups[k] = []
        groups[k].append(x)
    return x


'''

General utils

'''


def doalias(fname):
    '''Replace aliases in string.

    Examples:
    >>>
    '''
    parts = fname.split('/')
    for k, v in ALIASES.items():
        parts = [v if x == k else x for x in parts]
    return '/'.join(parts)


def as_valid_path(name, required=False):
    path = os.path.abspath(os.sep + name)
    path = os.path.relpath(path, os.path.abspath(os.sep))
    path = os.path.join(WORD_PATH, path + '.txt')
    if not os.path.isfile(path):
        if required:
            raise OSError(f"Wordlist '{name}' does not exist at location '{path}'.")
        return
    return path


def prefix(pre, xs):
    '''Prefix all items with a path prefix.'''
    return [f'{pre.rstrip("/")}/{x.lstrip("/")}' for x in as_multiple(xs)]


def choose(items, n=None):
    '''Choose one item from a list.'''
    items = as_multiple(items)
    x = random.choice(items) if n is None else random.choices(items, k=n)

    if isinstance(x, list):
        x = [xi() if callable(xi) else xi for xi in x]
    elif callable(x):
        x = x()
    return x

def sample_unique(func, n, *a, n_fails=50, unique=True, **kw):
    if not unique:
        return [func(*a, **kw) for _ in range(n)]
    words = set()
    for i in range(n):
        for j in range(n_fails):
            words.add(func(*a, **kw))
            if len(words) > i:
                break
        else:
            break
    return words


def as_multiple(x):
    '''Ensure a list or tuple.'''
    x = x if isinstance(x, (list, tuple)) else [x]
    return [si for s in x for si in ([s] if callable(s) else str(s).split(','))]



def find_parts_of_speech(name):
    '''Given a name, find all the groups that it belongs to.'''
    return {k for k, v in AVAILABLE.items() if name in v}


def getallcategories(d=''):
    '''Get all categories (subdirectories) from a word class (adjectives,
    nouns, etc.)'''
    d = os.path.join(WORD_PATH, d)
    path_to_all_categories = [
        os.path.relpath(os.path.splitext(f)[0], d)
        for f in glob.glob(os.path.join(d, '**/*.txt'), recursive=True)]

    # Replace OS-dependent separator with '/' which aligns with the input format
    # of the users.
    return [p.replace(os.sep, "/") for p in path_to_all_categories]


# get all available word classes and categories.
AVAILABLE = {k: getallcategories(k) for k in WORD_CLASSES}
ALL_CATEGORIES = getallcategories()  # FIXME: redundant
# ALL_SUB_CATEGORIES = [c.split('/', 1)[-1] for c in ALL_CATEGORIES]

# expand
ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM = [
    AVAILABLE[k] for k in WORD_CLASSES]



if __name__ == '__main__':
    import fire
    fire.Fire()
