
| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel| |coverage|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/quoter.svg?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/quoter

.. |version| image:: http://img.shields.io/pypi/v/quoter.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/quoter

.. |downloads| image:: http://img.shields.io/pypi/dm/quoter.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/quoter

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/quoter.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/quoter

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/quoter.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/quoter

.. |wheel| image:: https://img.shields.io/pypi/wheel/quoter.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/quoter

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/quoter

Usage
=====

::

    from quoter import *

    print single('this')       # 'this'
    print double('that')       # "that"
    print backticks('ls -l')   # `ls -l`
    print braces('curlycue')   # {curlycue}
    print braces('curlysue', padding=1)
                               # { curlysue }

And for a taste of some more advanced functionality, quoting HTML
content::

    print html.p("A para", ".focus")
    print html.img('.large', src='file.jpg')
    print html.br()
    print html.comment("content ends here")

Yields::

    <p class='focus'>A para</p>
    <img class='large' src='file.jpg'>
    <br>
    <!-- content ends here -->

This clearly goes beyond "simply wrapping some text with other text." The
output format varies widely and intelligently based on context, including
modification with CSS Selector controls, appropriately void/self-closing
elements, and specialized markup.

Finally, ``quoter`` provides a drop-dead simple, highly functional,
``join`` function::

    mylist = list("ABCD")
    print join(mylist)
    print join(mylist, sep=" | ", endcaps=braces)
    print join(mylist, sep=" | ", endcaps=braces.clone(padding=1))
    print and_join(mylist)
    print and_join(mylist, quoter=double, lastsep=" and ")

Yields::

    A, B, C, D
    {A | B | C | D}
    { A | B | C | D }
    A, B, C, and D
    "A", "B", "C" and "D"

Which shows a range of separators, separation styles (both Oxford and
non-Oxford commas), endcaps, padding, and individual item quoting. I
daresay you will not find a more flexible or configurable ``join``
function *anywhere* else in the Python world.


See `the rest of the story
at Read the Docs <http://quoter.readthedocs.org/en/latest/>`_.

