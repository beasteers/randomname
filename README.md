# randomname

Generate random unique ids using real words - like docker containers or github repos.

Often, I get tired of trying to hunt down files in folders differentiated by some numeric id, and unless I need to encode a timestep into the name, I'd rather use an id that's memorable and easy to type.

The wordlists are graciously sourced from: https://github.com/imsky/wordlists

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

# mix in your own words (e.g. "cat"):
$ randomname generate v/fire a/music_theory n/cats cat
# toast-adagio-angora-cat
```

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

## Available
adjectives: 
> `speed`, `weather`, `shape`, `sound`, `physics`, `temperature`, `corporate_prefixes`, `complexity`, `colors`, `taste`, `quantity`, `size`, `algorithms`, `geometry`, `materials`, `construction`, `music_theory`, `appearance`, `linguistics`, `emotions`, `age`, `character`

nouns:      
> `accounting`, `fortifications`, `typography`, `spirits`, `cotton`, `car_parts`, `shopping`, `chemistry`, `seasonings`, `gaming`, `cats`, `real_estate`, `wood`, `military_navy`, `wine`, `music_production`, `sports`, `meat`, `physics`, `physics_waves`, `corporate`, `web_development`, `condiments`, `design`, `automobiles`, `metals`, `fast_food`, `radio`, `physics_units`, `military_airforce`, `3d_printing`, `3d_graphics`, `travel`, `dogs`, `houses`, `astronomy`, `buildings`, `minerals`, `startups`, `algorithms`, `fruit`, `apex_predators`, `infrastructure`, `geometry`, `set_theory`, `ghosts`, `military_army`, `music_instruments`, `filmmaking`, `birds`, `construction`, `music_theory`, `corporate_job`, `driving`, `linear_algebra`, `fish`, `coding`, `architecture`, `writing`, `phones`, `machine_learning`, `furniture`, `history`, `plants`, `cheese`, `food`, `containers`, `vcs`, `water`, `storage`, `geography`, `physics_optics`, `data_structures`, `screenwriting`, `insurance`

verbs:
> `graphics`, `movement`, `music`, `cooking`, `thought`, `military_navy`, `music_production`, `manipulation`, `sports`, `corporate`, `creation`, `destruction`, `quantity`, `radio`, `3d_graphics`, `look`, `fire`, `collection`, `programming`, `art`, `driving`, `vcs`, `communication`, `web`

ipsum:
> `corporate`, `hipster`, `blockchain`, `lorem`, `reddit`
