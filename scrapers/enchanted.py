#%%
import os
from random import random
import bs4
import requests
import randomname

ROOT_URL = 'https://www.enchantedlearning.com'
PATH = os.path.join('word_dumps', 'enchanted')

def pull():
    soup = bs4.BeautifulSoup(requests.get(f'{ROOT_URL}/wordlist').content, 'html.parser')
    # right click inspect element > copy selector
    table = soup.select('p:nth-child(13) table')[0]
    links = {a.get_text(): a['href'] for a in table.select('a')}

    os.makedirs(PATH, exist_ok=True)

    # links = {'birds': '/wordlist/birds.shtml'}

    for k, url in links.items():
        name = url.split('/')[-1].rsplit('.')[0]
        soup = bs4.BeautifulSoup(requests.get(f'{ROOT_URL}{url}').content, 'html.parser')
        wl = randomname.WordList([
            w.text
            for w in soup.select('.wordlist-item')
        ], name=k)
        if wl:
            wl.dump(os.path.join(PATH, f'{name}.txt'))
        print(wl)
    process()


def process():
    import glob
    for f in glob.glob(os.path.join(PATH, '*.txt')):
        print(f)
        wl = randomname.WordListFile(f)
        wl[:] = (fix_word(w) for w in wl)
        wl.dump(f)


def fix_word(w):

    # drop notes in parentheses
    w = w.split('(')[0]
    return w.strip()


if __name__ == '__main__':
    import fire
    fire.Fire()