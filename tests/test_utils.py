import os
import randomname


def test_doalias():
    assert randomname.util.doalias('a/music') == 'adjectives/music'
    assert randomname.util.doalias('n/music') == 'nouns/music'
    assert randomname.util.doalias('v/music') == 'verbs/music'
    assert randomname.util.doalias('nn/music') == 'nouns/music'

opj = os.path.join
PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'randomname', 'wordlists'))

def test_valid_path():
    path = opj(PATH, 'nouns', 'food') + '.txt'
    assert randomname.util.as_valid_path('../../../nouns/food') == path
    assert randomname.util.as_valid_path('nouns/food') == path
    #assert randomname.util.as_valid_path(r'nouns\food') == path


def test_prefix():
    assert randomname.util.prefix('hi', ['a', 'b']) == ['hi/a', 'hi/b']


def test_load():
    assert randomname.util.load('v/music')


def test_close_matches():
    # test underspecified
    assert set(randomname.util.close_matches('music')) == {
        'verbs/music',
        'nouns/music_theory',
        'adjectives/music_theory',
        'nouns/music_production',
        'verbs/music_production',
        'nouns/music_instruments',
    }
    # test specific group
    assert set(randomname.util.close_matches('n/music')) == {
        'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory'}
    assert set(randomname.util.close_matches('nouns/music')) == {
        'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory'}
    assert set(randomname.util.close_matches('v/music')) == {
        'verbs/music', 'verbs/music_production'}
    assert set(randomname.util.close_matches('a/music')) == {'adjectives/music_theory'}

    # test fnmatch
    assert set(randomname.util.close_matches('a/*usic')) == set()
    assert set(randomname.util.close_matches('a/*usic*')) == {'adjectives/music_theory'}

    # test partials/misc
    assert set(randomname.util.close_matches('tast')) == {'adjectives/taste'}
    assert set(randomname.util.close_matches('tasty')) == {'adjectives/taste'}
    assert set(randomname.util.close_matches('tasty', 0.4)) == {
        'adjectives/taste', 'nouns/astronomy', 'nouns/metals'}
    assert set(randomname.util.close_matches('phy')) == {
        'adjectives/physics',
        'nouns/physics',
        'nouns/physics_waves',
        'nouns/physics_units',
        'nouns/physics_optics',
    }
