
Introduction
============

``quoter`` provides a simple, powerful, systematic way do accomplish
one of the most common low-level operations in Python programming:
combing strings and data objects into other strings. For example::

    from quoter import *

    print single('this')       # 'this'
    print double('that')       # "that"
    print backticks('ls -l')   # `ls -l`
    print braces('curlycue')   # {curlycue}
    print braces('curlysue', padding=1)
                               # { curlysue }

Cute...but way too simple to be useful, right? Fair enough. Any of
those could have been programmed with a simple utility function.

Let's try something more complicated, where the output has to be
intelligently based on context. Here's a taste of quoting some HTML
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
output format varies widely, correctly interpreting CSS Selector-based
controls, using void/self-closing elements where needed, and specialized
markup. The HTML quoter and its companion XML quoter are competitive in
power and simplicity with bespoke markup-generating packages.

Finally, ``quoter`` provides a drop-dead simple, highly functional,
``join`` function::

    mylist = list("ABCD")
    print join(mylist)
    print join(mylist, sep=" | ", endcaps=braces)
    print join(mylist, sep=" | ", endcaps=braces.but(padding=1))
    print and_join(mylist)
    print and_join(mylist[:2])
    print and_join(mylist[:3])
    print and_join(mylist, quoter=double, lastsep=" and ")

Yields::

    A, B, C, D
    {A | B | C | D}
    { A | B | C | D }
    A and B
    A, B, and C
    A, B, C, and D
    "A", "B", "C" and "D"

Which shows a range of separators, separation styles (both Oxford and
non-Oxford commas), endcaps, padding, and individual item quoting. I
daresay you will not find a more flexible or configurable ``join``
function *anywhere* else, in
any programming language, at any price.

And if you like any particular style of formatting, make it your own::

    >>> my_join = join.but(sep=" | ", endcaps=braces.but(padding=1))
    >>> print my_join(mylist)
    { A | B | C | D }

Now you have a convenient specialized formatter to your own specifications.

Discussion
==========

Programs stringify and quote values all the time. They wrap both native
strings and the string representation of other values in all manner of
surrounding text. Single quotes. Double quotes. Curly quotes. Backticks.
Separating whitespace. Unicode symbols. HTML or XML markup. *Et
cetera.*

There are a *lot* of ways to do this text formatting and wrapping. For
example::

    value = 'something'
    print '{x}'.replace('x', value)             # {something}
    print "'{0}'".format(value)                 # 'value'
    print "'" + value + "'"                     # 'value'
    print "{0}{1}{2}".format('"', value, '"')   # "value"
    print ''.join(['"', value, '"'])            # "value"

But for such a simple, common task as wrapping values in surrounding text,
these look pretty ugly, low-level, and dense. Writing them out, it's easy to
mistype a character here or there, or to forget some of the gotchas. Say
you're formatting values, some of which are strings, but others are integers
or other primitive types. Instant ``TypeError``! Only strings can be
directly concatenated with strings in Python.

The repetitive, *ad hoc* nature of textual quoting and wrapping is tiresome
and error-prone. It's never more so than when constructing multi-level
quoted strings, such as Unix command line arguments, SQL commands, or HTML
attributes.

``quoter`` provides a clean, consistent, higher-level alternative. It also
provides a mechanism to pre-define your own quoting styles that can then be
easily reused.

We Can Do Better
================

Unlike native Python concatenation operators, ``quoter`` isn't flustered if
you give it non-string data. It knows you want a string output, so it
auto-stringifies non-string values::

    assert brackets(12) == '[12]'
    assert braces(4.4) == '{4.4}'
    assert double(None) == '"None"'
    assert single(False) == "'False'"


.. |laquo| unicode:: 0xAB .. left angle quote
    :rtrim:
.. |raquo| unicode:: 0xBB .. right angle quote
    :ltrim:
.. |lsquo| unicode:: 0x2018 .. left angle quote
    :rtrim:
.. |rsquo| unicode:: 0x2019 .. right angle quote
    :ltrim:
.. |ldquo| unicode:: 0x201C .. left angle quote
    :rtrim:
.. |rdquo| unicode:: 0x201D .. right angle quote
    :ltrim:

The module pre-defines callable ``Quoters`` for a handful of the most
common quoting styles:

 *  ``braces``  {example}
 *  ``brackets`` [example]
 *  ``angles`` <example>
 *  ``parens`` (example)
 *  ``double`` "example"
 *  ``single`` 'example'
 *  ``backticks`` \`example\`
 *  ``anglequote`` |laquo| example |raquo|
 *   ``curlysingle`` |lsquo| example |rsquo|
 *   ``curlydouble`` |ldquo| example |rdquo|

But there are a *huge* number of ways you might want to wrap or quote text.
Even considering just "quotation marks," there are `well over a dozen
<http://en.wikipedia.org/wiki/Quotation_mark_glyphs>`_. There are also
`numerous bracketing symbols in common use
<http://en.wikipedia.org/wiki/Bracket>`_. That's to say nothing of the
constructs seen in markup, programming, and templating languages. So
``quoter`` couldn't possibly provide a default option for every possible
quoting style. Instead, it provides a general-purpose mechanism for defining
your own::

    from quoter import Quoter

    bars = Quoter('|')
    print bars('x')                    # |x|

    plus = Quoter('+','')
    print plus('x')                    # +x

    para = Quoter('<p>', '</p>')
    print para('this is a paragraph')  # <p>this is a paragraph</p>
                                       # NB simple text quoting - see below
                                       # for higher-end HTML handling

    variable = Quoter('${', '}')
    print variable('x')                # ${x}

Note that ``bars`` is specified with just one symbol. If only one is given,
the prefix and suffix are considered to be identical. If you really only want
a prefix or a suffix, and not both, then instantiate the ``Quoter`` with two, one
of which is an empty string, as in ``plus`` above.

In most cases, it's cleaner and more efficient to define a style, but
there's nothing preventing you from an on-the-fly usage::

    print Quoter('+[ ', ' ]+')('castle')   # +[ castle ]+


