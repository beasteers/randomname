import functools
from .core import *

def main():
    # need to wrap these so they go to stdout - idk whats going on
    @functools.wraps(get_name)
    def print_name(*a, **kw):
        print(get_name(*a, **kw))

    @functools.wraps(generate)
    def print_generate(*a, **kw):
        print(generate(*a, **kw))

    import fire
    fire.Fire({
        'get': print_name, 'generate': print_generate,
        'available': available, 'sample': sample})
