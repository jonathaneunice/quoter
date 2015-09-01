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

