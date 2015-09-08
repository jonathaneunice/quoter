Markdown
========

An experimental Markdown formatter has been added. It is quite simple at
present, supporting both span:

========  ================
Function  Markdown Span
--------  ----------------
``md.i``  \*italics\*
``md.b``  \*\*bold\*\*
``md.a``  anchor, aka link
========  ================

and some block functions:

==========  ================
Function    Markdown Block
----------  ----------------
``md.h``    heading
``md.h1``   heading level 1
``md.h2``   heading level 2
...         ...
``md.h6``   heading level 6
``md.p``    paragraph
``md.hr``   horizontal rule
``md.doc``  document
==========  ================

All functions are accessed through the ``md`` style set.

List, image, blockquote, and code-block formatting are next steps. At this
demonstration stage, the goal is to stretch the ``quoter`` use-case and
prove/harden its extension mechanisms, which it is already doing. A much
more extensive block-oriented quoting mechanism is in the works to flesh out
Markdown construction. Stay tuned for more extensive functions and
documentation.
