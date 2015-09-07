"""
Module to assist in the super-common operation of
wrapping values with prefix and suffix strings.
"""

import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .base import QuoterBase
from .util import *
from .styleset import StyleSet


class BadStyleName(ValueError):
    pass


class Quoter(OptionsClass, QuoterBase):

    """
    A quote style. Instantiate it with the style information. Call
    it with a value to quote the value.
    """

    options = Options(
        prefix       = None,
        suffix       = None,
        pair         = Transient,
        margin       = 0,
        padding      = 0,
        encoding     = None,
    )

    def __init__(self, *args, **kwargs):
        """
        Create a quoting style.
        """
        opts = self.options = self.__class__.options.push(kwargs)
        self._interpret_args(args)

    def _interpret_args(self, args):
        """
        Consume 'flat' *args if present when object is constructed.
        Interpret them, and possibly also options already set.
        """
        opts = self.options
        if opts.pair is not Transient:
            opts.prefix, opts.suffix = halfstr(opts.pair)
            opts.pair = Transient
        if args:
            used = opts.addflat(args, ['prefix', 'suffix'])
            if 'suffix' not in used:
                opts.suffix = opts.prefix
                # this suffix = prefix behavior appropriate for flat args only

    def _whitespace(self, opts):
        """
        Compute the appropriate margin and padding strings.
        """
        pstr = ' ' * opts.padding if isinstance(opts.padding, int) else opts.padding
        mstr = ' ' * opts.margin  if isinstance(opts.margin, int)  else opts.margin
        return (pstr, mstr)

        # could extend the padding and margins with tuples to enable
        # asymmetric before/after settings

    def _output(self, parts, opts):
        """
        Given a list of string parts, concatentate them and output
        with the given encoding (if any).
        """
        outstr = ''.join(parts)
        return outstr.encode(opts.encoding) if opts.encoding else outstr

    def __call__(self, value, **kwargs):
        """
        Quote the value, according to the current options.
        """
        opts = self.options.push(kwargs)
        pstr, mstr = self._whitespace(opts)
        suffix = opts.suffix or ''
        parts = [ mstr, opts.prefix, pstr, stringify(value), pstr, suffix, mstr ]
        return self._output(parts, opts)

    def clone(self, **kwargs):
        """
        Create a new instance whose options are chained to this instance's
        options (and thence to self.__class__.options). kwargs become the
        cloned instance's overlay options.
        """
        cloned = self.__class__()
        cloned.options = self.options.push(kwargs)
        return cloned

        # NB clone takes only kwargs, not flat args, contra constructor

    but = clone


# create some default named styles

quote = StyleSet(factory=Quoter,
                 instant=False,
                 immediate=Quoter("'"))


braces   = quote._define("braces",   pair='{}')
brackets = quote._define("brackets", pair='[]')
angles   = quote._define("angles",   pair='<>')
parens   = quote._define("parens",   pair='()')
qs = single = quote._define("qs single", "'")
qd = double = quote._define("qd double", '"')
qt = triple = quote._define("qt triple", '"""')
qb = backticks = quote._define("qb backticks", "`")
qdb = doublebackticks = quote._define("qdb doublebackticks", "``")

# and some Unicode styles
anglequote = guillemet = quote._define("anglequote guillemet",
                                           pair=six.u('\u00ab\u00bb'))
chevron = quote._define("chevron",         pair=six.u('\u2039\u203a'))
curlysingle = quote._define("curlysingle", pair=six.u('\u2018\u2019'))
curlydouble = quote._define("curlydouble", pair=six.u('\u201c\u201d'))


class LambdaQuoter(Quoter):

    """
    A Quoter that uses code to decide what quotes to use, based on the value.
    """

    options = Quoter.options.add(
        func   = None,
        prefix = Prohibited,
        suffix = Prohibited,
        pair   = Prohibited,
    )

    def _interpret_args(self, args):
        """
        Consume 'flat' *args if present when object is constructed.
        Interpret them, and possibly also options already set.
        """
        if args:
            self.options.addflat(args, ['func'])

    def __call__(self, value, **kwargs):
        """
        Quote the value, based on the instance's function.
        """
        opts = self.options.push(kwargs)
        pstr, mstr = self._whitespace(opts)
        prefix, value, suffix = opts.func(value)
        parts = [mstr, prefix, pstr, stringify(value), pstr, suffix, mstr]
        return self._output(parts, opts)

lambdaq = StyleSet(
            factory=LambdaQuoter,
            instant=False,
            immediate=LambdaQuoter(lambda v: ('', 'ALL YOUR BASE ARE BELONG TO US', '')))
