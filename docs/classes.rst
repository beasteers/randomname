
Available Wordlists
------------------------

 - `imsky`_
 - `Enchanted Learning`_
 - `Pokemon`_
 - `wordnet`_ (not loaded by default)

.. exec-code::

   import randomname
   wl = randomname.get_wordlist()
   print(wl)
   for l in wl.lists:
      print(l.name, len(l.lists), 'lists', len(l), 'words')


.. exec-code::

   import randomname
   wl = randomname.get_wordlist('wordnet')
   print(len(wl.lists), 'lists', len(wl), 'words')

imsky
^^^^^^^^^^^^^^^^^^^

Access by name: ``imsky``

Source: https://github.com/imsky/wordlists

This was the original word list and has been the default since the 
beginning of the project. 

.. exec-code::

   import randomname
   wl = randomname.get_wordlist('imsky')
   for l in wl.lists:
      print(f'{wl.name}/{l.name}:', len(l), 'words')


Enchanted Learning
^^^^^^^^^^^^^^^^^^^^^^^^^

Access by name: ``enchanted``

Source: https://www.enchantedlearning.com/wordlist/

These lists weren't originally divided by part of speech so we use `randomname/fab/categorize.py` to divide them by Part of Speech 
using ``nltk``'s ``owm-1.4`` corpus. Any words with multiple parts of speech are placed in each one.

.. exec-code::

   import randomname
   wl = randomname.get_wordlist('enchanted')
   for l in wl.lists:
      print(f'{wl.name}/{l.name}:', len(l), 'words')


Pokemon
^^^^^^^^^^^^^^^

Access by name: ``pokemon``

Source:
 - ``names`` of Pokemon: https://www.slowpoketail.com/post/pokemon-list-by-name
 - Everything else: https://bulbapedia.bulbagarden.net/

.. exec-code::

   import randomname
   wl = randomname.get_wordlist('pokemon')
   for l in wl.lists:
      print(f'{wl.name}/{l.name}:', len(l), 'words')


wordnet
^^^^^^^^^^^^^^^^^^^^

Access by name: ``wordnet``

Source: https://wordnet.princeton.edu/download/current-version

If you want a broader vocabulary, I've also pulled the dictionary used by 
wordnet (extracted from their database files). The word groupings are from 
``nltk synsets.lexname()``.

If you have a better way to get word groups from nltk please let me know!!


.. exec-code::

   import randomname
   wl = randomname.get_wordlist('wordnet')
   for l in wl.lists:
      print(f'{wl.name}/{l.name}:', len(l), 'words')

You can download the wordnet database files and run these commands to extract the words for yourself.

.. code-block:: python

   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adj | cut -d ' ' -f 5 > adjectives.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adv | cut -d ' ' -f 5 > adverbs.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.noun | cut -d ' ' -f 5 > nouns.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.verb | cut -d ' ' -f 5 > verbs.txt

.. note:: 

   this is basically the english dictionary 
   meaning it includes swears and slurs. I've included a blacklist 
   (modified from a list by CMU) to exclude some innapropriate terms.


Other word lists
^^^^^^^^^^^^^^^^^^^^^

If you have any ideas for word lists or word list organization, feel free to submit a PR!

Personally, I think it'd be fun to add some niche/nerdy categories so preference for that. 

Potential sources:
 - https://www.ldoceonline.com/browse/topics.html

Undesireable Words
^^^^^^^^^^^^^^^^^^^^^^^


You can manage your own blacklist in multiple ways:

 - Add them to your global blacklist at ``~/.randomname/blacklist``
 - Add them to a directory-specific blacklist ``./.randomname.blacklist``
 - Add them manually like this:

.. code-block:: python

   import randomname
   randomname.wordlists -= randomname.WordListFile("./my.blacklist")
   randomname.wordlists -= ['bad word']
