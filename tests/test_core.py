import math
from pathlib import Path

import randomname
import tempfile

import unittest


class TestCode(unittest.TestCase):
    '''Tests the core module.'''

    def test_get_name(self):
        name = randomname.get_name('music_theory', 'cats').split('-', 1)
        assert len(name) > 1
        assert name[0] in randomname.util.get_groups_list('a/music_theory')
        assert name[1] in randomname.util.get_groups_list('n/cats')
        assert 'asdf' in randomname.util.get_groups_list(['n/cats', 'asdf'])

    def test_generate(self):
        name = randomname.generate('n/cats', 'a/music_theory', 'n/food').split('-', 2)
        self.assertGreater(len(name), 2)
        self.assertIn(name[0], randomname.util.get_groups_list('n/cats'))
        self.assertIn(name[1], randomname.util.get_groups_list('a/music_theory'))
        self.assertIn(name[2], randomname.util.get_groups_list('n/food'))
        self.assertIn(name[0], randomname.util.get_groups_list('n/food'))

    def test_generate_with_seed(self):
        for seed in range(0, 100, 10):
            with self.subTest(seed=seed):
                self.assertEqual(
                    [randomname.generate(seed=seed, sep='_')
                     for _ in range(20)],
                    [randomname.generate(seed=seed, sep='_')] * 20)

    def test_generated_names_are_valid_file_names(self):
        with tempfile.TemporaryDirectory() as tmp_path:
            random_names = [randomname.generate() for _ in range(10)]

            for name in random_names:
                # does not raise
                (Path(tmp_path) / name).touch()

    def test_estimate_entropy_words(self):
        estimated = randomname.estimate_entropy('n/cats', 'n/food')
        cats = randomname.util.get_groups_list('n/cats')
        food =  randomname.util.get_groups_list('n/food')
        self.assertEqual(len(cats), len(set(cats)))
        self.assertEqual(len(food), len(set(food)))
        self.assertAlmostEqual(
            estimated,
            math.log2(len(cats) * len(food)))

    def test_estimate_entropy_functions(self):
        # Default settings should be less than a bit off.
        estimated = randomname.estimate_entropy('uuid/')
        self.assertEqual(int(estimated), 121)
        # More samples should give better precision.
        estimated = randomname.estimate_entropy('uuid/', func_word_samples=100000)
        self.assertAlmostEqual(
            estimated, 122, places=1)

    def test_estimate_entropy_mixed(self):
        self.assertGreater(
            randomname.estimate_entropy(['n/cats'], ['uuid/']),
            randomname.estimate_entropy(['n/cats'], ['n/food']))

        # Splitting 50 / 50 between a word and a UUID should decrease entropy
        # compared to just using a UUID, since half the time we're sampling from
        # a low entropy distribution.
        self.assertLess(
            randomname.estimate_entropy(['n/cats'], ['uuid/', 'n/food']),
            randomname.estimate_entropy(['n/cats'], ['uuid/']))

        # The higher the likelihood of UUIDs the higher the entropy.
        self.assertLess(
            randomname.estimate_entropy(['n/cats'], ['uuid/', 'n/food']),
            randomname.estimate_entropy(['n/cats'], ['uuid/', 'uuid/', 'n/food']))

    def test_estimate_collision_probability(self):
        self.assertAlmostEqual(
            randomname.estimate_collision_probability(
                'n/cats', 'n/food', num_ids=2), 0, places=2)
        self.assertAlmostEqual(
            randomname.estimate_collision_probability(
                'n/cats', 'n/food', num_ids=100000), 1)

    def test_estimate_collision_probability_mixed(self):
        self.assertGreater(
            randomname.estimate_collision_probability(
                'n/cats', ['n/food'], num_ids=100),
            randomname.estimate_collision_probability(
                'n/cats', ['uuid/', 'n/food'], num_ids=100))
        self.assertGreater(
            randomname.estimate_collision_probability(
                'n/cats', ['uuid/', 'n/food'], num_ids=100),
            randomname.estimate_collision_probability(
                'n/cats', ['uuid/', 'uuid/', 'n/food'], num_ids=100))


if __name__ == '__main__':
    unittest.main()