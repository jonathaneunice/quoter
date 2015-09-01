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

