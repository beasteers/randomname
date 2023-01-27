'''Sanitize word lists so they don't have characters we don't want.
'''
import os
import glob
import re
import randomname


INVALID_PATTERN = re.compile('[\W_]+')
def _sanitize(word):
    return INVALID_PATTERN.sub('', word.split('(')[0]).lower()

def sanitize(root, dry_run=False):
    for f in glob.glob(os.path.join(root, '**/*.txt'), recursive=True):
        wl = randomname.WordListFile(f)
        wl2 = randomname.WordList(randomname.util.unique([_sanitize(w) for w in wl]))
        diff = {w1: w2 for w1, w2 in zip(wl, wl2) if w1 != w2}
        if diff:
            print(f)
            print(diff)
        if not dry_run:
            wl2.dump(f)


if __name__ == '__main__':
    import fire
    fire.Fire(sanitize)