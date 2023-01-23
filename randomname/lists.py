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
import random
import difflib

try:
    pass
except ImportError:
    pass

from . import util
from .util import sample_unique, as_multiple, join_path, Aliases


PATH = os.path.dirname(__file__)
WORD_PATH = os.path.join(PATH, 'words')






aliases = util.Aliases({
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
    # full singular
    'adjective': 'adjectives',
    'noun': 'nouns',
    'verb': 'verbs',
    'name': 'names',
})



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
    def __init__(self, value, name=None, exact_match=False):
        self.name = name
        self.exact_match = exact_match
        super().__init__(value or ())

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.name or '--', len(self))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.name)

    def __add__(self, other):
        return WordLists([self, WordList.as_wordlist(other)], name=self.name)

    # def __radd__(self, other):
    #     return WordLists([WordList.as_wordlist(other), self])


    def __sub__(self, other):
        wl = copy.copy(self)
        wl -= other
        return wl

    def __isub__(self, other):
        other = other if isinstance(other, set) else set(other)
        if other:
            self[:] = (w for w in self if w not in other)
        return self

    # def __eq__(self, other):
    #     return list(self) == list(other)

    def __call__(self, *a, **kw):
        return self.sample(*a, **kw)

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

    def copy(self, name=None):
        '''Return a copy of the list.'''
        wl = copy.copy(self)
        if name:
            wl.name = name
        return wl

    def sample(self, n=None):
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
        return sample_unique(random.choice, n, self)

    def search(self, pattern):
        '''Search for a word in the wordlist.

        Arguments:
            pattern (str): The fnmatch pattern to select words by.

        Returns:
            found (list): The word list containing only words that match the pattern.
        
        .. code-block:: python

            for word in wordlist.search("some*"):
                print(word)
        '''
        return WordList(w for w in self if fnmatch.fnmatch(w, pattern))

    def match(self, pattern, exact=None):
        '''Check if a search pattern matches the name of this wordlist.
        
        This is used internally to ``WordLists`` for filtering down the available word lists.

        Arguments:
            pattern (str): The fnmatch pattern to check against.

        .. code-block:: python

            if wordlist.match("nouns/"):
                print("It's a noun wordlist")
        '''
        return self.name if self._matches(pattern, exact) else None

    def _matches(self, pattern, exact=None):
        if pattern == self.name:
            return True
        if self.exact_match if exact is None else exact:
            return False
        if fnmatch.fnmatch(self.name, pattern.rstrip('/')):
            return True
        if self.name.startswith(pattern.rstrip('/') + '/'):
            return True
        return False

    def filter(self, check, *a, **kw):
        '''Filter words from a wordlist using a function that returns a True-thy value 
        if we want to keep the word.
        
        .. code-block:: python

            # remove words over 10 characters
            wl = wordlist.filter(lambda word: len(word) < 10)
            assert all(len(w) < 10 for w in wl)
        '''
        filtered = copy.copy(self)
        filtered[:] = [x for x in filtered if check(x, *a, **kw)]
        return filtered

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
        if callable(value):  # it's a function, draw sample by calling function
            return WordListFunction(value, name, **kw)
        if isinstance(value, str) or isinstance(value, os.PathLike):
            if os.path.isdir(value):
                return cls._from_directory(value, name)
            builtin = os.path.join(WORD_PATH, value, **kw)
            if os.path.isdir(builtin):
                return cls._from_directory(builtin, name or value, **kw)
            return WordListFile(value, name, **kw)
        if isinstance(value, (list, tuple)):
            if all(isinstance(x, str) for x in value):
                return WordList(value, name, **kw)
        if isinstance(value, dict):
            return WordLists([cls.as_wordlist(l, k) for k, l in value.items()], name)
        raise ValueError("Not sure how to convert this to a wordlist: {}".format(value))

    @classmethod
    def _from_directory(cls, path, name=None, **kw):
        fs = util.recursive_files(path)
        if not fs:
            raise OSError(f"Unable to find wordlist: {path!r}")
        wl = WordLists([
            cls.as_wordlist(p, join_path(name, k))
            for k, p in fs.items()
        ], name or os.path.dirname(path), **kw)
        wl -= {
            w for p in glob.glob(os.path.join(path, '.blacklist')) 
            for w in cls.as_wordlist(p)}
        return wl

    # @classmethod
    # def _from_module_directory(cls, path, name=None, module_name='randomname', module_path='words', **kw):
    #     pass

    # @classmethod
    # def combine(cls, lst):
    #     '''Combine multiple wordlists into a single combination wordlist.
    #     '''
    #     return lst[0] if len(lst) == 1 else WordLists(lst)


class WordListFile(WordList):
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
    _loaded = False
    BLACKLIST = []
    def __init__(self, path, name=None, *a, lazy=True, **kw):  # process=None, filters=None, blacklist=None, 
        self.path = path
        # self.process = process

        # self.filters = list(filters or [])
        # if blacklist:
        #     self.filters.append(lambda word: word not in blacklist)
        # self.filters.append(lambda word: word not in self.BLACKLIST)

        if not os.path.exists(self.path):
            raise OSError("Word list does not exist.")
        super().__init__((), name or os.path.splitext(os.path.basename(path))[0], *a, **kw)
        if not lazy:
            self.load()  # not sure the best way to do lazy loading. Otherwise we don't know the length

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__, self.name, 
            len(self) if self._loaded else 'exists' if self.path and os.path.isfile(self.path) else "doesn't exist")

    def load(self, reload=False):
        # print('called load for', self.path)
        if not reload and self._loaded:
            return self
        # print('loading', self.path)
        self.clear()
        with open(self.path, 'r') as f:
            ls = (l.strip() for l in f)
            ls = (l for l in ls if l and l[0] not in self.comment_chars)
            # if self.process:
            #     ls = (self.process(l) for l in ls)
            # ls = (l for l in ls if all(f(l) for f in self.filters))
            self.extend(ls)
        self._loaded = True
        return self

    def clear(self):
        super().clear()
        self._loaded = False

    # lazy loading

    def __len__(self):
        self.load()
        return super().__len__()

    def __contains__(self, item):
        self.load()
        return super().__contains__(item)

    def __getitem__(self, key):
        self.load()
        return super().__getitem__(key)

    def __iter__(self):
        self.load()
        return super().__iter__()

    def sample(self, *a, **kw):
        self.load()
        return super().sample(*a, **kw)

    def filter(self, *a, **kw):
        self.load()
        return super().filter(*a, **kw)
    

class WordListFunction(WordList):
    '''A word list that gets sampled one-by-one from a function.
    
    .. code-block:: python

        import random
        def myuniqueid(x=100):
            return 'myid-{}'.format(random.randint(x))
        
        # prepare the wordlist function
        lst = WordListFunction(myuniqueid)

        # myuniqueid is not run until sample is called
        assert lst.sample().startswith('myid-'), 'this should sample an id'
        assert len(lst.sample(3)) == 3, 'this should sample 3 ids'

    '''
    def __init__(self, func, name=None, length=1000, *a, **kw):
        self.func = func
        super().__init__([None]*length, name or func.__name__, *a, **kw)

    def __iter__(self):
        for x in super().__iter__():
            if x is not None:
                yield x

    def __getitem__(self, index):
        if isinstance(index, slice):
            # sample any values requested by the slice
            xs = self[index] = [
                self.sample() if x is None else x
                for x in super().__getitem__(index)
            ]
            return xs
        x = super().__getitem__(index)
        if x is None:
            self[index] = x = self.sample()
        return x

    def sample(self, n=None, unique=False, **kw):
        return sample_unique(self.func, n, unique=unique, **kw)

    def match(self, pattern):
        parts = pattern.split('/', 1)
        if self.name == parts[0]:
            return '/'.join([self.name] + parts[1:])


class WordLists(WordList):
    '''Combines multiple wordlists so that they function as one.
    
    .. code-block:: python

        words = WordLists([
            WordList(['cookie', 'cat']), 
            WordListFile('my/wordlist.txt'),
            WordListFile('my/second-wordlist.txt'),
        ])

    '''
    def __init__(self, lists=None, name=None, aliases=aliases, true_word_distribution=False, default_list=None, **kw):
        # self._lookup = {}
        self.lists = []
        self.aliases = Aliases.as_alias(aliases)
        self.true_word_distribution = true_word_distribution
        self.default_list = default_list
        super().__init__([], name, **kw)
        for l in lists or ():
            self._append(l)
        

    def __repr__(self):
        return '{}({}, {} lists, {})'.format(
            self.__class__.__name__, self.name, len(self.lists), 
            ''.join('\n  {}'.format(l.name) for l in self.lists))


    # list management

    def __isub__(self, other):
        other = other if isinstance(other, set) else set(WordList.as_wordlist(other))
        if other:
            for l in self.lists:
                l -= other
        return self

    def add(self, lst, name=None, conflict='merge'):
        '''Add a wordlist.
        
        Arguments:
            lst: Anything that can be converted to a wordlist (path, list of words, function, etc.)
            name (str): A name to give the list.
            conflict (str): What to do with name conflict. Possible values:
                'error': throw error if key already exists, 
                'merge': combine with existing list, 
                'overwrite': overwrite existing list.
        '''
        self._append(lst, name, conflict)

    # def extend(self, lst, conflict='merge'):
    #     '''Add multiple wordlists.'''
    #     for l in lst:
    #         self._append(l, conflict=conflict)

    # def register(self, word_lists, name=None, **kw):
    #     '''Register a directory of word lists.
        
    #     Arguments:
    #         word_lists (str, dict): This can either be a file or directory pointing to the
    #             desired word lists, or a dict of name -> word list
    #     '''
    #     blacklist = []
    #     for key, lst in self._as_list_candidates(word_lists, name, **kw):
    #         if key == 'BLACKLIST':
    #             blacklist.append(lst)
    #             continue
    #         self._append(lst, key)
    #     if blacklist:
    #         self -= {w for b in blacklist for w in b}
    #     return self

    def _append(self, lst, name=None, conflict='merge'):
        lst = WordList.as_wordlist(lst, name)
        name = name or lst.name
        # if name in self._lookup:
        #     if conflict == 'error':
        #         raise KeyError('List with name {} already exists.'.format())
        #     if conflict == 'merge':
        #         lst = WordList(list(self._lookup[name]) + list(lst), name)
        self.lists.append(lst)
        # self._lookup[name] = lst

    # def _as_list_candidates(self, word_lists, name=None, blacklists=True):
    #     if isinstance(word_lists, str):
    #         if os.path.isfile(word_lists):  # if it is a file, treat it as one
    #             yield name or os.path.splitext(word_lists)[0].rsplit(os.sep, -1)[-1], word_lists
    #             return
            
    #         builtin_fname = os.path.join(WORD_PATH, word_lists)
    #         if os.path.exists(builtin_fname):
    #             word_lists = builtin_fname
    #         # otherwise treat as a directory
    #         fs = util.recursive_files(word_lists)
    #         if not fs:
    #             raise ValueError(f"Unable to find wordlist: {word_lists!r}")
    #         for key, path in fs.items():
    #             yield join_path(name, key), path
    #         if blacklists:
    #             for f in glob.glob(os.path.join(word_lists, '.blacklist')):
    #                 yield "BLACKLIST", f
    #         return
    #     # allow passing a dict of lists (or paths)
    #     elif isinstance(word_lists, dict):
    #         for key, lst in word_lists.items():
    #             yield join_path(name, key), lst
    #         return
    #     yield name, word_lists

    # @classmethod
    # def from_directory(cls, path, name=None):
    #     builtin_fname = os.path.join(WORD_PATH, path)
    #     if os.path.exists(builtin_fname):
    #         path = builtin_fname
    #     fs = util.recursive_files(path)
    #     if not fs:
    #         raise ValueError(f"Unable to find wordlist: {path!r}")
    #     wl = cls([], name)
    #     for key, path in fs.items():
    #         wl.append(path, join_path(name, key))
    #     return wl


    # content access

    def sample(self, n=None):
        '''Sample one or more word from the word list.'''
        if self.true_word_distribution:
            return super().sample(n)
        return sample_unique(self._sample, n)

    def _sample(self):
        return random.choice(self.lists).sample()

    def filter(self, check):
        '''Filter '''
        wl = copy.copy(self)
        wl.lists = [l.filter(check) for l in self.lists]
        return wl

    def __len__(self):
        '''Length of all wordlists.'''
        return sum(len(lst) for lst in self.lists)
        # try:
        #     # print(sum(len(lst) for lst in self.lists))
        #     return sum(len(lst) for lst in self.lists)
        # except ValueError:
        #     import traceback
        #     traceback.print_exc()
        #     raise

    def __contains__(self, item):
        '''Any wordlist contains word.'''
        return any(item in l for l in self.lists)

    def __iter__(self):
        '''Iterate all the wordlists.'''
        for lst in self.lists:
            yield from lst

    def __getitem__(self, index):
        '''Get the item by index.'''
        if isinstance(index, str):
            index = self.aliases(index)
            return WordLists.combine([
                l for l in self.lists if l.match(index, exact=True)
            ])
            # return self._lookup[self.aliases(index)]
        if not self.lists:
            raise IndexError(index)
        if isinstance(index, slice):
            # lookup the start/end of a slice
            rel_start, lst_start, j_start, start = self._find_offset(index.start or 0)
            rel_end, lst_end, j_end, end = self._find_offset(index.stop, j_start, start)

            if lst_start is not lst_end:  # not within a single list
                out = lst_start[rel_start:]
                out.extend(x for lst in self.lists[j_start+1:j_end] for x in lst)
                out.extend(lst_end[:rel_end])
            else:
                out = lst_start[rel_start:rel_end]
            return out[::index.step]
        # lookup single index
        rel_idx, lst, _, _ = self._find_offset(index)
        # print(rel_idx, lst, i_lst, offset)
        if lst is not None:
            return lst[rel_idx]
        raise IndexError(index)

    def _find_offset(self, index, start=0, offset=0):
        '''Using the global index, find the list that contains it and its relative index.
        
        Arguments:
            index (int): The global list index. In [0, sum(len(l) for l in lists)]
            start (int): The list index to start with. In [0, len(lists)]
            offset (int): The total length of all previous lists. (Used for resuming previous call.)

        Returns:
            rel_index (int): The index relative to the offset.
            lst (WordList): The word list that contains that index.
            i_lst (int): The index of the list selected. In [0, len(lists)]
            offset (int): The total length of all previous lists. Pass this if you provide ``start``.

        To resume a offset search.

        .. code-block:: python

            # finding a slice can be done like this.
            rel_start, start, lst_start, j_start = self._find_offset(index.start or 0)
            rel_end, end, lst_end, j_end = self._find_offset(index.stop, j_start, start)
        
        '''
        if index is None:  # shortcut to the end
            if self.lists:
                return None, self.lists[-1], len(self.lists)-1, None
            return None, None, None, None
        # find the list we're trying to index
        for i_lst, lst in enumerate(self.lists[start:]):
            end = offset + len(lst)
            if index < end:
                return index - offset, lst, i_lst, offset
            offset = end
        return None, None, None, None




    # list filtering

    def filter_lists(self, *names, accept_literals=False):
        '''Filter lists using pattern matching.'''
        if not names:
            return self
        names = [n for ns in names for n in as_multiple(ns)]
        lsts = []
        literals = []
        for name in names:
            if accept_literals and '/' not in name:
                literals.append(name)
                continue
            lsts.extend(self._match(name))
        if literals:
            lsts.append(WordList(literals, 'literals'))
        return WordLists(lsts, ','.join(map(str, names)))

    def _match(self, name, *a, require=True, **kw):
        '''Resolve a fuzzy-matched category. Throw an error if it doesn't
        match anything.'''
        name = self.aliases(name)

        # gather wordlists to check
        lists = self.lists
        # if self.default_list:
        #     dft = self._lookup[self.default_list]
        #     assert isinstance(dft, WordLists)
        #     lists = dft.lists + lists

        # gather matched wordlists
        matches = []
        for l in lists:
            if l.match(name):
                if isinstance(l, WordLists):
                    # XXX:
                    name_i = util.remove_prefix(name, l.name).lstrip('/')
                    matches.extend(l._match(name_i, require=False) if name_i else l)
                else:
                    matches.append(l)
        if not require or matches:
            return matches

        # no matches. throw nice error
        matches = self._close_matches(name, *a, **kw)
        raise ValueError("No matching wordlist '{}'. {}".format(
            name, 'Did you mean {}?'.format(_or_fmt(matches)) if matches else
            'No close matches found.'))

    def _close_matches(self, name, cutoff=0.65):
        '''Find close matching wordlist names. This is used for a 
        Did you mean? error to correct misspellings.'''
        # they entered a underspecified category
        name = self.aliases(name)
        print(name)
        cats = [l.name for l in self.lists]
        word_classes, _, subcats = zip(*(c.partition('/') for c in cats))
        matches = [cat for cat, sub in zip(cats, subcats) if name == sub]

        if '/' in name:
            part0, part1 = name.split('/', 1)
            part0 = part0 or '*'
            # they spelled the first part correctly
            if part0 in word_classes:
                avail = [sub for c, sub in zip(word_classes, subcats) if part0 == c]
                _ms = _get_matches(part1, avail, cutoff=cutoff)
                matches += [k for k in ('{}/{}'.format(part0, m) for m in _ms) if k in cats]
            # they entered a misspelled category
            elif part1 in subcats:
                avail = [c for c, sub in zip(word_classes, subcats) if part1 == sub]
                _ms = _get_matches(part0, avail, cutoff=cutoff)
                matches += [k for k in ('{}/{}'.format(m, part1) for m in _ms) if k in cats]
            # they entered a misspelled category and misspelled group
            else:
                matches += _get_matches(name, cats, cutoff=cutoff)
        else:
            # get sub matches
            _ms = _get_matches(name, subcats, cutoff=cutoff)
            matches += [
                '{}/{}'.format(pos, cat) for cat in _ms 
                for pos in (c for c, sub in zip(word_classes, subcats) if cat == sub)]

        # remove duplicates
        return _ordered_unique(matches)

    # def get_parts_of_speech(self, name):
    #     '''Get all parts of speech that a category belongs to.'''
    #     names = (l.name for l in self.lists)
    #     parts = (n.split('/', 1) for n in names)
    #     parts = (p[:2] if len(parts) > 1 else p + [''] for p in parts)
    #     return {pos for pos, name_i in parts if name in name_i}

    def squeeze(self):
        return self.lists[0] if len(self.lists) == 1 else self

    @classmethod
    def combine(cls, lsts):
        return lsts[0] if len(lsts) == 1 else cls(lsts)



def _get_matches(pattern, available, **kw):
    return (
        difflib.get_close_matches(pattern, available, **kw) +
        [m for m in available if m.startswith(pattern) or fnmatch.fnmatch(m, pattern)])


def _or_fmt(fnames):
    return ' or '.join("'{}'".format(f) for f in fnames)


def _ordered_unique(xs):
    unique = []
    for x in xs:
        if x not in unique:
            unique.append(x)
    return unique

