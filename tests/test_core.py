from pathlib import Path

import randomname


def test_get_name():
    name = randomname.get_name('music_theory', 'cats').split('-', 1)
    assert len(name) > 1
    assert name[0] in randomname.util.get_groups_list('a/music_theory')
    assert name[1] in randomname.util.get_groups_list('n/cats')
    assert 'asdf' in randomname.util.get_groups_list(['n/cats', 'asdf'])

def test_generate():
    name = randomname.generate('n/cats', 'a/music_theory', 'n/food').split('-', 2)
    assert len(name) > 2
    assert name[0] in randomname.util.get_groups_list('n/cats')
    assert name[1] in randomname.util.get_groups_list('a/music_theory')
    assert name[2] in randomname.util.get_groups_list('n/food')
    assert name[0] not in randomname.util.get_groups_list('n/food')

def test_generated_names_are_valid_file_names(tmp_path: Path):
    random_names = [randomname.generate() for _ in range(10)]

    for name in random_names:
        # does not raise
        (Path(tmp_path) / name).touch()
