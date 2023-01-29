'''

The purpose of the WordList class is to allow you to define word lists from a variety of sources.
This basic class just takes wordlists from a lists and uses that as a literal word list.
Subclasses allow you to get wordlists from a file, directory, function, or other source.

Then you can take those lists and call list.sample() to get a element from it.

If you have a collection of wordlists, you can call wordlists.filter('nouns/*') and it would 
only sample from the noun wordlists, utilizing lazy loading to only load the lists that you need.

'''
import os
import copy
import glob
import fnmatch

import randomname
from randomname import rng

from . import imprc, BUILTIN_LIST_LOCATION
from .. import util
from ..util import sample_unique, join_path


class WordList(list):
    '''A basic word list - just pass a list of words.

    Arguments:
        value (list): A list of words to sample from.
        name (str): The name of the word list. This is used for list filtering.
        filters (list): 
        blacklist (list): Words to 
        exact_match (bool):
    
    .. code-block:: python

        words = ['cat', 'cookie', 'coffee']
        
        lst = WordList(words, 'nouns/mywords')
        assert lst.sample() in words, 'this should sample a single word from the list'
        assert len(lst.sample(3)) == 3, 'this should sample 3 words from the list'
    '''
    def __init__(self, value, name=None, listpath=None, exact_match=False):
        self.name = name
        self.listpath = listpath
        self.exact_match = exact_match
        super().__init__(value or ())

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.name or '--', len(self))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        '''Can be used as a dictionary key.'''
        return hash(self.name)

    def __add__(self, other):
        '''Concatenate too wordlists together, creating a new wordlist.'''
        return randomname.WordLists([self, WordList.as_wordlist(other)], name=self.name)

    # def __radd__(self, other):
    #     return WordLists([WordList.as_wordlist(other), self])


    def __sub__(self, other):
        '''Subtract two wordlists, returning a copy.'''
        wl = self.copy()
        wl -= other
        return wl

    def __isub__(self, other):
        '''Subtract a wordlist from another, in-place.'''
        other = other if isinstance(other, set) else set(other)
        if other:
            self[:] = (w for w in self if w not in other)
        return self

    # def __eq__(self, other):
    #     return list(self) == list(other)

    # def __call__(self, *a, **kw):
    #     '''Sample from the wordlist. See ``WordList.sample()`` for details.'''
    #     return self.sample(*a, **kw)

    def dump(self, path, mkdir=True):
        '''Save the word list to disk.

        Arguments:
            path (str): The path to save the wordlist to.
        
        .. code-block:: python

            wordlist = randomname.WordList(['cat', 'cookie', 'coffee'])

            # write wordlist to file and then read it back
            path = wordlist.dump('my/new/wordlist.txt')
            wordlist2 = WordListFile(path)
            assert list(wordlist) == list(wordlist2)
        '''
        if mkdir:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('\n'.join(self))
        return path

    def copy(self, values=None, name=None):
        '''Return a copy of the list.'''
        wl = copy.copy(self)
        if name:
            wl.name = name
        if values is not None:
            wl[:] = values
        return wl


    # ---------------------------------------------------------------------------- #
    #                                   Sampling                                   #
    # ---------------------------------------------------------------------------- #

    def sample(self, n=None, **kw):
        '''Sample one or more word from the word list.

        Arguments:
            n (int, None): The number of examples to return.

        Returns:
            sampled_words: a single sampled word (str) if n is None 
            else a list of sampled words.
        
        .. code-block:: python

            # sample a single word
            word = wordlist.sample()
            assert isinstance(word, str)

            # sample a list of words
            words = wordlist.sample(5)
            assert isinstance(words, list) and len(words) == 5
            words = wordlist.sample(20)
            assert isinstance(words, list) and len(words) == 20
            words = wordlist.sample(1)
            assert isinstance(words, list) and len(words) == 1
        '''
        return sample_unique(rng.choice, n, self, **kw)


    # ---------------------------------------------------------------------------- #
    #                                Word operators                                #
    # ---------------------------------------------------------------------------- #

    def find(self, pattern):
        '''Search for a word in the wordlist.

        Arguments:
            pattern (str): The fnmatch pattern to select words by.

        Returns:
            found (list): The word list containing only words that match the pattern.
        
        .. code-block:: python

            for word in wordlist.search("some*"):
                print(word)
        '''
        if isinstance(pattern, str):
            name, pattern = pattern, lambda x: fnmatch.fnmatch(x, name)
        else:
            name = getattr(pattern, '__name__', None)
        return WordList((w for w in self if pattern(w)), name=name)

    def filter(self, check, *a, **kw):
        '''Filter words from a wordlist using a function that returns a Truethy value 
        if we want to keep the word.
        
        .. code-block:: python

            # remove words over 10 characters
            wl = wordlist.filter(lambda word: len(word) < 10)
            assert all(len(w) < 10 for w in wl)
        '''
        if isinstance(check, str):
            s, check = check, lambda x: fnmatch.fnmatch(x, s)
        filtered = self.copy()
        filtered[:] = [x for x in filtered if check(x, *a, **kw)]
        return filtered


    # ---------------------------------------------------------------------------- #
    #                         Matching lists based on name                         #
    # ---------------------------------------------------------------------------- #

    def _get_matches(self, pattern, **kw):
        '''Check if a search pattern matches the name of this wordlist.
        
        This is used internally to ``WordLists`` for filtering down the available word lists.

        Arguments:
            pattern (str): The fnmatch pattern to check against.

        .. code-block:: python

            if wordlist.match_wordlist_name("nouns/"):
                print("It's a noun wordlist")
        '''
        return [self] if self._matches_name(pattern, **kw) else []

    def _matches_name(self, pattern, exact=None):
        if not self.name:
            return False
        if pattern.strip('/') == self.name:
            return True
        # if it requires an exact match, exit early
        if self.exact_match if exact is None else exact:
            return False
        # user provided asterisk - verbs/*
        if fnmatch.fnmatch(self.name, pattern.strip('/')):
            return True
        # check for prefix
        if self.name.startswith(f'{pattern.rstrip("/")}/'):
            return True
        # check for suffix
        if self.name.endswith(f'/{pattern.lstrip("/")}'):
            return True
        # check for pattern somewhere in path
        if fnmatch.fnmatch(self.name, f'*/{pattern.strip("/")}/*'):
            return True
        return False

    def _iter_list_names(self):
        yield self.name

    # ---------------------------------------------------------------------------- #
    #                              Class Constructors                              #
    # ---------------------------------------------------------------------------- #

    @classmethod
    def as_wordlist(cls, value, name=None, **kw):
        '''Coerce a value into a wordlist.
        
        .. code-block:: python

            wl = WordList.as_wordlist(['cookie', 'cat'])
            assert isinstance(wl, WordList)
            wl = WordList.as_wordlist('path/to/file.txt')
            assert isinstance(wl, WordListFile)
            wl = WordList.as_wordlist(my_word_function)
            assert isinstance(wl, WordListFunction)

        '''
        if isinstance(value, WordList):  # already a wordlist
            return value
        # wordlist function
        if callable(value):
            return randomname.WordListFunction(value, name, **kw)
        # check for builtin list
        if isinstance(value, str) and not value.startswith(os.sep) or isinstance(value, imprc.resources_abc.Traversable):
            builtin_path = BUILTIN_LIST_LOCATION / value
            if builtin_path.is_dir():
                return cls._from_package_dir(builtin_path, name, **kw)

        # local directory/file
        if isinstance(value, (str, os.PathLike)):
            if os.path.isdir(value):
                return cls._from_directory(value, name, **kw)
            elif not os.path.isfile(value):
                raise OSError(f"File not found: {value}")
            return randomname.WordListFile(value, name, **kw)

        # listeral list
        if isinstance(value, (list, tuple)):
            if all(isinstance(x, str) for x in value):
                return WordList(value, name, **kw)
        # dict of word lists
        if isinstance(value, dict):
            return randomname.WordLists.combine([
                cls.as_wordlist(l, k) 
                for k, l in value.items()
            ], name=name, **kw)
        raise ValueError("Not sure how to convert this to a wordlist: {}".format(value))

    @classmethod
    def _from_directory(cls, path, name=None, **kw):
        fs = util.recursive_files(path)
        if not fs:
            raise OSError(f"Unable to find wordlist: {path!r}")
        wl = randomname.WordLists.combine([
            cls.as_wordlist(p, k)#join_path(name, k)
            for k, p in fs.items()
        ], name=name or os.path.basename(path), **kw)
        wl -= {
            w for p in glob.glob(os.path.join(path, '.blacklist')) 
            for w in cls.as_wordlist(p)}
        return wl

    @classmethod
    def _from_package_dir(cls, path, name=None, **kw):
        fs = list(util.recursive_traversable(path, ext='.txt'))
        if not fs:
            raise OSError(f"Unable to find wordlist: {path!r}")
        wl = randomname.WordLists.combine([
            randomname.WordListPackageFile(p, name.split('/',1)[-1])
            for name, p in fs
        ], name=name or path.name, **kw)
        blacklist = path / '.blacklist'
        if blacklist.is_file():
            wl -= cls.as_wordlist(blacklist, '.blacklist')
        return wl
