Misc.
===============


Omitting words
-------------------

If there's certain words you don't want to include, you can omit them like this:

.. code-block:: python

    import randomname

    randomname.wordlists -= randomname.WordListFile('path/to/my.blacklist')
    randomname.wordlists -= ["word-i-dont-like"]

TODO: Add a way to configure this by default? maybe package-wide/system-wide or by CLI.