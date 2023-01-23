
Builtin Wordlists
------------------------

 - `imsky`_
 - `Enchanted Learning`_
 - `Pokemon`_
 - `wordnet`_

imsky
^^^^^^^^^^^^^^^^^^^

Access by name: ``imsky``

Source: https://github.com/imsky/wordlists

This was the original word list and has been the default since the 
beginning of the project. 

.. exec-code::

   import randomname

   wordlists = randomname.get_wordlist('imsky')
   print(len(wordlists.lists))

   pos = sorted({l.name.split('/')[0] for l in randomname.wordlists.lists})
   for k in pos:
      print(k)
      wl = randomname.wordlists.filter_lists(f'{k}/')
      wl.lists.sort()
      print(wl)
      print()


Enchanted Learning
^^^^^^^^^^^^^^^^^^^^^^^^^

Access by name: ``enchanted``

Source: https://www.enchantedlearning.com/wordlist/

.. exec-code::

   import randomname

   wordlists = randomname.get_wordlist('enchanted')
   print(len(wordlists.lists))

   pos = sorted({l.name.split('/')[0] for l in wordlists.lists})
   for k in pos:
      print(k)
      wl = wordlists.filter_lists(f'{k}/')
      wl.lists.sort()
      print(wl)
      print()



Pokemon!
^^^^^^^^^^^^^^^

Access by name: ``pokemon``

Source: https://www.reddit.com/r/pokemon/comments/1qrnw8/i_made_a_few_plain_text_printer_friendly_pokemon/

Pokemon names \<3

TODO: add types, moves, towns, gym leaders?

.. exec-code::

   import randomname

   wordlists = randomname.get_wordlist('pokemon')
   print(wordlists)


wordnet
^^^^^^^^^^^^^^^^^^^^

Access by name: ``wordnet``

Source: https://wordnet.princeton.edu/download/current-version

If you want a broader vocabulary, I've also pulled the dictionary used by 
wordnet (extracted from their database files). The word groupings are from 
``nltk synsets.lexname()`` so I don't know what some of them mean (like adjectives ????).

If you have a better way to get word groups from nltk please let me know!!


.. exec-code::

   import randomname

   wordlists = randomname.get_wordlist('wordnet')
   print(len(wordlists.lists))

   pos = sorted({l.name.split('/')[0] for l in wordlists.lists})
   for k in pos:
      print(k)
      wl = wordlists.filter_lists(f'{k}/')
      wl.lists.sort()
      print(wl)
      print()

You can download the wordnet database files and run these commands to extract the words for yourself.

.. code-block:: python

   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adj | cut -d ' ' -f 5 > adjectives.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.adv | cut -d ' ' -f 5 > adverbs.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.noun | cut -d ' ' -f 5 > nouns.txt
   egrep -o "^[0-9]{8}\s[0-9]{2}\s[a-z]\s[0-9]{2}\s[a-zA-Z]*\s" data.verb | cut -d ' ' -f 5 > verbs.txt

.. note:: 

   this is basically the english dictionary 
   meaning it includes swears and slurs. I've included a blacklist 
   (modified from a list by CMU) to exclude racist, sexist, homophobic, transphobic, 
   ablist, and explicitly sexual (and genital-related) terms,
   but obviously I don't have time to scour the entire dictionary, so use at your own risk (!!) 
   and feel free to manage your own blacklist.
   And if you find more offensive words, especially racist slurs, please submit a PR to include them 
   in the blacklist. But keep in mind, I don't have much bandwidth to manage this 
   project so try not to be too anal (ha!) about words that are context-specific and can 
   be interpreted in multiple ways.


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
