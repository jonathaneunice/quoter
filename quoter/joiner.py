"""
Module to assist in the super-common operation of
joining values in sequences into strings.
"""

import re
from options import Options
from .util import *
from .quoter import Quoter
import six


class Joiner(Quoter):

    """
    A type of Quoter that deals with sequences.
    """

    styles = {}         # remember named styles

    options = Quoter.options.add(
        sep=', ',    # separator between items
        twosep=None,   # separator between items if only two
        lastsep=None,  # separator between penultimate and final item
        quoter=None,   # quoter for individual items
        endcaps=None,  # quoter for entire joined sequence
    )

    def __init__(self, *args, **kwargs):
        """
        Create a Joiner
        """
        # Restating basic init to avoid errors of self.__getattribute__
        # that can flummox superclass instantiation
        Quoter.__init__(self)

        opts = self.options = self.__class__.options.push(kwargs)
        self._register_name(opts.name)

    def __call__(self, seq, **kwargs):
        """
        Join the items of a sequence into a string. Implicitly stringifies any
        not-string values. Allows specification of the separator between items (and
        a special case for the last separator). Allows each item to be optionally
        quoted by a function, and the entire list to be optionally quoted with an
        endcaps function. A separate suffix and prefix may also be provdied.
        """
        opts = self.options.push(kwargs)

        def prep(v):
               """
               Prepare an item by stringifying and optionally quoting it.
               """
               s = stringify(v)
               return opts.quoter(s) if opts.quoter else s

        seqlist = list(seq)
        length = len(seqlist)
        if length == 0:
            core = ''
        elif length == 1:
            core = prep(seqlist[0])
        elif length == 2 and opts.twosep:
            sep = opts.twosep if opts.twosep is not None else opts.sep
            core = sep.join(prep(v) for v in seqlist)
        else:
            start = [ prep(v) for v in seqlist[:-1] ]
            final = prep(seqlist[-1])
            if opts.lastsep is None:
                opts.lastsep = opts.sep
            core = opts.lastsep.join([ opts.sep.join(start), final])
        pstr, mstr = self._whitespace(opts)
        capped = opts.endcaps(core) if opts.endcaps else core
        payload = [mstr, blanknone(opts.prefix), pstr, capped, pstr,
                         blanknone(opts.suffix), mstr]
        return self._output(payload, opts)


# FIXME: issue with named styles that have multiple styles extant

join = Joiner()

# specializations

# A and B. A, B, and C.
and_join = join.but(sep=', ', twosep=' and ', lastsep=', and ', name='and_join and')
word_join = and_join # deprecated

# A or B. A, B, or C.
or_join = join.but(sep=', ', twosep=' or ', lastsep=', or ', name='or_join or')

joinlines = join.but(sep="\n", suffix="\n", name='joinlines lines')

# TODO: Rationalize with respect to more sophisticated quoter args
# TODO: Rationalizw wrt more sophisticated quoter class structure and extensibility
# TODO: Add padding and margin, like quoter

concat = join.but(sep='', twosep='', lastsep='', name='concat')


def is_sequence(arg):
    """
    Is a list, set etc. Not a string.
    """
    if hasattr(arg, "__iter__") or hasattr(arg, "__getitem__"):
        if not hasattr(arg, "strip"):
            return True
    return False


items_options = Options(
    sep="\n",  # separator between items
    fmt="{key}: {value!r}",
    header=None,   # header for entire list
    footer=None    # footer for entire list
)


def iter_items(items):
    if hasattr(items, 'items'):  # dict or mapping
        for k, v in items.items():
            yield k, v
    else:
        for k, v in enumerate(items):
            yield k, v


def items(seq, **kwargs):
    opts = items_options.push(kwargs)

    formatted_items = [ opts.fmt.format(key=k, value=v) for k,v in iter_items(seq) ]
    items_str = opts.sep.join(formatted_items)
    if opts.header or opts.footer:
        parts = []
        if opts.header:
            parts.extend([opts.header, opts.sep])
        parts.append(items_str)
        if opts.footer:
            parts.extend([opts.sep, opts.footer])
        items_str = ''.join(parts)
    return items_str

# TODO: needs to be moved into object struture, like quoter
