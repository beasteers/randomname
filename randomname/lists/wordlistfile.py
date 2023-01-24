import os
try:
    from importlib.resources import files as ir_files, as_file as ir_as_file
except ImportError:
    from importlib_resources import files as ir_files, as_file as ir_as_file

import randomname
from .lazywordlist import LazyWordList


class WordListFile(LazyWordList):
    '''
    A word list that gets loaded from file. This is loaded lazily, only when you try to sample from
    the word list, or if you do something like try to check its length.
    
    .. code-block:: python

        words = ['cat', 'cookie', 'coffee']

        # so we have a text file with line separated words
        path = 'wordfile.txt'
        with open(path, 'w') as f:
            f.write('\\n'.join(words))
        
        # create the word list and sample from it
        lst = WordListFile(path)
        assert lst.sample() in words, 'this should sample a single word from the list'
        assert len(lst.sample(3)) == 3, 'this should sample 3 words from the list'
    '''
    comment_chars = ';#'
    def __init__(self, path, name=None, *a, lazy=True, **kw):  # process=None, filters=None, blacklist=None, 
        self.path = path
        # self.process = process

        if not os.path.exists(self.path):
            raise OSError("Word list does not exist.")
        super().__init__(
            (), name or os.path.splitext(os.path.basename(path))[0], 
            *a, lazy=lazy, **kw)
        

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__, self.name, 
            len(self) if self._loaded else 'exists' if self.path and os.path.isfile(self.path) else "doesn't exist")

    def _load(self):
        with open(self.path, 'r') as f:
            ls = (l.strip() for l in f)
            ls = (l for l in ls if l and l[0] not in self.comment_chars)
            # if self.process:
            #     ls = (self.process(l) for l in ls)
            # ls = (l for l in ls if all(f(l) for f in self.filters))
            self.extend(ls)


class WordListPackageFile(LazyWordList):
    def __init__(self, value, name=None, module=randomname, **kw):
        self.module = module
        super().__init__(value, name, **kw)

    def _load(self):
        with ir_as_file(ir_files(self.module).joinpath(self.path)) as eml:
            pass

# class WordListPackage(LazyWordList):
#     def __init__(self, value, name=None, module=randomname, exact_match=False, lazy=True):
#         self.module = module
#         super().__init__(value, name, exact_match, lazy)

#     def _load(self):
#         with ir_as_file(ir_files(self.module).joinpath(self.path)) as eml:
#             pass