import pytest
import randomname


def test_doalias():
    aliases = randomname.wordlists.aliases
    print(aliases)
    assert aliases('a/music') == 'adjectives/music'
    assert aliases('n/music') == 'nouns/music'
    assert aliases('v/music') == 'verbs/music'
    assert aliases('nn/music') == 'nouns/music'
    assert aliases('nouns/music') == 'nouns/music'
    assert aliases('asdf/music') == 'asdf/music'
    assert aliases('/music') == '/music'


def test_prefix():
    assert randomname.util.prefix('hi', ['a', 'b']) == ['hi/a', 'hi/b']

def test_joinpath():
    assert randomname.util.join_path('a', 'b') == 'a/b'
    assert randomname.util.join_path('', 'b') == 'b'
    assert randomname.util.join_path('a', '') == 'a'
    assert randomname.util.join_path('a', None) == 'a'


def test_joinwords():
    assert randomname.util.join_words(['a', 'b']) == 'a-b'
    assert randomname.util.join_words(['', 'b']) == 'b'
    assert randomname.util.join_words(['a', '']) == 'a'
    assert randomname.util.join_words(['a', None]) == 'a'

    assert randomname.util.join_words(['a a a', 'b b b']) == 'a-a-a-b-b-b'



def testclose_matches2():
    wl = randomname.wordlists.copy()
    # test underspecified
    assert set(wl.close_matches('music')) == {
        # 'verbs/music',
        # 'nouns/music_theory',
        # 'adjectives/music_theory',
        # 'nouns/music_production',
        # 'verbs/music_production',
        # 'nouns/music_instruments',
        'enchanted/nouns/musictheory',
        'enchanted/adjectives/musictheory',
        'imsky/verbs/music',
        'enchanted/adverbs/musictheory',
        'enchanted/verbs/musictheory',
    }
        
@pytest.mark.parametrize("q,expected", [
    ('n/music', ['enchanted/nouns/musictheory', 'imsky/nouns/music_theory', 'imsky/nouns/music_production', 'imsky/nouns/music_instruments', 'enchanted/nouns/musicalinstruments']),
    ('nouns/music', ['enchanted/nouns/musictheory', 'imsky/nouns/music_theory', 'imsky/nouns/music_production', 'imsky/nouns/music_instruments', 'enchanted/nouns/musicalinstruments']),
    ('v/music', ['imsky/verbs/music', 'enchanted/verbs/musictheory', 'imsky/verbs/music_production', 'enchanted/verbs/musicalinstruments', 'enchanted/adverbs/musictheory']),
    ('a/music', ['enchanted/adjectives/musictheory', 'imsky/adjectives/music_theory', 'enchanted/adverbs/musictheory', 'imsky/verbs/music', 'enchanted/adjectives/adjectives']),
    ('a/*usic', ['imsky/verbs/music']),
    ('a/*usic*', ['imsky/adjectives/music_theory', 'enchanted/adjectives/musictheory', 'enchanted/adverbs/musictheory', 'imsky/nouns/music_production', 'imsky/nouns/music_instruments']),
    ('tast', ['imsky/adjectives/taste', 'imsky/names/states/usa', 'imsky/names/states/city_states', 'imsky/names/states/switzerland', 'imsky/names/states/canada']),
    ('tasty', ['imsky/adjectives/taste', 'imsky/nouns/astronomy', 'enchanted/adjectives/astronomy', 'enchanted/nouns/astronomy', 'enchanted/verbs/astronomy']),
    ('phy', ['imsky/adjectives/physics', 'imsky/nouns/physics', 'imsky/nouns/physics_waves', 'imsky/nouns/physics_units', 'imsky/nouns/physics_optics']),
])
def test_close_matches(q,expected):
    wl = randomname.wordlists
    print(wl.close_matches(q))
    assert wl.close_matches(q)==expected
    # # test specific group
    # assert wl.close_matches('n/music') == ['enchanted/nouns/musictheory', 'imsky/nouns/music_theory', 'imsky/nouns/music_production', 'imsky/nouns/music_instruments', 'enchanted/nouns/musicalinstruments']
    # assert wl.close_matches('nouns/music') == ['enchanted/nouns/musictheory', 'imsky/nouns/music_theory', 'imsky/nouns/music_production', 'imsky/nouns/music_instruments', 'enchanted/nouns/musicalinstruments']
    # assert wl.close_matches('v/music') == ['imsky/verbs/music', 'enchanted/verbs/musictheory', 'imsky/verbs/music_production', 'enchanted/verbs/musicalinstruments', 'enchanted/adverbs/musictheory']
    # print(wl.close_matches('a/music'))
    # assert wl.close_matches('a/music') == ['enchanted/adjectives/musictheory', 'imsky/adjectives/music_theory', 'enchanted/adverbs/musictheory', 'enchanted/adjectives/adjectives', 'enchanted/adverbs/adjectives']

    # # test fnmatch
    # assert wl.close_matches('a/*usic') == ['imsky/verbs/music']
    # assert wl.close_matches('a/*usic*') == ['enchanted/adjectives/musictheory', 'imsky/adjectives/music_theory', 'enchanted/adverbs/musictheory', 'enchanted/nouns/musicalinstruments', 'enchanted/nouns/musictheory']

    # # test partials/misc
    # assert wl.close_matches('tast') == ['imsky/adjectives/taste', 'wordnet/nouns/state', 'enchanted/nouns/metals', 'enchanted/nouns/castle', 'enchanted/verbs/metals']
    # assert wl.close_matches('tasty') == ['imsky/adjectives/taste', 'wordnet/nouns/state', 'enchanted/adjectives/astronomy', 'enchanted/nouns/astronomy', 'enchanted/verbs/astronomy']
    # # assert wl.close_matches('tasty', cutoff=0.4) == ['imsky/adjectives/taste', 'wordnet/nouns/state', 'enchanted/adjectives/astronomy', 'enchanted/nouns/astronomy', 'enchanted/verbs/astronomy']
    # assert set(wl.close_matches('phy')) == {
    #     'imsky/adjectives/physics',
    #     'imsky/nouns/physics',
    #     'imsky/nouns/physics_waves',
    #     'imsky/nouns/physics_units',
    #     'imsky/nouns/physics_optics',
    # }

def test_aliases():
    assert isinstance(randomname.util.Aliases({}), randomname.util.Aliases)
    assert isinstance(randomname.util.Aliases.as_alias({}), randomname.util.Aliases)
    assert isinstance(randomname.util.Aliases.as_alias(randomname.aliases), randomname.util.Aliases)
    a=randomname.util.Aliases({})
    assert 'a' not in a
    a.update({'a':  'asdf'})
    assert 'a' in a
    with pytest.raises(ValueError):
        a.update({'a':  'asdfa'})


def test_choose():
    xs = [1, 2, 3]
    assert randomname.util.choose(xs) in xs
    assert not set(randomname.util.choose(xs, n=3)) - set(xs)