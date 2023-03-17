'''
get_groups_list
    resolve_fname
        load
            load_file
                as_valid_path
            get_matched_categories
                close_matches
                    as_valid_path
getallcategories

'''
import collections
import difflib
import glob
import fnmatch
import functools
import math
import os
import random


WORD_CLASSES = ['adjectives', 'nouns', 'verbs', 'names', 'ipsum']

# WORD_PATH = '../wordlists'
WORD_PATH = os.path.join(os.path.dirname(__file__), 'wordlists')

ALIASES = {
    'a': 'adjectives',
    'n': 'nouns',
    'v': 'verbs',
    'nm': 'names',
    'ip': 'ipsum',
    # longer, clearer abbreviations
    'adj': 'adjectives',
    'nn': 'nouns',
    'vb': 'verbs',
    'u': 'uuid',
    'uu': 'uuid',
}

import uuid
def uuid_(n=None):
    return str(uuid.uuid4())[:n and int(n)]
WORD_FUNCS = {
    'uuid': uuid_,
}

# randomname owns its own rng
rng = random.Random()
rng.seed()

def run_with_set_random_seed(method):
    '''Set randomname (pseudo-)random number generator seed to ensure reproducibility 
        before executing the method. 
        Does nothing if seed=None.'''
    def decorated_method(*args, seed=None, **kwargs):
        if seed is not None:
            rng.seed(seed)
        result = method(*args, **kwargs)
        return result
    return decorated_method


def get_groups_list(fnames):
    '''Get word lists from multiple word groups.'''
    return [x for f in as_multiple(fnames) for x in resolve_fname(f)]


def resolve_fname(fname):
    '''Detect if fname is a path or is a literal word. Replace any path
    shortcuts.'''
    return load(fname) if '/' in fname else [fname]


def load(name):
    '''Load a list of words from file. Can use glob matching to load
    multiple files.

    Examples:
    >>> load('n/music') == ['arrange', 'carol', 'compose', ... 'yodel']
    '''
    return [w for f in get_matched_categories(name) for w in load_file(f)]


@functools.lru_cache(128)
def load_file(name):
    '''Load a wordlist. Does not do any name conversion.'''
    parts = name.split('/')
    if parts[0] in WORD_FUNCS:
        return [functools.partial(WORD_FUNCS[parts[0]], *(p for p in parts[1:] if p != '*'))]

    with open(as_valid_path(name, required=True), 'r') as f:
        return [
            l for l in (l.strip() for l in f.readlines())
            if l and l[0] not in ';#']


@functools.lru_cache(128)
def get_matched_categories(name, *a, **kw):
    '''Resolve a fuzzy-matched category. Throw an error if it doesn't
    match anything.'''
    name = doalias(name)
    # glob matching
    if name.endswith('/'):
        name += '*'
    matches = [f for f in ALL_CATEGORIES if fnmatch.fnmatch(f, name)]
    if matches:
        return matches

    parts = name.split('/', 1)
    matches = ['/'.join((f, parts[1])) for f in WORD_FUNCS if fnmatch.fnmatch(f, parts[0])]
    if matches:
        return matches

    # no matches. throw nice error
    matches = close_matches(name, *a, **kw)
    raise ValueError("No matching wordlist '{}'. {}".format(
        name, 'Did you mean {}?'.format(_or_fmt(matches)) if matches else
        'No close matches found.'))


def close_matches(name, cutoff=0.65):
    '''Find close matching wordlist names.'''
    # they entered a underspecified category
    name = doalias(name)
    matches = [cat for cat in ALL_CATEGORIES if name == cat.split('/', 1)[1]]
    all_sub_categories = [c.split('/', 1)[-1] for c in ALL_CATEGORIES]

    if '/' in name:
        part0, part1 = name.split('/', 1)
        if not part0:
            part0 = '*'
        # they spelled the first part correctly
        if part0 in WORD_CLASSES:
            _ms = _get_matches(part1, AVAILABLE[part0], cutoff=cutoff)
            matches += [f for f in ('{}/{}'.format(part0, m) for m in _ms) if as_valid_path(f)]
        # they entered a misspelled category
        elif part1 in all_sub_categories:
            _ms = _get_matches(part0, [k for k in AVAILABLE if part1 in AVAILABLE[k]], cutoff=cutoff)
            matches += [f for f in ('{}/{}'.format(m, part1) for m in _ms) if as_valid_path(f)]
        # they entered a misspelled category and misspelled group
        else:
            matches += _get_matches(name, ALL_CATEGORIES, cutoff=cutoff)
        _ms = _get_matches(part0, list(WORD_FUNCS), cutoff=cutoff)
        matches += ['{}/{}'.format(m, part1) for m in _ms]
    else:
        # get sub matches
        _ms = _get_matches(name, all_sub_categories, cutoff=cutoff)
        matches += [
            '{}/{}'.format(pos, cat)
            for cat in _ms for pos in find_parts_of_speech(cat)]

    # remove duplicates
    return _ordered_unique(matches)


def _get_matches(pattern, available, **kw):
    return (
        difflib.get_close_matches(pattern, available, **kw) +
        [m for m in available if m.startswith(pattern) or fnmatch.fnmatch(m, pattern)]
    )


def _or_fmt(fnames):
    return ' or '.join("'{}'".format(f) for f in fnames)


def _ordered_unique(xs):
    unique = []
    for x in xs:
        if x not in unique:
            unique.append(x)
    return unique


def _groupby(items, func):
    groups = {}
    for x in items:
        k = func(x)
        if k not in groups:
            groups[k] = []
        groups[k].append(x)
    return x


'''

General utils

'''


def doalias(fname):
    '''Replace aliases in string.

    Examples:
    >>>
    '''
    parts = fname.split('/')
    for k, v in ALIASES.items():
        parts = [v if x == k else x for x in parts]
    return '/'.join(parts)


def as_valid_path(name, required=False):
    path = os.path.abspath(os.sep + name)
    path = os.path.relpath(path, os.path.abspath(os.sep))
    path = os.path.join(WORD_PATH, path + '.txt')
    if not os.path.isfile(path):
        if required:
            raise OSError(f"Wordlist '{name}' does not exist at location '{path}'.")
        return
    return path


def prefix(pre, xs):
    '''Prefix all items with a path prefix.'''
    return [f'{pre.rstrip("/")}/{x.lstrip("/")}' for x in as_multiple(xs)]


def choose(items, n=None):
    '''Choose one item from a list.'''
    items = as_multiple(items)
    x = rng.choice(items) if n is None else rng.choices(items, k=n)

    if isinstance(x, list):
        x = [xi() if callable(xi) else xi for xi in x]
    elif callable(x):
        x = x()
    return x

def sample_unique(func, n, *a, n_fails=50, unique=True, **kw):
    if not unique:
        return [func(*a, **kw) for _ in range(n)]
    words = set()
    for i in range(n):
        for j in range(n_fails):
            words.add(func(*a, **kw))
            if len(words) > i:
                break
        else:
            break
    return words


def as_multiple(x):
    '''Ensure a list or tuple.'''
    x = x if isinstance(x, (list, tuple)) else [x]
    return [si for s in x for si in ([s] if callable(s) else str(s).split(','))]


def find_parts_of_speech(name):
    '''Given a name, find all the groups that it belongs to.'''
    return {k for k, v in AVAILABLE.items() if name in v}


def getallcategories(d=''):
    '''Get all categories (subdirectories) from a word class (adjectives,
    nouns, etc.)'''
    d = os.path.join(WORD_PATH, d)
    path_to_all_categories = [
        os.path.relpath(os.path.splitext(f)[0], d)
        for f in glob.glob(os.path.join(d, '**/*.txt'), recursive=True)]

    # Replace OS-dependent separator with '/' which aligns with the input format
    # of the users.
    return [p.replace(os.sep, "/") for p in path_to_all_categories]


def estimate_function_entropy(fun, func_word_samples=1000):
    '''Estimate the entropy of a callable in bits by sampling.

    This estimates the entropy of the return distribution of the function, based
    on the assumption that each character is selected independently of the other
    characters in the string. This will converge on an upper bound of true
    function entropy as the number of samples goes towards infinity.

    This will do well with typical ID functions like UUID, but is going to
    coarsely overapproximate entropy for functions that have a lot of interdepent
    structure in how they generate individual characters in an ID.

    For example, consider the function:
        def my_id_funct():
          return 'bananas' if random.random() < 0.5 else 'bahamas'

    Then the true entropy of this function is 1 bit, but this estimation will
    yield 2 bits, because it will assume that the function also generates
    'bahanas', 'banamas'.

    Another issue is that if the ID function returns different length strings,
    'ban' and 'banana', then the entropy estimate will be wildly off-base, since
    it treats characters beyond the end of a string as special null characters
    <X>, which leads to impossible words like 'bana<X>a'.

    Regardless, this works for most 'typical' ID functions, in particular,
    UUIDs. It may be better to produce strict underapproximations in the future,
    to help conservatively estimate collision probabilities.
    '''
    samples = [fun() for _ in range(func_word_samples)]
    samples = [s if isinstance(s, str) else str(s) for s in samples]
    max_len = max(len(s) for s in samples)

    # Count characters at each index, using None to represent that a
    # string is shorter than the index.
    chars_per_index = [dict() for _ in range(max_len)]
    for sample in samples:
        for i in range(max_len):
            char = sample[i] if i < len(sample) else None
            chars_per_index[i].setdefault(char, 0)
            chars_per_index[i][char] += 1

    # Calculate the entropy as the sum of the entropy of each index.
    # Sum(-p(char) * log2(p(char))
    entropy = 0.0
    for i in range(max_len):
        chars_dict = chars_per_index[i]
        total = sum(chars_dict.values())
        ps = [count / total for count in chars_dict.values()]
        entropy += sum(-p * math.log2(p) for p in ps)
    return entropy


def word_list_entropy(word_list):
    '''Calculates the entropy of a list of words in bits.'''
    counts = collections.Counter(word_list)
    total = len(word_list)
    ps = [count / total for count in counts.values()]
    return sum(-p * math.log2(p) for p in ps)


def estimate_groups_list_entropy(fnames, func_word_samples=1000):
    '''Estimate the entropy in bits of the groups_list.

    The estimate is precise if no word_funcs are used in groups (e.g., 'uuid').
    If functions are used, the estimate converges on an upper bound of the true
    entropy as the number of samples goes towards infinity. We assume that
    functions generate disjoint sets of IDs, independent of the other functions,
    and disjoint from any of the wordlists. If this assumption is not true,
    then the resulting estimate will be too high.
    '''
    groups_list = get_groups_list(fnames)
    callables = [c for c in groups_list if callable(c)]
    words = [c for c in groups_list if not callable(c)]
    # Entropy is the expected surprise of a distribution, surprise
    # of x being defined as -log p(x), formally, let W be the distribution
    # over words W, then:
    #   H(W) = E_{x ~ W}[ -log p(x) ]
    # A domain is a set of possible values for x (either a wordlist
    # or the set of values returned by an ID function in our setting).
    # We assume domains to be non-overlapping and independent. This
    # assumption may well not be true, but it's going to be fine for
    # most usage scenarios. With the assumption, we can rewrite the
    # above as:
    #   H(W) = E_{D ~ Domain} E_{x ~ D} [-log p(x)]
    # The probability that a word x is drawn from a given domain D is
    # modeled by the expression p(x | D). Since we know that x is drawn
    # from D (and does not occur in other domains), we can rewrite the
    # -log p(x) = -log p(x and D) = -log (p(x | D) * p(D)). This gives us:
    #   H(W) = E_{D ~ Domain} E_{x ~ D} [-log (p(x | D) * p(D))]
    #   H(W) = E_{D ~ Domain} E_{x ~ D} [-log p(x | D) -  log(p(D))]
    #   H(W) = E_{D ~ Domain} [E_{x ~ D} [-log p(x | D)] - log(p(D))]
    # Now the inner expectation can be simplified as the entropy H(D)
    # of the distribution over domains:
    #   H(W) = E_{D ~ Domain} [ H(D) - log(p(D)) ]
    # We can distribute the expectation over the subtraction and get:
    #   H(W) = E_{D ~ Domain} [H(D)] + E_{D ~ Domain} [-log(p(D))]
    # Now the second summand is just the entropy of the distribution
    # over domains H(Domain). We call this the selector_h in the code below.
    #   H(W) = E_{D ~ Domain} [H(D)] + H(Domain)
    # For easier reading, we reorder the two summands.
    #   H(W) = H(Domain) + E_{D ~ Domain} [H(D)]
    # Expectations over finite domains can simply be computed as
    # probability-weighted sums, which gives us:
    #   H(W) = H(Domain) + Sum_{D in Domain} p(D) * H(D)
    # We have derived that the entropy the distribution of generated words
    # is equal to the entropy of the Domain selection process, which in our
    # case is simply the choice between sampling from a wordlist and sampling
    # from on of the functions, plus entropy of the selected domain weighted
    # by its selection probability, now in code:
    p_callable = 1 / len(groups_list)
    p_word = len(words) / len(groups_list)
    # This is the sum over p(D) * H(D) for callable Ds.
    weighted_h_callable = sum(
        p_callable * estimate_function_entropy(c, func_word_samples)
        for c in callables)
    # This is the sum over p(D) * H(D) for D being the wordlist.
    weighted_h_wordlist = p_word * word_list_entropy(words)
    # We can now compute the selection probabilities for each domain.
    # Typically, this will be dominated by p_word, unless there are
    # a LOT of functions in the mix.
    selector_ps = [p_callable] * len(callables) + [p_word]
    # We now use the entropy formula to calculate H(D), we guard the
    # execution of math.log2, to ensure we don't evaluate math.log2(0).
    selector_h = sum(0 if not p else -p * math.log2(p) for p in selector_ps)
    # Now by H(p)
    return selector_h + weighted_h_callable + weighted_h_wordlist


def estimate_collision_probability(entropy_bits, num_samples):
    '''Estimate the probability of a collision in a set of samples'''
    return 1 - math.exp(-num_samples *
                        (num_samples-1) / (2 ** entropy_bits))


# get all available word classes and categories.
AVAILABLE = {k: getallcategories(k) for k in WORD_CLASSES}
ALL_CATEGORIES = getallcategories()  # FIXME: redundant
# ALL_SUB_CATEGORIES = [c.split('/', 1)[-1] for c in ALL_CATEGORIES]

# expand
ADJECTIVES, NOUNS, VERBS, NAMES, IPSUM = [
    AVAILABLE[k] for k in WORD_CLASSES]



if __name__ == '__main__':
    import fire
    fire.Fire()
