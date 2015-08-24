

Cloning and Setting
===================

``Quoter`` parameters can be changed (set) in real time.::

    bars = Quoter('|')
    print bars('x')                    # |x|
    bars.set(prefix='||', suffix='||')
    print bars('x')                    # ||x||
    bars.set(padding=1)
    print bars('x')                    # || x ||

And ``Quoter`` instances you like can be cloned, optionally with several
options changed in the clone::

    bart = bars.clone(prefix=']', suffix='[')
    assert bart('x') == '] x ['

.. warning::
   ``Quoter`` instances can be cloned and modified, but this feature is
   not yet operational for the more complex ``HTMLQuoter`` and ``XMLQuoter``
   types discussed below.

Formatting and Encoding
=======================

The Devil, as they say, is in the details. We often don't just want quote
marks wrapped around values. We also want those values set apart from
the rest of the text. ``quoter`` supports this with ``padding`` and ``margin``
settings patterned on the `CSS box model <http://www.w3.org/TR/CSS2/box.html>`_.
In CSS, moving out from content one finds padding, a border, and then a margin.
Padding can be thought of as an internal margin, and
the prefix and suffix strings like the border. With that in mind::

    print braces('this')                      # '{this}'
    print braces('this', padding=1)           # '{ this }'
    print braces('this', margin=1)            # ' {this} '
    print braces('this', padding=1, margin=1) # ' { this } '

If desired, the ``padding`` and ``margin`` can be given explicitly, as
strings. If given as integers, they are interpreted as a
number of spaces.

One can also define the ``encoding`` used for each call, per instance, or
globally. If some of your quote symbols use Unicode characters, yet your output
medium doesn't support them directly, this is an easy fix. E.g.::

    Quoter.options.encoding = 'utf-8'
    print curlydouble('something something')

Now ``curlydouble`` will output UTF-8 bytes. But in general, this is not a
great idea; you should work in Unicode strings in Python, encoding or
decoding only at the time of input and output, not as each piece of content
is constructed.

Shortcuts
=========

One often sees very long function calls and expressions as text parts are being
assembled. In order to reduce this problem, ``quoter`` defines aliases for
``single``, ``double``, and ``triple`` quoting, as well as ``backticks``, and
double backticks::

    from quoter import qs, qd, qt, qb, qdb

    print qs('one'), qd('two'), qt('three'), qb('and'), qdb('four')
    # 'one' "two" """three""" `and` ``four``

You can, of course, define your own aliases as well, and/or redefine existing
styles. If, for example, you like ``braces`` but wish it added a padding space
by default, it's simple to redefine::

    braces = Quoter('{', '}', padding=1, name='braces')
    print braces('braces plus spaces!')  # '{ braces plus spaces! }'

You could still get the no-padding variation with::

    print braces('no space braces', padding=0) # '{no space braces}'

Clean Imports
=============

As an organizational assist, quoters are available as
named attributes of a pre-defined ``quote`` object. For those
who like strict, minimalist imports, this permits
``from quoter import quote`` without loss of generality. For example::

    from quoter import quote

    quote.double('test')    # "test"
    quote.braces('test')    # {test}
    # ...and so on...

Each of these can also serve like an instance of an enumerated type,
specifying for a later time what kind of quoting you'd like. Then,
at the time that quoter is needed, it can simply be called. E.g.::

    preferred_quoting = quote.brackets

    ...

    print preferred_quoting(data)

Or you could use something very short, like ``q``.

HTML
====

Quoting does not need to be a simple matter of string concatenation.
It can involve sophisticated on-the-fly decisions based on content
and context.

For example, there is an extended quoting mode designed for XML and HTML
construction. Instead of prefix and suffix strings, ``XMLQuoter`` and
``HTMLQuoter`` classes build valid HTML out of tag names and "CSS selector"
style specifications (similar to those used by `jQuery
<http://jquery.com>`_). This is a considerable help in Python, which defines
and/or reserves some of the attribute names most used in HTML (e.g.
``class`` and ``id``). Using the CSS selector style neatly gets around this
annoyance--and is more compact and more consistent with modern web
development idioms to boot.::

    from quoter import *

    print html.p('this is great!', {'class':'emphatic'})
    print html.p('this is great!', '.spastic')
    print html.p('First para!', '#first')

Yields:

    <p class='emphatic'>this is great!</p>
    <p class='spastic'>this is great!</p>
    <p id='first'>First para!</p>

Note that the order in which attributes appear is not guaranteed. They're
stored in ``dict`` objects, which have different orderings on different versions
of Python. This generally isn't a problem, in that ordering isn't significant
in HTML. It can, however, make string-based testing more annoying.

The following CSS selectors are understood:

===========  ========================
CSS Spec     Result X/HTML
===========  ========================
tag          <tag>
#ident       id="ident"
.classname   class="classname"
[key=value]  key="value"
===========  ========================

Note that with the exception of tagnames and ids, multiple setters
are possible in the same CSS spec. So ``p#one.main.special[lang=en]``
defines ``<p id='one' class='main special' lang='en'>``.

HTML quoting also understands that some elements are "void" or
"self-closing," meaning they do not need closing tags (and in some cases,
not even content). So for example::

    >>> print html.br()
    <br>

    >>> print html.img('.big', src='afile')
    <img class='big' src='afile'>

The ``html`` object for ``HTMLQuoter`` (or corresponding ``xml`` for
``XMLQuoter``) is a convenient front-end that can be immediately
used to provide simple markup language construction.

You can also access the underlying classes directly, and/or define
your own customized quoters. Your own quoters can be called as a function
would be. Or, if you give them a name, they can be called through
the ``html`` front-end, just like the pre-defined tags. For instance::

    para_e = HTMLQuoter('p.emphatic', name='para_e')
    print para_e('this is great!')
    print html.para_e('this is great?', '.question')
    print html.img('.large', src='somefile')
    print html.br()

Yields::

    <p class='emphatic'>this is great!</p>
    <p class='question emphatic'>this is great?</p>
    <img class='large' src='somefile'>
    <br>

``HTMLQuoter`` quotes attributes by default with single quotes. If you
prefer double quotes, you may set them when the element is defined::

    div = HTMLQuoter('div', attquote=double)

.. note:: Some output may show HTML and XML elements in a different order
    that described in the documentation. This is because Python ``dict``
    data structures in which keyword arguments are stored are expressly
    unordered. In practice, their order is implementation dependent, and
    varies based on whether you're running on Python 2, Python 3, or
    PyPy. ``quoter`` always produces correct output, but the ordering
    may be subtly different from the order suggested by the source code.
    If this variance bothers you, please join me in lobbying for dictionary
    ordering (``OrderedDict``) to become the standard behavior for kwargs
    in future versions of Python.

XML
===

``XMLQuoter`` with its ``xml`` front-end is a similar quoter with markup
intelligence. It offers
one additional attribute beyond ``HTMLQuoter``:
``ns`` for namespaces. Thus::

    item = XMLQuoter(tag='item', ns='inv', name='item inv_item')
    print item('an item')
    print xml.item('another')
    print xml.inv_item('yet another')
    print xml.thing('something')
    print xml.special('else entirely', '#unique')

yields::

    <inv:item>an item</inv:item>
    <inv:item>another</inv:item>
    <inv:item>yet another</inv:item>
    <thing>something</thing>
    <special id='unique'>else entirely</special>

Note: ``item`` was given two names. Multiple aliases are supported.
While the ``item`` object carries its namespace specification through its
different invocations, the calls to non-``item`` quoters nave no persistent
namespace. Finally, that the CSS specification language heavily used in
HTML is present and available for XML, though its use may be less common.

In general, ``xml.tagname`` auto-generates quoters just like
``html.tagname`` does on first use. There are also pre-defined utility
methods such as ``html.comment()`` and ``xml.comment()`` for commenting
purposes.

Named Styles
============

Quoting via the functional API or the attribute-accessed front-ends
(``quote``, ``lambdaq``, ``html``, and ``xml``) is probably the easiest way to go. But
there's one more way. If you provide the name of a defined style via the
``style`` attribute, that's the style you get. So while
``quote('something')`` gives you single quotes by default (``'something'``),
if you invoke it as ``quote('something', style='double')``, you get double
quoting as though you had used ``quote.double(...)``, ``double(...)``, or
``qd(...)``. This even works through named front.ends;
``quote.braces('something', style='double')`` still gets you
``"something"``. If you don't want to be confused by such double-bucky
forms, don't use them. The best use-case for named styles is probably when
you don't know how something will be quoted (or what tag it will use, in the
HTML or XML case), but that decision is made dynamically. Then
``style=desired_style`` makes good sense.

Style names are stored in the class of the quoter. So all ``Quoter``
instances share the same named styles, as do ``HTMLQuoter``, ``XMLQuoter``,
and ``LambdaQuoter``.

Dynamic Quoters
===============

``XMLQuoter`` and ``HTMLQuoter`` show that it's straightforward to define
``Quoters`` that don't just concatenate text, but that examine it and
provide dynamic rewriting on the fly.

``LambdaQuoter`` is a further generalization of this idea. It allows generic
formatting to be done by a user-provided function. For example, in finance,
one often wants to present numbers with a special formatting::

    from quoter import LambdaQuoter

    f = lambda v: ('(', abs(v), ')') if v < 0 else ('', v, '')
    financial = LambdaQuoter(f)
    print financial(-3)            # (3)
    print financial(45)            # 45

    password = LambdaQuoter(lambda v: ('', 'x' * len(v), ''))
    print password('secret!')      # xxxxxxx

    wf = lambda v:  ('**', v, '**') if v < 0 else ('', v, '')
    warning = LambdaQuoter(wf, name='warning')
    print warning(12)              # 12
    print warning(-99)             # **-99**

The trick is instantiating ``LambdaQuoter`` with a callable (e.g. ``lambda``
expression or even a full function) that accepts one value and returns a
tuple of three values: the quote prefix, the value (possibly rewritten), and
the suffix. The rewriting mechanism can be entirely general, doing truncation,
column padding, content obscuring, hashing, or...just anything.

``LambdaQuoter`` named instances are accessed through the ``lambdaq``
front-end (because ``lambda`` is a reserved word). Given the code above,
``lambdaq.warning`` is active, for example.

``LambdaQuoter`` is an edge case, arcing over towards being a general
formatting function. That has the virtue of providing a consistent mechanism
for tactical output transformation with built-in margin and padding support.
It's also able to encapsulate complex quoting / representation decisions
that would otherwise muck up "business logic," making representation code
much more unit-testable. But, one might argue that such full transformations
are "a bridge too far" for a quoting module. So use the dynamic component
of``quoter``, or not, as you see fit.

Markdown
========

An experimental Markdown formatter has been added. It is quite simple at
present, supporting just ``i`` (italics), ``b`` (bold), ``a`` (anchor, or
link), ``p`` (paragraph), and ``doc`` (document) functions.

List, heading, image, blockquote, and code-block formatting are next steps.
At this demonstration stage, the goal is to stretch the ``quoter`` use-case
and prove/harden its extension mechanisms, which it is already doing. Stay
tuned for more extensive functions and documentation.

Joiners
=======

``Joiner`` is a type of ``Quoter`` that combines sequences. The simplest
invocation ``join(mylist)`` is identical to ``', '.join(mylist)``. But
of course it doesn't stop there. The ``sep`` parameter determines what
string is placed between each list item. But the separator need not be
uniform. For the common (and linguistically important) case where there are
two items in list, the ``twosep`` parameter provides an alternate value.
The final separator can be defined via the ``lastsep`` parameter, permitting
proper `Oxford commas <https://en.wikipedia.org/wiki/Serial_comma>`_, or
if you prefer, a non-Oxford heathen style. The standard ``prefix``, ``suffix``,
``margin`` and ``padding`` parameters are available. Finally, individual
sequence items can be formatted (``quoter``) and the entire "core" of
joined material can be wrapped by an ``endcap`` quoter.

Some examples::

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

It's a bit of a historical accident that both the ``prefix``/``suffix``
pair and ``endcap`` are available, as they accomplish the same goal.
If an ``endcap`` quoter is used, note that any desired padding (spaces
inside the endcaps) must be provided by the endcapper, as it operates
earlier than, and in conflict with, the application of normal padding. E.g.::

    print join(mylist, sep=" | ", endcaps=braces.but(padding=1))
    print join(mylist, sep=" | ", prefix="{", suffix="}", padding=1)

Do the same thing. But mixing and matching the two styles may not give you
what you wanted.

Various defined ``Joiner`` objects may be of use:: ``and_join``, ``or_join``,
``joinlines``, and ``concat``.

Notes
=====

* ``quoter`` provides simple transformations that could be alternatively
  implemented as a series of small functions. The problem is that such
  "little functions" tend to be constantly re-implemented, in different
  ways, and spread through many programs. That need to constantly
  re-implement such common and straightforward text formatting has led me to
  re-think how software should format text. ``quoter`` is one facet of a
  project to systematize higher-level formatting operations. See `say
  <http://pypi.python.org/pypi/say>`_ and `show
  <http://pypi.python.org/pypi/show>`_ for other parts of the larger effort.

* ``quoter`` is also a test case for `options
  <http://pypi.python.org/pypi/options>`_, a module that supports flexible
  option handling. In fact, it is one of ``options`` most extensive test
  cases, in terms of subclassing and dealing with named styles.

* In the future, additional quoting styles such as ones for Markdown or RST
  format styles might appear. It's not hard to subclass ``Quoter`` for new
  languages.

* You might look at some of the modules for ANSI-coloring text such as
  `ansicolors <https://pypi.python.org/pypi/ansicolors>`_ as being
  special cases of the ``quoter`` idea.  While ``quoter`` doesn't
  provide this specific kind of wrapping, it's in-line with the mission.

* Automated multi-version testing managed with the wonderful
  `pytest <http://pypi.python.org/pypi/pytest>`_,
  `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <http://pypi.python.org/pypi/coverage>`_,
  and `tox <http://pypi.python.org/pypi/tox>`_.
  Continuous integration testing
  with `Travis-CI <https://travis-ci.org/jonathaneunice/textdata>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

  Successfully packaged for, and
  tested against, most late-model versions of Python: 2.7, 3.2, 3.3,
  3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
  2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

* Support for Python 2.6 is questionable. It does build, test, and work
  under many configurations, but there is a 2.6 installability failure of
  recent versions of the ``stuf`` module underlying the ``options`` module
  on which ``quoter`` relies. Installing an old-enough version of ``stuf``
  to not fail on Python 2.6 is tricky. I've submitted a patch to the
  developer of ``stuf``, but as yet it hasn't been acted upon. So for now,
  unless someone indicates 2.6 support
  is critical to them, I'm inclined to just let 2.6 slip away.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes your comments
  and suggestions.
