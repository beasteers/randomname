import functools
from .core import *
from . import util

def main():
    import fire
    fire.Fire({
        'get': prints(get_name), 'generate': prints(generate),
        'available': available, 'sample': sample, 'util': util})

def prints(func):
    # need to wrap funcs so they go to stdout - idk whats going on
    @functools.wraps(func)
    def inner(*a, **kw):
        print(func(*a, **kw))
    return inner
