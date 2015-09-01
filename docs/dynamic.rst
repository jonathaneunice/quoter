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

