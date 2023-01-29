
API
===================

Generating adjective-noun phrases
-----------------------------------

A common thing you see is people generating adjective-noun pairs. 

.. automodule:: randomname
    :members: get

.. exec-shell::
    
    randomname get

.. exec-shell::
    
    randomname get -n 5

Generating arbitrary phrases
-----------------------------------

But in reality, you can do so much more.

.. automodule:: randomname
    :members: generate

.. exec-shell::
    
    randomname generate v/ adj/ n/

.. exec-shell::
    
    randomname generate v/ adj/ n/ -n 5


Dealing with single words
-----------------------------------

.. automodule:: randomname
    :members: sample_word, search

Managing word lists
-----------------------------------

.. automodule:: randomname
    :members: get_wordlist, set_wordlist

.. exec-code::
    :hide_code:

    import randomname

    print(randomname.aliases)
