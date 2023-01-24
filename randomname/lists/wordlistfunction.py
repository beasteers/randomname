from .wordlist import WordList
from ..util import sample_unique


class WordListFunction(WordList):
    '''A word list that gets sampled one-by-one from a function.
    
    .. code-block:: python

        import random
        def myuniqueid(x=100):
            return 'myid-{}'.format(random.randint(x))
        
        # prepare the wordlist function
        lst = WordListFunction(myuniqueid)

        # myuniqueid is not run until sample is called
        assert lst.sample().startswith('myid-'), 'this should sample an id'
        assert len(lst.sample(3)) == 3, 'this should sample 3 ids'

    '''
    def __init__(self, func, name=None, length=1000, *a, **kw):
        self.func = func
        super().__init__([None]*length, name or func.__name__, *a, **kw)

    def __iter__(self):
        for x in super().__iter__():
            if x is not None:
                yield x

    def __getitem__(self, index):
        if isinstance(index, slice):
            # sample any values requested by the slice
            xs = self[index] = [
                self.sample() if x is None else x
                for x in super().__getitem__(index)
            ]
            return xs
        x = super().__getitem__(index)
        if x is None:
            self[index] = x = self.sample()
        return x

    def sample(self, n=None, unique=False, **kw):
        return sample_unique(self.func, n, unique=unique, **kw)

    def match(self, pattern):
        parts = pattern.split('/', 1)
        if self.name == parts[0]:
            return '/'.join([self.name] + parts[1:])

