'''
'''
import os
import glob
from randomname import rng


class Aliases(dict):
    '''Manage string aliases'''
    def __init__(self, aliases=None):
        super().__init__(aliases or {})

    def __call__(self, name, char='/'):
        '''Replace aliases in string.'''
        parts = name.split(char)
        for k, v in self.items():
            parts = [v if x == k else x for x in parts]
        return char.join(parts)

    def update(self, aliases, force=False):
        if not force:
            existing = [a for a in aliases if a in self]
            if existing:
                raise ValueError("Could not set aliases {} as they already are used.".format(existing))
        super().update(aliases)
        return self

    @classmethod
    def as_alias(cls, aliases):
        if isinstance(aliases, Aliases):
            return aliases
        return Aliases(aliases)



def join_path(*xs, char='/'):
    '''like os.path.join, but doesn't change if you're on windows.'''
    return char.join(x.strip(char) for x in xs if x)


def join_words(it, sep='-', spaces=None):
    return sep.join(str(p) for p in it if p).replace(' ', sep if not spaces and spaces != '' else spaces)


def prefix(pre, xs):
    '''Prefix all items with a path prefix.'''
    return [join_path(pre, x.lstrip('/')) for x in as_multiple(xs)]

def remove_prefix(x, prefix=None):
    '''Remove a prefix from a string if it exists.'''
    return x[len(prefix):] if prefix and x.startswith(prefix) else x


def choose(items, n=None):
    '''Choose one item from a list.'''
    items = as_multiple(items)
    return rng.choice(items) if n is None else rng.choices(items, k=n)


def sample_unique(func, n, *a, n_fails=50, unique=True, **kw):
    if n is None:
        return func(*a, **kw)
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



def recursive_files(d='', ext='.txt'):
    '''Get all categories (subdirectories) from a word class (adjectives,
    nouns, etc.)'''
    ext = as_list(ext)
    return {
        os.path.relpath(os.path.splitext(f)[0], d): f
        for f in glob.iglob(os.path.join(d, '**/*'), recursive=True)
        if any(os.path.splitext(f)[-1] == e for e in ext)}



import importlib.resources


def recursive_package_files(module, path, ext='.txt'):
    ext = as_list(ext)
    paths = {}
    p = importlib.resources.files(module) / path
    d = str(p)
    for f in p.glob('**/*.txt'):
        # hidden files
        if any(s.startswith('.') for s in f.split(os.sep)): continue
        for fi in f.iterdir():
            paths[os.path.relpath(os.path.splitext(f)[0], d)] = fi
    return module, paths


# CLI parsing


def as_multiple(x, sep=','):
    '''Ensure a list or tuple. This will also split comma separated strings (like from the cli).'''
    return [si for s in as_list(x) for si in ([s] if callable(s) else str(s).split(sep) if sep else s)]


def as_list(x):
    '''Coerce a value into a list. None converts to an empty list.'''
    return x if isinstance(x, (list, tuple)) else [x] if x is not None else []


if __name__ == '__main__':
    import fire
    fire.Fire()
