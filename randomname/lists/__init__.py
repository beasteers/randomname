try:
    import importlib.resources as imprc
except ImportError:  # pragma: no cover
    import importlib_resources as imprc  # pragma: no cover

import randomname
BUILTIN_LIST_LOCATION = imprc.files(randomname) / 'words'
BUILTIN_LISTS = list(BUILTIN_LIST_LOCATION.iterdir())
# print(BUILTIN_LISTS)
# print([p.name for p in BUILTIN_LISTS])

from .wordlist import WordList
from .wordlistfile import WordListFile, WordListPackageFile
from .lazywordlist import LazyWordList
from .wordlistfunction import WordListFunction
from .wordlists import WordLists