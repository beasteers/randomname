import randomname


def test_get_name():
    name = randomname.get_name('music_theory', 'cats').split('-', 1)
    assert len(name) > 1
    assert name[0] in randomname.wordlists.filter('a/music_theory')
    assert name[1] in randomname.wordlists.filter('n/cats')
    assert 'asdf' in randomname.wordlists.filter(['n/cats', 'asdf'])

def test_generate():
    cats = 'n/cats', 'a/music_theory', 'n/food'
    name = randomname.generate(*cats, spaces=' ').split('-', 2)
    assert len(name) == len(cats)
    lists = [randomname.wordlists.filter(c) for c in cats]
    for i, n in enumerate(name):
        assert all((n in l) == (i == j) for j, l in enumerate(lists))
