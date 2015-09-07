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
used to provide simple markup language construction. (It's actually a
``StyleSet`` that knows how to create new styles on-the-fly.)

You can also access the underlying classes directly, and/or define
your own customized quoters. Your own quoters can be called as a function
would be. Or, if you give them a name, they can be called through
the ``html`` front-end, just like the pre-defined tags. For instance::

    para_e = html._define('para_e', 'p.emphatic')
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
