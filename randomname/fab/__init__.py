'''


https://stackoverflow.com/questions/57057039/how-to-extract-all-words-in-a-noun-food-category-in-wordnet
'''
import os
import glob
import re
import nltk
# dwnd = nltk.downloader.Downloader()
# dwnd._update_index()
# dwnd.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

import randomname


POS = {'nouns': wn.NOUN, 'verbs': wn.VERB, 'adjectives': wn.ADJ, 'adverbs': wn.ADV}
POS_INV = {v: k for k, v in POS.items()}
POS_INV['s'] = 'adjectives'

def check_topic(word, pos, *topics):
    lexs = [syn.lexname() for syn in wn.synsets(str(word), pos=POS[pos])]

    match = topics and any(
        t in syn.lexname() 
        for syn in wn.synsets(str(word), pos=POS[pos]) 
        for t in topics)
    if match:
        print(word, topics, [[t, syn.lexname()] 
        for syn in wn.synsets(str(word), pos=POS[pos]) 
        for t in topics])
        1/0
    return match


def list_lexs(pos='nouns'):
    src = os.path.join(randomname.PATH, 'wordnetdb', f'{pos}.txt')
    print("using", src)
    wl = randomname.WordListFile(src)
    seen = set()
    for w in wl:
        for syn in wn.synsets(str(w), pos=POS[pos]):
            lex = syn.lexname()
            if lex not in seen:
                print(lex)
            seen.add(lex)


def pos_by_lex(pos):
    ''''''
    src = os.path.join(randomname.PATH, 'wordnetdb', f'{pos}.txt')
    dest = os.path.join(randomname.PATH, 'wordnetdb', f'{pos}/{{}}.txt')
    print("using", src)
    wl = randomname.WordListFile(src)
    print(len(wl))

    groups = {}
    for w in wl:
        for syn in wn.synsets(str(w), pos=POS[pos]):
            lex = syn.lexname().lower().split('.', 1)[-1]
            if lex not in groups:
                print(lex)
                groups[lex] = set()
            groups[lex].add(w)

    for name, lst in groups.items():
        dest_i = dest.format(name)
        os.makedirs(os.path.dirname(dest_i), exist_ok=True)
        print(f"saving {len(lst)} words to {dest_i}")
        randomname.WordList(sorted(lst)).dump(dest_i)

def by_lex():
    for pos in POS:
        pos_by_lex(pos)


def compare(a, b, blacklist=True):
    '''Compare two wordlists and find their differences and similarities.'''
    a = set(randomname.WordLists().register(a, blacklists=blacklist))
    b = set(randomname.WordLists().register(b, blacklists=blacklist))
    
    print("In common:")
    print('\n'.join(sorted(a & b)), '\n')

    print('-'*30)

    print("In b, not a:")
    print('\n'.join(sorted(b - a)), '\n')




def cat2pos(src, name=None, minsize=10):
    '''Given a directory of words organized by theme/category, read all words, 
    get their parts of speech, and save them underneath {pos}/{category}.
    '''

    # group all words
    pos_groups = {k: {} for k in POS}
    for key, f in randomname.util.recursive_files(src).items():
        for w in randomname.WordListFile(f, key):
            for s in wn.synsets(w):
                p = pos_groups[POS_INV[s.pos()]]
                if key not in p:
                    p[key] = set()
                p[key].add(w)

    # take those groups and convert them into flat lists of wordlists
    small = []
    wls = []
    for pos, group in pos_groups.items():
        for cat, l in group.items():
            wl = randomname.WordList(sorted(l), randomname.util.join_path(pos, cat))
            if len(wl) < minsize:
                small.append(wl)
            else:
                wls.append(wl)

    # the primary word lists
    wl = randomname.WordLists(wls, name)
    for l in wl.lists:
        print(l)
        if name:
            l.dump(os.path.join(randomname.WORD_PATH, name, f'{l.name}.txt'))

    # the too small word lists
    print()
    print('too small')
    small = randomname.WordLists(small, name)
    for l in small.lists:
        print(l)
        if name:
            l.dump(os.path.join(randomname.WORD_PATH, name, '.too_small', f'{l.name}.txt'))


INVALID_PATTERN = re.compile('[\W_]+')
def _sanitize(word):
    return INVALID_PATTERN.sub('', word).lower()

def sanitize(root, dry_run=False):
    for f in glob.glob(os.path.join(root, '**/*.txt'), recursive=True):
        wl = randomname.WordListFile(f)
        wl2 = randomname.WordList([_sanitize(w) for w in wl])
        diff = {w1: w2 for w1, w2 in zip(wl, wl2) if w1 != w2}
        if diff:
            print(f)
            print(diff)
        if not dry_run:
            wl2.dump(f)


if __name__ == '__main__':
    import fire
    fire.Fire()