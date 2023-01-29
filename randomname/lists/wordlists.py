import copy
import random
import difflib
import fnmatch

import randomname
from randomname import rng

from .wordlist import WordList
from .. import util
from ..util import Aliases, sample_unique, as_multiple
from .. import matching


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
        # lists = [li for l in lists for li in (l.lists if isinstance(l, WordLists) else [l])]
        for l in lists or ():
            self.add(l)
        

    def __repr__(self):
        return '{}({}, {} lists, {})'.format(
            self.__class__.__name__, self.name, len(self.lists), 
            ''.join('\n  {}'.format(l.name) for l in self.lists))


    # ---------------------------------------------------------------------------- #
    #                                List Operators                                #
    # ---------------------------------------------------------------------------- #

    def __isub__(self, other):
        '''In-place subtraction. This makes a copy of child lists.'''
        other = other if isinstance(other, set) else set(WordList.as_wordlist(other))
        if other:
            self.lists = [l - other for l in self.lists]
        return self

    def add(self, lst, name=None, conflict='overwrite'):
        '''Add a wordlist.
        
        Arguments:
            lst: Anything that can be converted to a wordlist (path, list of words, function, etc.)
            name (str): A name to give the list.
            conflict (str): What to do with name conflict. Possible values:
                'error': throw error if key already exists, 
                'merge': combine with existing list, 
                'overwrite': overwrite existing list.
        '''
        lst = WordList.as_wordlist(lst, name)
        for i, l in enumerate(self.lists):
            if l.name == lst.name:
                if conflict == 'merge':
                    self.lists[i][:] = util.unique(list.__add__(self.lists[i], lst))
                    return
                if conflict == 'overwrite':
                    self.lists[i] = lst
                    return
                if conflict == 'error':
                    raise ValueError(f"Wordlist {lst.name!r} already exists.")
        self.lists.append(lst)

    def extend(self, lst, conflict='overwrite'):
        '''Add multiple wordlists.'''
        for l in lst:
            self.add(l, conflict=conflict)

    def __len__(self):
        '''Length of all wordlists.'''
        return sum(len(lst) for lst in self.lists)

    def __contains__(self, item):
        '''Any wordlist contains word.'''
        return any(item in l for l in self.lists)

    def __iter__(self):
        '''Iterate all the wordlists.'''
        for lst in self.lists:
            yield from lst


    # ---------------------------------------------------------------------------- #
    #                                Sampling words                                #
    # ---------------------------------------------------------------------------- #

    def sample(self, n=None):
        '''Sample one or more word from the word list.'''
        if self.true_word_distribution:
            return super().sample(n)
        return sample_unique(self._sample, n)

    def _sample(self):
        return rng.choice(self.lists).sample()


    # ---------------------------------------------------------------------------- #
    #                                Word Operators                                #
    # ---------------------------------------------------------------------------- #

    def filter(self, check):
        '''Filter the wordlist using a condition.'''
        wl = self.copy()
        wl.lists = [l for l in (l.filter(check) for l in self.lists) if l]
        return wl


    # ---------------------------------------------------------------------------- #
    #                           Accessing items by index                           #
    # ---------------------------------------------------------------------------- #

    def get(self, index, default=None):
        index = self.aliases(index)
        ls = [l for l in self.lists if l._get_matches(index, exact=True)]
        return WordLists.combine(ls) if ls else default

    def __getitem__(self, index):
        '''Get the item by index.'''
        if isinstance(index, slice):
            if index.start is None and index.stop is None:
                return self.copy()
            # lookup the start/end of a slice
            rel_start, lst_start, j_start, start, _ = self._find_offset(index.start or 0)
            if lst_start is None or j_start is None:
                return self.copy([])
            rel_end, lst_end, j_end, _, _ = self._find_offset(index.stop, j_start, start or 0)
            if lst_end is None:
                return self.copy([])  # pragma: no cover

            if lst_start is not lst_end:  # not within a single list
                out = lst_start[rel_start:]
                out.extend(x for lst in self.lists[j_start+1:j_end] for x in lst)
                out.extend(lst_end[:rel_end])
            else:
                out = lst_start[rel_start:rel_end]
            return out[::index.step]

        # lookup wordlist by name
        if isinstance(index, str):
            wl = self.get(index)
            if wl is None:
                raise KeyError(index)
            return wl

        # no lists so there's nothing to get
        if not self.lists:
            raise IndexError(index)

        # lookup single index
        rel_idx, lst, _, _, valid = self._find_offset(index)
        if valid and lst is not None and rel_idx < len(lst):
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
            valid_value (bool): Whether the index points to a valid value. 

        To resume a offset search.

        .. code-block:: python

            # finding a slice can be done like this.
            rel_start, start, lst_start, j_start = self._find_offset(index.start or 0)
            rel_end, end, lst_end, j_end = self._find_offset(index.stop, j_start, start)
        
        '''
        if index is None:  # shortcut to the end
            if self.lists:
                l = self.lists[-1]
                return len(l), l, len(self.lists)-1, None, False
        # find the list we're trying to index
        i_lst, lst = 0, None
        for i_lst, lst in enumerate(self.lists[start:]):
            end = offset + len(lst)
            if index < end:
                return index - offset, lst, i_lst, offset, True
            offset = end
        return index - offset, lst, i_lst, offset, False


    # ---------------------------------------------------------------------------- #
    #                            Accessing lists by name                           #
    # ---------------------------------------------------------------------------- #

    def subset(self, *names, accept_literals=False):
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
            lsts.extend(self._get_matches(name, require=True))
        if literals:
            lsts.append(WordList(literals, '__literals__'))
        return WordLists.combine(lsts, name=','.join(map(str, names)))

    def _get_matches(self, name, require=False, **kw):
        '''Resolve a fuzzy-matched category. Throw an error if it doesn't
        match anything.'''
        name = self.aliases(name)
        if name.strip('/') == self.name:
            return [self]

        # gather matched wordlists
        matches = []
        name_i = util.remove_prefix(name, self.name).lstrip('/')
        for l in self.lists:
            matches.extend(l._get_matches(name_i))
        if not require or matches:
            return matches

        # no matches. throw nice error
        matches = self.close_matches(name, **kw)
        raise ValueError("No matching wordlist '{}'. {}".format(
            name, f'Did you mean {_or_fmt(matches)}?' if matches else
            'No close matches found.'))

    def _iter_list_names(self):
        for l in self.lists:
            for name in l._iter_list_names():
                yield util.join_path(self.name, name)

    # ---------------------------------------------------------------------------- #
    #                                Error reporting                               #
    # ---------------------------------------------------------------------------- #

    def close_matches(self, name, **kw):
        return matching.close_matches(
            self.aliases(name), list(self._iter_list_names()), **kw)


    # ---------------------------------------------------------------------------- #
    #                      Minimizing extra wrapper WordLists                      #
    # ---------------------------------------------------------------------------- #

    def squeeze(self):
        return self.lists[0] if len(self.lists) == 1 else self

    @classmethod
    def combine(cls, lsts, **kw):
        return lsts[0] if len(lsts) == 1 else cls(lsts, **kw)



# ---------------------------------------------------------------------------- #
#                                     Utils                                    #
# ---------------------------------------------------------------------------- #


def _or_fmt(words):
    '''List options separated by "or".'''
    return ' or '.join(f'{x!r}' for x in words)

# def try_len(x, default=0):
#     try:
#         return len(x)
#     except Exception:
#         return default