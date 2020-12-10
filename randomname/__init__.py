import functools
from .core import *
from . import util

def main():
    import fire
    fire.Fire({
        'get': prints(get_name), 'generate': prints(generate),
        'available': available, 'sample': prints(sample), 'util': util,
        'sample_words': sample_words})

def prints(func):
    # need to wrap funcs so they go to stdout - idk whats going on
    @functools.wraps(func)
    def inner(*a, **kw):
        x = func(*a, **kw)
        if isinstance(x, (list, tuple)):
            for i in x:
                print(i)
        elif isinstance(x, dict):
            for k, v in x.items():
                print('{}: {}'.format(k, v))
        else:
            print(x)
    return inner
