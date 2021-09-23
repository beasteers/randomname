from pathlib import Path

import randomname


def test_doalias():
    assert randomname.util.doalias('a/music') == 'adjectives/music'
    assert randomname.util.doalias('n/music') == 'nouns/music'
    assert randomname.util.doalias('v/music') == 'verbs/music'
    assert randomname.util.doalias('nn/music') == 'nouns/music'


def test_safepath():
    assert randomname.util.safepath('../../../some-path') == 'some-path'
    assert randomname.util.safepath('/some-path') == 'some-path'


def test_prefix():
    assert randomname.util.prefix('hi', ['a', 'b']) == ['hi/a', 'hi/b']


def test_load():
    assert randomname.util.load('v/music')


def test_close_matches():
    # test underspecified
    matches = randomname.util.close_matches('music')
    assert {Path(m) for m in matches} == {
            Path('verbs/music'),
            Path('nouns/music_theory'),
            Path('adjectives/music_theory'),
            Path('nouns/music_production'),
            Path('verbs/music_production'),
            Path('nouns/music_instruments'),
        }

    # test specific group
    for name in ['n/music', 'nouns/music']:
        matches = randomname.util.close_matches(name)
        assert {Path(m) for m in matches} == {
            Path('nouns/music_production'),
            Path('nouns/music_instruments'),
            Path('nouns/music_theory')
        }

    matches = randomname.util.close_matches('v/music')
    assert {Path(m) for m in matches} == {
        Path('verbs/music'), Path('verbs/music_production')}

    matches = randomname.util.close_matches('a/music')
    assert {Path(m) for m in matches} == {Path('adjectives/music_theory')}

    # test fnmatch
    assert set(randomname.util.close_matches('a/*usic')) == set()

    matches = randomname.util.close_matches('a/*usic*')
    assert {Path(m) for m in matches} == {Path('adjectives/music_theory')}

    # test partials/misc
    for name in ['tast', 'tasty']:
        matches = randomname.util.close_matches(name)
        assert {Path(m) for m in matches} == {
            Path('adjectives/taste'),
        }

    matches = randomname.util.close_matches('tasty', 0.4)
    assert {Path(m) for m in matches} == {
        Path('adjectives/taste'),
        Path('nouns/astronomy'),
        Path('nouns/metals')}

    matches = randomname.util.close_matches('phy')
    assert {Path(m) for m in matches} == {
        Path('adjectives/physics'),
        Path('nouns/physics'),
        Path('nouns/physics_waves'),
        Path('nouns/physics_units'),
        Path('nouns/physics_optics'),
    }
