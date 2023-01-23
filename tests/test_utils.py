import randomname


def test_doalias():
    aliases = randomname.wordlists.aliases
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
    assert randomname.util.join_words('a', 'b') == 'a-b'
    assert randomname.util.join_words('', 'b') == 'b'
    assert randomname.util.join_words('a', '') == 'a'
    assert randomname.util.join_words('a', None) == 'a'

    assert randomname.util.join_words('a a a', 'b b b') == 'a-a-a-b-b-b'


def test_close_matches():
    # test underspecified
    assert set(randomname.wordlists._close_matches('music')) == {
        'verbs/music',
        'nouns/music_theory',
        'adjectives/music_theory',
        'nouns/music_production',
        'verbs/music_production',
        'nouns/music_instruments',
    }
    # test specific group
    assert randomname.wordlists._close_matches('n/music') == [
        'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory']
    assert randomname.wordlists._close_matches('nouns/music') == [
        'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory']
    assert randomname.wordlists._close_matches('v/music') == [
        'verbs/music', 'verbs/music_production']
    assert randomname.wordlists._close_matches('a/music') == ['adjectives/music_theory']

    # test fnmatch
    assert randomname.wordlists._close_matches('a/*usic') == []
    assert randomname.wordlists._close_matches('a/*usic*') == ['adjectives/music_theory']

    # test partials/misc
    assert randomname.wordlists._close_matches('tast') == ['adjectives/taste']
    assert randomname.wordlists._close_matches('tasty') == ['adjectives/taste']
    assert randomname.wordlists._close_matches('tasty', 0.4) == [
        'adjectives/taste', 'nouns/astronomy', 'nouns/metals']
    assert set(randomname.wordlists._close_matches('phy')) == {
        'adjectives/physics',
        'nouns/physics',
        'nouns/physics_waves',
        'nouns/physics_units',
        'nouns/physics_optics',
    }
