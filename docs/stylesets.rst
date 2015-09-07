StyleSets
=========

As an organizational assist, quoters are available as
named attributes of a pre-defined ``quote`` object. For those
who like strict, minimalist imports, this permits
``from quoter import quote`` without loss of generality. For example::

    from quoter import quote

    quote.double('test')    # "test"
    quote.braces('test')    # {test}
    # ...and so on...

``quote`` is is a ``StyleSet``--a group of related named quoters (i.e.
"quoting styles") conveniently packaged through attributes of a single
object.

Visiting the Factory
--------------------

Each ``StyleSet`` has a factory function for creating new
styles; in the case of ``quote``
the factory is the ``Quoter`` class. You can use the ``_define`` method if
you like to create new members::

    colon = quote._define('colon', ':')
    assert colon('this') == quote.colon('this') == ':this:'

The assignement to a standalone name ``colon`` here is optional;
you could just always refer to ``quote.colon`` after the definition
if you wish.

You may even call a ``StyleSet`` in immediate mode::

    print quote("super")   # "'super'"

To define your own set of named styles::

    cq = StyleSet(factory=Quoter,
                  immediate=Quoter(':'))

    cq._define("two", Quoter('::'))

Now::

    print cq('this')         # ':this:'
    print cq.two('this')     # '::this::'
