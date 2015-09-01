"""
Module to assist in the super-common operation of
wrapping values with prefix and suffix strings.
"""

import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .util import *


class BadStyleName(ValueError):
    pass


QUOTER_ATTRS = set(['options', 'styles', 'set', 'settings', 'clone', 'but'])
# set of attribute names to support __getattribute__ implementation

class Quoter(OptionsClass):

    """
    A quote style. Instantiate it with the style information. Call
    it with a value to quote the value.
    """

    styles = {}         # remember named styles

    options = Options(
        prefix       = None,
        suffix       = None,
        name         = None,
        margin       = 0,
        padding      = 0,
        encoding     = None,
        style        = None,
    )

    def __init__(self, *args, **kwargs):
        """
        Create a quoting style.
        """
        opts = self.options = self.__class__.options.push(kwargs)
        self._flatargs(args)
        self._register_name(opts.name)

    def _flatargs(self, args):
        """
        Consume 'flat' *args if present when object is constructed.
        """
        if args:
            opts = self.options
            used = opts.addflat(args, ['prefix', 'suffix'])
            if 'suffix' not in used:
                opts.suffix = opts.prefix
                # this suffix = prefix behavior appropriate for flat args only

    def _register_name(self, name, cls=None):
        """
        Given a name or space-separated list of names, define styles
        based on that name, and define class attributes for that style
        name as well (as long as such a style name doesn't start with
        an underscore, which is hereby prohibuted for style names to
        avoid conflict with existing Quoter methods.)
        """
        if not name:
            return
        cls = cls or getattr(self, '__class__')
        if ' ' in name:
            names = name.split()
            self.options.name = name.replace(' ', '-')
        else:
            names = [name]

        sdict = getattr(cls, 'styles')
        for n in names:
            if not n.startswith('_'):
                sdict[name] = self
                setattr(cls, n, self)
            else:
                msg = 'Style names should not start with an underscore'
                raise BadStyleName(msg)

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
        Quote the value, with the given padding, margin, and encoding.
        """
        opts = self.options.push(kwargs)
        if opts.style:
            cls = self.__class__
            return cls.styles[opts.style](value, **kwargs)
        else:
            pstr, mstr = self._whitespace(opts)
            suffix = opts.suffix if opts.suffix is not None else opts.prefix
            parts = [ mstr, opts.prefix, pstr, stringify(value), pstr, suffix, mstr ]
            return self._output(parts, opts)

    def clone(self, **kwargs):
        """
        Create a new instance whose options are chained to this instance's
        options (and thence to self.__class__.options). kwargs become the
        cloned instance's overlay options.
        """
        cloned = self.__class__()
        name = kwargs.setdefault('name', None) # make sure there's a name
                                               # even if it's None
        cloned.options = self.options.push(kwargs)
        if name:
            cloned._register_name(name)
        return cloned


    but = clone


    def __getattribute__(self, name):
        if name in QUOTER_ATTRS or name.startswith('_'):
            return object.__getattribute__(self, name)
        cls = object.__getattribute__(self, '__class__')
        cdict = object.__getattribute__(cls, '__dict__')
        if name in cdict:
            return cdict[name]
        return cls(name, name=name)

    # Having an auto-instantiate capability through __getattribute__ is
    # great from an ease point of view, but makes the implementation
    # very tricky to get right, especially when inheritance is
    # involved.


    # should clone take same flat args as normal instanitation?
    # currently only takes kwargs

# create some default named styles (ASCII)

quote    = Quoter("'",      name= 'default')

braces   = Quoter('{', '}', name='braces')
brackets = Quoter('[', ']', name='brackets')
angles   = Quoter('<', '>', name='angles')
parens   = Quoter('(', ')', name='parens')
qs = single   = Quoter("'",      name='single qs')
qd = double   = Quoter('"',      name='double qd')
qt = triple   = Quoter('"""',    name='triple qt')
qb = backticks= Quoter("`",      name='backticks qb')
qdb = doublebackticks= Quoter("``",      name='doublebackticks qdb')

# and some Unicode styles
anglequote = guillemet = Quoter(six.u('\u00ab'), six.u('\u00bb'), name='anglequote guillemet')
curlysingle = Quoter(six.u('\u2018'), six.u('\u2019'), name='curlysingle')
curlydouble = Quoter(six.u('\u201c'), six.u('\u201d'), name='curlydouble')

# consider adding the html entity names as the names of the above quotes
# at least as aliases

# fix issue with aliased style names


class LambdaQuoter(Quoter):

    """
    A Quoter that uses code to decide what quotes to use, based on the value.
    """

    styles = {}

    options = Quoter.options.add(
        func   = None,
        prefix = Prohibited,
        suffix = Prohibited,
    )

    def _flatargs(self, args):
        """
        Consume 'flat' *args if present when object is constructed.
        """
        if args:
            self.options.addflat(args, ['func'])

    def __call__(self, value, **kwargs):
        """
        Quote the value, based on the instance's function.
        """
        opts = self.options.push(kwargs)
        if opts.style:
            cls = self.__class__
            return cls.styles[opts.style](value, **kwargs)
        else:
            pstr, mstr = self._whitespace(opts)
            prefix, value, suffix = opts.func(value)
            parts = [mstr, prefix, pstr, stringify(value), pstr, suffix, mstr]
            return self._output(parts, opts)

lambdaq = LambdaQuoter(lambda v: ('', 'ALL YOUR BASE ARE BELONG TO US', ''))
