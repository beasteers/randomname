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


if __name__ == '__main__':
    unittest.main()