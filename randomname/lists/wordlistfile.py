import os
import randomname
from . import imprc
from .lazywordlist import LazyWordList


class _BaseWordListFile(LazyWordList):
    comment_chars = ';#'
    def _process_lines(self, lines):
        lines = (l.strip() for l in lines)
        lines = (l for l in lines if l and l[0] not in self.comment_chars)
        return lines

class WordListFile(_BaseWordListFile):
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
    def __init__(self, path, name=None, *a, **kw):
        self.path = path

        if not os.path.exists(self.path):
            raise OSError("Word list does not exist.")
        super().__init__(
            (), name or os.path.splitext(os.path.basename(path))[0], 
            *a, **kw)

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__, self.name, 
            len(self) if self._loaded else 'exists' if self.path and os.path.isfile(self.path) else "doesn't exist")

    def _load(self):
        with open(self.path, 'r') as f:
            self.extend(self._process_lines(f))


class WordListPackageFile(_BaseWordListFile):
    def __init__(self, handle, name=None, **kw):
        assert isinstance(handle, imprc.resources_abc.Traversable)
        self.handle = handle
        super().__init__([], name or getattr(handle, 'name', None), **kw)

    def _load(self):
        f = self.handle.read_text().splitlines()
        self.extend(self._process_lines(f))
