from .wordlist import WordList


class LazyWordList(WordList):
    def __init__(self, value, name=None, exact_match=False, lazy=True):
        super().__init__(value, name, exact_match)
        if not lazy:
            self.load()  # not sure the best way to do lazy loading. Otherwise we don't know the length

    _loaded = False
    def load(self, reload=False):
        if not reload and self._loaded:
            return self
        self.clear()
        self._load()
        self._loaded = True
        return self

    def _load(self):
        raise NotImplementedError

    def clear(self):
        super().clear()
        self._loaded = False

    # lazy loading

    def __len__(self):
        self.load()
        return super().__len__()

    def __contains__(self, item):
        self.load()
        return super().__contains__(item)

    def __getitem__(self, key):
        self.load()
        return super().__getitem__(key)

    def __iter__(self):
        self.load()
        return super().__iter__()

    def sample(self, *a, **kw):
        self.load()
        return super().sample(*a, **kw)

    def filter(self, *a, **kw):
        self.load()
        return super().filter(*a, **kw)
