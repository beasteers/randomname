import copy
import random
import difflib
import fnmatch

import randomname
from randomname import rng

from .wordlist import WordList
from .. import util
from ..util import Aliases, sample_unique, as_multiple


class WordLists(WordList):
    '''Combines multiple wordlists so that they function as one.
    
    .. code-block:: python

        words = WordLists([
            WordList(['cookie', 'cat']), 
            WordListFile('my/wordlist.txt'),
            WordListFile('my/second-wordlist.txt'),
        ])

    '''
    def __init__(self, lists=[], name=None, aliases=None, true_word_distribution=False, default_list=None, **kw):
        # self._lookup = {}
        self.lists = []
        self.aliases = randomname.aliases if aliases is None else Aliases.as_alias(aliases)
        self.true_word_distribution = true_word_distribution
        self.default_list = default_list
        super().__init__([], name, **kw)
        for l in lists or ():
            self._append(l)
        

    def __repr__(self):
        return '{}({}, {} lists, {})'.format(
            self.__class__.__name__, self.name, len(self.lists), 
            ''.join('\n  {}'.format(l.name) for l in self.lists))

    # def __getattr__(self, k):
    #     # try:
    #     #     return super().__getattr__(k)
    #     # except AttributeError:
    #     # if k.startswith('_'):
    #     #     return object.__getattr__(self, k)
    #     # if k not in self.__dict__:
    #     if k != 'lists':
    #         for l in self.lists:
    #             if util.remove_prefix(l.name, f'{self.name}/') == k:
    #                 return l
    #     raise AttributeError(k)

    # def __dir__(self):
    #     return list(super().__dir__()) + [util.remove_prefix(l.name, f'{self.name}/') for l in self.lists]

    # list management

    def __isub__(self, other):
        '''In-place subtraction. This makes a copy of child lists.'''
        other = other if isinstance(other, set) else set(WordList.as_wordlist(other))
        if other:
            self.lists = [l - other for l in self.lists]
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
        return rng.choice(self.lists).sample()

    def filter(self, check):
        '''Filter the wordlist using a condition.'''
        wl = copy.copy(self)
        lists = [l.filter(check) for l in self.lists]
        wl.lists = [l for l in lists if l]
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
        # lookup wordlist by name
        if isinstance(index, str):
            index = self.aliases(index)
            return WordLists.combine([
                l for l in self.lists if l.match_wordlist_name(index, exact=True)
            ])
            # return self._lookup[self.aliases(index)]

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

        # no lists so there's nothing to get
        if not self.lists:
            raise IndexError(index)

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
            lsts.extend(self._match_wordlist_name(name))
        if literals:
            lsts.append(WordList(literals, 'literals'))
        return WordLists(lsts, ','.join(map(str, names)))

    def _match_wordlist_name(self, name, require=True, **kw):
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
            if l.match_wordlist_name(name):
                if isinstance(l, WordLists):
                    # XXX:
                    name_i = util.remove_prefix(name, l.name).lstrip('/') if l.name else name
                    matches.extend(l._match_wordlist_name(name_i, require=False) if name_i else l)
                else:
                    matches.append(l)
        if not require or matches:
            return matches

        # no matches. throw nice error
        matches = self._close_matches(name, **kw)
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
