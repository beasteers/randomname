.. randomname documentation master file, created by
   sphinx-quickstart on Sun Jan 23 22:44:11 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

randomname
======================================

Generate random unique ids using real words - just like docker containers and github repos do it.

Often, I get tired of trying to hunt down files in folders differentiated by some numeric 
id, and unless I need to encode a timestep into the name, I'd rather use an id that's memorable 
and easy to type.

The wordlists are graciously sourced from: https://github.com/imsky/wordlists

The main commands are:

.. code-block:: bash

   # get random adjective-noun pairs

   randomname get  # generate one adjective noun pair
   randomname sample-names  # runs `randomname get` n times and ensures uniqueness

   # e.g. adjectives/colors,adjectives/geometry nouns/cats
   randomname get colors,geometry cats

   randomname sample-names colors,geometry cats


   # generate is a more general version of get, where you can specify any 
   # part of speech combo you want.

   # e.g. randomname generate verb/ adj/ noun/cats
   randomname generate  # generate one phrase, you can specify any parts of speech/wordlist
   randomname sample  # runs `randomname generate` n times and ensures uniqueness

   # e.g. verbs/music adjectives/colors nouns/cats
   randomname generate v/music a/colors n/cats

   randomname sample v/music a/colors n/cats


With ``generate`` you can also mix in literal words, or literal word lists (using commas).

.. code-block:: bash

   randomname sample underwater,land-bound n/cats cat loves a/ n/
   # land-bound-birman-cat-loves-wicker-filter
   # underwater-ginger-cat-loves-some-class
   # land-bound-bombay-cat-loves-pure-fox
   # underwater-bengal-cat-loves-convoluted-remote
   # land-bound-longhair-cat-loves-every-angora
   # underwater-bengal-cat-loves-hushed-tint
   # underwater-ginger-cat-loves-faint-holder
   # land-bound-birman-cat-loves-hasty-syntax
   # underwater-siberian-cat-loves-antique-clubhouse
   # land-bound-burmese-cat-loves-internal-exception


Here's a sample!

.. code-block:: bash

   $ randomname sample
   # local-ray
   # adjacent-poutine
   # savory-compressor
   # amortized-angle
   # humane-window
   # marked-attenuation
   # many-gothic
   # dynamic-ayu
   # insulated-antiquity
   # every-force

   # say how many you want to generate
   $ randomname sample -n 2
   # polite-observatory
   # parallel-material

generate adjective-noun pairs one-by-one like this:

.. code-block:: bash

   # get adj-noun:
   $ randomname get
   # sleek-voxel
   $ randomname get
   # frayed-potentiality
   $ randomname get
   # recursive-vector
   $ randomname get
   # convoluted-peninsula

.. You can select sub-categories for adjectives and nouns, respectively. Here 
.. we're selecting adjectives related to weather and nouns related to either 
.. shopping or cats.

.. .. code-block:: bash

..    # specify adj-noun sub-categories (respectively):
..    $ randomname get weather shopping,cats
..    # freezing-store





Installation
---------------

.. code-block:: bash

   pip install randomname


.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

   self


.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   api
   deeper
   classes


Future Work
---------------

 - 