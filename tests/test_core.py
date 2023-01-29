import randomname


def test_get_wordlist():
    og = randomname.wordlists
    assert randomname.get_wordlist(None) is randomname.wordlists
    wl = randomname.WordList([])
    assert randomname.get_wordlist(wl) is wl
    assert randomname.get_wordlist('enchanted').name == 'enchanted'

    assert randomname.set_wordlist(wl) is wl
    assert randomname.get_wordlist() is wl
    assert randomname.wordlists is wl
    randomname.set_wordlist(og)
    assert randomname.wordlists is og


def test_get_name():
    name = randomname.get_name('music_theory', 'cats').split('-', 1)
    assert len(name) > 1
    assert name[0] in randomname.wordlists.subset('a/music_theory')
    assert name[1] in randomname.wordlists.subset('n/cats')
    assert 'asdf' in randomname.wordlists.subset(['n/cats', 'asdf'], accept_literals=True)

def test_generate():
    cats = 'n/cats', 'a/music_theory', 'n/food'
    name = randomname.generate(*cats, spaces=' ').split('-', 2)
    assert len(name) == len(cats)
    lists = [randomname.wordlists.subset(c) for c in cats]
    for i, n in enumerate(name):
        assert all((n in l) == (i == j) for j, l in enumerate(lists))


def test_sample():
    cats = 'n/cats'
    wl = randomname.wordlists.subset(cats)
    assert all(w for w in randomname.generate(cats, n=10))

def test_sample_names():
    cats = 'cats'
    wl = randomname.wordlists.subset(cats)
    assert all(w for w in randomname.get(cats, n=10))


def test_search():
    assert list(randomname.search('iggly*', 'pokemon/names')) == ['igglybuff']
    assert list(randomname.search('*puff', 'pokemon/names')) == ['jigglypuff', 'slurpuff']
    assert list(randomname.search('*iggly*', 'pokemon/names')) == ['igglybuff', 'jigglypuff', 'wigglytuff']


def test_available():
    wl = randomname.available('pokemon')
    assert isinstance(wl, randomname.WordLists)
    assert wl.name == 'pokemon'
    # assert all(l.name.startswith('pokemon') for l in wl.lists)
    assert not {'pokeballs', 'moves'} - set(l.name for l in wl.lists)

def test_blacklist():
    wl = randomname.get_wordlist('wordnet')
    bl = randomname.WordList.as_wordlist(randomname.BUILTIN_LIST_LOCATION / 'wordnet/.blacklist')
    assert len(bl)
    for w in bl:
        assert w not in wl

def test_main():
    import sys
    sys.argv = ['', 'get']
    randomname.main()
    sys.argv = ['', 'get', '-n', '3']
    randomname.main()

    # for coverage
    randomname._prints(lambda: {'a': 5})()