# Changelog

## 0.1.3
 - added `randomname saved` (or `randomname.SavedList()`) to let you precompute the IDs in a set order and access them by index. Their values are stored in json under `~/.randomname`
 - `sample()` now guarantees unique values. Disable using `unique=False`. If `n_fails (default 50)` to draw a unique value occur in a row, then sample will return under-sampled

## 0.1.0

### core
 - rename `sample` -> `sample_words` to sample specific words from categories.
 - added `sample_names` as a `get_name` equivalent
 - changed default `sample` behavior to be the same as `sample_names`
 - added changelog (lol)

### util
 - better error message for `load_file`
 - add fuzzy matching for categories
    - `close_matches` - get matches as a list
    - `get_matched_categories` - add matches to exception
 - caching `load_file` and `get_matched_categories`
 - util as a cli - for testing
 - added util tests
