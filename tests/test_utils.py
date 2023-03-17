import os
import randomname

import unittest


PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'randomname', 'wordlists')).lower()


class TestUtils(unittest.TestCase):

    def test_doalias(self):
        self.assertEqual(randomname.util.doalias('a/music'), 'adjectives/music')
        self.assertEqual(randomname.util.doalias('n/music'), 'nouns/music')
        self.assertEqual(randomname.util.doalias('v/music'), 'verbs/music')
        self.assertEqual(randomname.util.doalias('nn/music'), 'nouns/music')


    def test_valid_path(self):
        path = os.path.join(PATH, 'nouns', 'food') + '.txt'
        self.assertEqual(randomname.util.as_valid_path('../../../nouns/food').lower(), path)
        self.assertEqual(randomname.util.as_valid_path('nouns/food').lower(), path)
        #assert randomname.util.as_valid_path(r'nouns\food').lower() == path


    def test_prefix(self):
        self.assertEqual(randomname.util.prefix('hi', ['a', 'b']), ['hi/a', 'hi/b'])


    def test_load(self):
        self.assertTrue(randomname.util.load('v/music'))


    def test_close_matches(self):
        # test underspecified
        self.assertEqual(
            set(randomname.util.close_matches('music')),
            {'verbs/music',
             'nouns/music_theory',
             'adjectives/music_theory',
             'nouns/music_production',
             'verbs/music_production',
             'nouns/music_instruments',
            })
        # test specific group
        self.assertEqual(
            set(randomname.util.close_matches('n/music')),
            {'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory'})
        self.assertEqual(
            set(randomname.util.close_matches('nouns/music')),
            {'nouns/music_production', 'nouns/music_instruments', 'nouns/music_theory'})
        self.assertEqual(
            set(randomname.util.close_matches('v/music')),
            {'verbs/music', 'verbs/music_production'})
        self.assertEqual(
            set(randomname.util.close_matches('a/music')),
            {'adjectives/music_theory'})

        # test fnmatch
        self.assertEqual(
            set(randomname.util.close_matches('a/*usic')),
            set())
        self.assertEqual(
            set(randomname.util.close_matches('a/*usic*')),
            {'adjectives/music_theory'})

        # test partials/misc
        self.assertEqual(
            set(randomname.util.close_matches('tast')),
            {'adjectives/taste'})
        self.assertEqual(
            set(randomname.util.close_matches('tasty')),
            {'adjectives/taste'})
        self.assertEqual(
            set(randomname.util.close_matches('tasty', 0.4)),
            {'adjectives/taste', 'nouns/astronomy', 'nouns/metals'})
        self.assertEqual(
            set(randomname.util.close_matches('phy')),
            {'adjectives/physics',
             'nouns/physics',
             'nouns/physics_waves',
             'nouns/physics_units',
             'nouns/physics_optics',
            })


if __name__ == '__main__':
    unittest.main()