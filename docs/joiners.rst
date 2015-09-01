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

