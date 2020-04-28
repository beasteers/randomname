# randomname

Generate random ids using real human words (in english) - like docker containers or github repos.

Often, I get tired of trying to hunt down files in folders differentiated by some numeric id, and unless I need to encode a timestep into the name, I'd rather use an id that's memorable and easy to type.

The wordlists are graciously sourced from: https://github.com/imsky/wordlists

The lists include various word classes:
- `adjectives` (`a`, `adj`) - ya know those describe-y things
    - e.g. `a/colors`, `adj/shape`, `adjectives/sound`
- `nouns` (`n`, `nn`) - people, places, things dawg
    - e.g. `n/cats`, `nn/ghosts`, `nouns/wine`
- `verbs` (`v`, `vb`) - doing things
    - e.g. `v/art`, `vb/3d_graphics`
- `names` (`nm`) - things like surnames, streets, cities, etc.
    - e.g. `nm/cities`, `names/codenames`
- `ipsum` (`ip`) - misc.
    - e.g. `ip/reddit`, `ipsum/blockchain`

## Install

```bash
pip install randomname
```

## Usage
```bash
# get adj-noun:
$ randomname get
# sleek-voxel
$ randomname get
# frayed-potentiality
$ randomname get
# recursive-vector
$ randomname get
# convoluted-peninsula

# specify adj-noun sub-categories (respectively):
$ randomname get weather shopping,cats
# freezing-store

# or define your own format:
$ randomname generate adj/sound n/apex_predators
# blaring-crocodile

# use multiple categories:
$ randomname generate v/art,v/thought a/sound n/apex_predators
# doodle-silent-salamander

# mix in your own words:
$ randomname generate v/fire a/music_theory n/cats cat
# toast-adagio-angora-cat
```

## It's importable too!

```python
import randomname

# generate name using all categories
name = randomname.get_name()
# or specify a subset of the categories
name = randomname.get_name(adj=('music_theory',), noun=('cats', 'food'))
# or - you can take a bit more liberty about
name = randomname.generate(
    'v/fire', 'adj/music_theory', ('n/cats', 'n/food'))

# these contain the available groups
print('adjective categories:', randomname.ADJECTIVES)
print('noun categories:', randomname.NOUNS)

```
