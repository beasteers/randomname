import os
import randomname as rn
from randomname.lists import WordList, WordListFunction

import pytest


def test_as_wordlist():

    # as_wordlist( list )
    wl = rn.WordList.as_wordlist(['a', 'b'])
    assert wl.__class__ is rn.WordList
    assert list(wl) == ['a', 'b']

    # as_wordlist( WordList )
    assert rn.WordList.as_wordlist(wl) is wl

    # as_wordlist( WordListFunction )
    import random
    wl = rn.WordList.as_wordlist(random.random)
    assert isinstance(wl, rn.WordListFunction)

    # as_wordlist( filename )
    wl = rn.WordList.as_wordlist(os.path.join(rn.WORD_PATH, 'imsky/adjectives/colors.txt'))
    assert isinstance(wl, rn.WordListFile)

    # as_wordlist( directory )
    wl = rn.WordList.as_wordlist(os.path.join(rn.WORD_PATH, 'imsky'))
    assert isinstance(wl, rn.WordLists)

    # as_wordlist( builtin_directory )
    wl = rn.WordList.as_wordlist('imsky')
    assert isinstance(wl, rn.WordLists)

    # as_wordlist( missing_directory )
    with pytest.raises(OSError):
        wl = rn.WordList.as_wordlist('ahkjhaskdjfbaskjfb')
    with pytest.raises(OSError):
        wl = rn.WordList._from_directory('ahkjhaskdjfbaskjfb')  # for coverage

    # as_wordlist( dictionary )
    d = {
        'a': ['a', 'b', 'c'],
        'b': ['a', 'b', 'c'],
    }
    wl = rn.WordList.as_wordlist(d)
    assert isinstance(wl, rn.WordLists)
    assert [l.name for l in wl.lists] == list(d)
    for l in wl.lists:
        assert list(l) == d[l.name]

    # as_wordlist( bad_value )
    with pytest.raises(ValueError):
        rn.WordList.as_wordlist(5)

    # assert rn.

    


def test_wordlist_misc():
    wl = rn.WordList.as_wordlist(['a', 'b'], 'abc')
    assert wl.name and wl.name in str(wl)
    assert wl.name and wl.name in repr(wl)
    # D = {wl.name: 'hello', wl: 'hi'}
    # print(D)
    # assert len(D) == 1
    # assert D[wl.name] == 'hello'

    # as_wordlist( directory )
    wl2 = wl.copy(name='qqqqqqq')
    assert list(wl) == list(wl2)
    assert wl.name != wl2.name

    assert hash(wl) == hash(wl.name)
    assert list(wl.copy(['a','b','c'])) == ['a','b','c']

    


def test_wordlist_math():
    xs = list(map(str, range(5)))
    wl = rn.WordList(xs, 'a')

    for i in range(len(xs)):
        assert wl[i] == xs[i]
        assert wl[2:i] == xs[2:i]
        assert wl[-1-i] == xs[-1-i]

    assert list(wl) == xs
    assert len(wl) == len(xs)

    # WordList.__add__
    xs2 = list(map(str, [50, 51]))
    wl2  = wl + xs2
    wl22 = xs2 + wl
    assert not isinstance(wl22, WordList)

    assert list(wl) == xs
    assert list(wl2) == xs + xs2

    # WordList.__sub__
    wl3 = wl - xs[-2:]
    assert list(wl3) == xs[:-2]
    assert list(wl) == xs

    # WordList.__isub__
    wl -= xs[-2:]
    assert list(wl) == xs[:-2]


def test_wordlist_search():
    wl = rn.WordList(['asdf', 'asxc', 'zxcv'], 'a')
    assert wl.find('as') == []
    assert wl.find('as*') == ['asdf', 'asxc']
    assert wl.find('asd*') == ['asdf']
    assert wl.find('asdf') == ['asdf']
    assert wl.find(lambda w: w[::-1]=='fdsa') == ['asdf']

    assert list(wl.filter('as*')) == ['asdf', 'asxc']

def test_wordlist_sample():
    xs = [f'a{i}' for i in range(200)]
    wl = rn.WordList(xs, 'a')
    for _ in range(200):
        assert wl.sample() in xs
    assert len(wl.sample(40)) == 40


def test_wordlist_filter():
    xs = ['asdf', 'asxc', 'zxcv']
    wl = rn.WordList(xs, 'a')
    assert len(wl) == 3
    wl2 = wl.filter(lambda x: x.startswith('a'))
    assert len(wl2) == 2
    assert len(wl) == 3
    assert wl2 == xs[:2]

def test_wordlist_match():
    wl = rn.WordList(['a', 'b', 'c'], 'nouns/asdf')
    assert wl._get_matches('nouns')
    assert wl._get_matches('nouns/')
    assert wl._get_matches('nouns/*')
    assert wl._get_matches('nouns/asdf')

    assert not wl._get_matches('anouns')
    assert not wl._get_matches('anouns/')
    assert not wl._get_matches('anouns/*')
    assert not wl._get_matches('anouns/asdf')
    assert not wl._get_matches('nouns/asdfaaa')

    wl = rn.WordList(['a', 'b', 'c'], 'nouns/asdf', exact_match=True)
    assert not wl._get_matches('nouns')
    assert not wl._get_matches('nouns/')
    assert not wl._get_matches('nouns/*')
    assert wl._get_matches('nouns/asdf')

    assert not rn.WordList([])._matches_name(None)
    assert rn.WordList([], 'asdf/qwer/zxcv')._matches_name('qwer')


def test_wordlist_file():  # dump, lazy load
    # wl = rn.WordList.as_wordlist(os.path.join(rn.WORD_PATH, 'imsky/adjectives/colors.txt'))
    path = './pytest-wordlist.txt'
    try:
        if os.path.isfile(path): os.remove(path)
        wl = rn.WordList(['a', 'b', 'c'])
        assert not os.path.isfile(path)
        wl.dump(path)
        assert os.path.isfile(path)
        wlf = rn.WordListFile(path)
        assert list.__len__(wlf) == 0
        assert list(wlf) == list(wl)
        assert list.__len__(wlf) == len(wl)

        wlf = rn.WordListFile(path, lazy=False)
        assert list.__len__(wlf) == len(wl)

        wlf = rn.WordListFile(path)
        assert 'a' in wlf
        assert list.__len__(wlf) == len(wl)

        wlf = rn.WordListFile(path)
        assert wlf[0] == wl[0]
        assert list.__len__(wlf) == len(wl)

        wlf = rn.WordListFile(path)
        assert wlf.sample() in wl
        assert list.__len__(wlf) == len(wl)

        wlf2 = wlf.filter(lambda w: w != 'a')
        assert list.__len__(wlf2) == len(wl) - 1

        # wlf = rn.WordListFile(path)
        # assert wlf.filter()
        # assert list.__len__(wlf) == len(wl)

        assert wlf.name and wlf.name in repr(wlf)
        
    finally:
        if os.path.isfile(path): os.remove(path)

    with pytest.raises(OSError):
        rn.WordListFile("asdfasdfasdfasdfasdf")

    wl = rn.WordList.as_wordlist(os.path.join(rn.WORD_PATH, 'pokemon'))
    assert wl.name == 'pokemon'
    assert isinstance(wl, rn.WordLists)
    assert all([isinstance(l, rn.WordListFile) for l in wl.lists])

    with pytest.raises(OSError):
        rn.WordList._from_package_dir(rn.BUILTIN_LIST_LOCATION/'asdfasdfxx')


def test_wordlist_function():
    import random
    def rand(max=1): return random.random()*max
    wl = rn.WordListFunction(rand)
    assert all(0 <= int(i) <= 1 for i in wl.sample(200))
    assert list(wl) == []
    assert wl._get_matches('rand') and wl._matches_name('rand')
    assert wl._get_matches('rand(2)') and wl._matches_name('rand(2)')
    assert not wl._get_matches('random') and not wl._matches_name('random')
    # assert any(1 <= int(i) <= 2 for i in wl.sample(200))
    assert len(wl) == 0

    wl = rn.WordListFunction(rand, length=20)
    assert len(wl) == 20
    xs = [set(wl[i] for _ in range(10)) for i in range(10)]
    assert all(len(x) == 1 for x in xs)
    for w, x in zip(wl, xs):
        assert w in x
    for w, x in zip(wl[:10], xs):
        assert w in x

    



def test_wordlists():
    wl = rn.WordList.as_wordlist('imsky')
    # for l in wl.lists:
    #     assert os.path.isfile(os.path.join(
    #         rn.WORD_PATH, f'{l.name}.txt'))

    assert wl.name and wl.name in repr(wl)

    # add
    wl = rn.WordLists()
    wli = rn.WordList.as_wordlist(['a', 'b'], 'aaa')
    wl.add(wli)
    wl.add(rn.WordList.as_wordlist(['c', 'd'], 'aaa'), conflict='merge')
    wl.add(rn.WordList.as_wordlist(['x', 'y'], 'bbb'))
    assert len(wl) == 6
    assert list(wl) == ['a', 'b', 'c', 'd', 'x', 'y']

    # 
    assert list(wl.subset('aaa')) == ['a', 'b', 'c', 'd']
    assert 'd' in wl

    # __getitem__
    assert list(wl['aaa']) == ['a', 'b', 'c', 'd']
    with pytest.raises(IndexError):
        rn.WordLists()[0]
    # with pytest.raises(IndexError):
    #     rn.WordLists()[:]
    with pytest.raises(IndexError):
        rn.WordLists()[None]

    wlcp = wl[:]
    assert isinstance(wlcp, rn.WordLists)
    assert wlcp.name == wl.name
    assert len(wlcp.lists) == len(wl.lists)
    assert [l.name for l in wlcp.lists] == [l.name for l in wl.lists]
    
    assert list(wl[2:3]) == ['c']
    assert list(wl[2:5]) == ['c', 'd', 'x']
    assert list(wl[2:]) == ['c', 'd', 'x', 'y']
    assert wl[2] == 'c'
    with pytest.raises(IndexError):
        wl[100]

    wl.sample()
    wl.true_word_distribution = True
    wl.sample()

    wl = wl.filter(lambda w: w != 'a')
    assert 'a' not in set(wl.sample(100))

    # subset
    assert wl.subset() is wl
    # for l, l2 in zip(wl.subset('aaa/').lists, wl.lists):
    #     print(l)
    #     print(l2)
    # assert wl.subset('aaa/').lists == [wl.lists[:2]]
    with pytest.raises(ValueError):
        assert wl.subset('aaax/')

    # test subset with word literals
    ls = wl.subset('aaa/', 'xx,yy', accept_literals=True).lists
    print(ls)
    assert ls[0].name == 'aaa'
    # assert ls[1].name == 'aaa'
    assert list(ls[-1]) == ['xx', 'yy']

    sub = wl.subset('aaa')
    n = len(wl)
    nsub = len(sub)
    wl -= sub
    assert len(wl) == n - nsub


def test_wordlists_add():
    aaa=rn.WordList.as_wordlist(['a', 'b'], 'aaa')
    ccc=rn.WordList.as_wordlist(['c', 'd'], 'ccc')
    wl = rn.WordLists()
    wl.add(aaa)
    wl.add(aaa)
    with pytest.raises(ValueError):
        wl.add(aaa, conflict='error')
    wl.extend([aaa, ccc], conflict='merge')
    pass # add conflict, extend


def test_wordlists_getitem():
    aaa=rn.WordList.as_wordlist(['a', 'b'], 'aaa')
    ccc=rn.WordList.as_wordlist(['c', 'd'], 'ccc')
    wl = rn.WordLists([aaa, ccc])
    assert wl[:] is not wl
    assert list(wl[:]) == list(wl)
    assert wl['aaa'] is aaa
    assert wl['ccc'] is ccc
    with pytest.raises(KeyError):
        wl['bbb']

    wl = rn.WordLists()
    assert list(wl[len(wl)+1:]) == []
    assert list(wl[len(wl)+1:]) == []

    
def test_wordlists_squeeze():
    # squeeze
    wl = rn.WordLists([rn.WordList.as_wordlist(['a', 'b'], 'aaa')])
    assert isinstance(wl.squeeze(), rn.WordList)
    wl = rn.WordLists([
        rn.WordList.as_wordlist(['a', 'b'], 'aaa'), 
        rn.WordList.as_wordlist(['a', 'b'], 'aaay')])
    assert isinstance(wl.squeeze(), rn.WordLists)


@pytest.mark.parametrize("q,expected", [
    ('music', ['xxx/music', 'yyy/musicals', 'musicals/xxx', 'xxx/music_theory']),
    ('mu', ['xxx/music', 'yyy/musicals', 'xxx/music_theory', 'musicals/xxx']),
    ('mi', ['xxx/miso', 'xxx/mines', 'xxx/minerals', 'xxx/music']),
    ('mines', ['xxx/mines', 'xxx/minerals', 'xxx/miso']),
    ('mu*', ['xxx/music', 'xxx/music_theory', 'yyy/musicals', 'musicals/xxx']),
    ('xxx/music', ['xxx/music', 'musicals/xxx', 'xxx/music_theory'] ),
    ('xxx/mu', ['xxx/music', 'musicals/xxx', 'xxx/music_theory', 'xxx/mines', 'xxx/minerals']),
    ('xxx/mi', ['xxx/miso', 'xxx/mines', 'xxx/minerals', 'xxx/music', 'musicals/xxx']),
    ('xxx/mines', ['xxx/mines', 'xxx/minerals', 'xxx/miso', 'musicals/xxx']),
])
def test_wordlists_close(q,expected):
    # close_matches
    wl = rn.WordLists([
        rn.WordList.as_wordlist([], 'xxx/music'),
        rn.WordList.as_wordlist([], 'xxx/music_theory'),
        rn.WordList.as_wordlist([], 'yyy/musicals'),
        rn.WordList.as_wordlist([], 'musicals/xxx'),
        rn.WordList.as_wordlist([], 'xxx/mines'),
        rn.WordList.as_wordlist([], 'xxx/minerals'),
        rn.WordList.as_wordlist([], 'xxx/miso'),
    ])
    assert wl.close_matches(q) == expected

# def test_wordlists_math():
#     pass


# def test_wordlists_sample():
#     pass

# def test_wordlists_filter():
#     pass

# def test_wordlists_subset():
#     pass

# def test_wordlistsclose_matches():
#     pass