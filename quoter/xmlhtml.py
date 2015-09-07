"""
Module to assist in the super-common operation of
wrapping values with prefix and suffix strings.
"""

import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .util import *
from .quoter import *
from .styleset import *


class XMLQuoter(Quoter):

    """
    A more sophisticated quoter for XML elements that manages tags,
    namespaces, and the idea that some elements may not have contents.
    """

    options = Quoter.options.add(
        tag      = None,
        ns       = None,
        atts     = {},
        attquote = single,
        void     = False,
        prefix   = Prohibited,
        suffix   = Prohibited,
    )

    def __init__(self, *args, **kwargs):
        """
        Create an XMLQuoter
        """
        Quoter.__init__(self)

        # take the atts kwargs for special interpretation
        kw_atts_atts = style_attribs(kwargs.pop('atts', None))

        # update remaining kwargs
        opts = self.options = self.__class__.options.push(kwargs)

        # process flat args
        tagspec, attspec = pad(args, 2)

        # combine style attributes from kwargs and flat args
        # (in reverse order of priority)
        atts = {}
        update_style_dict(atts, kw_atts_atts)
        update_style_dict(atts, kwargs)
        update_style_dict(atts, style_attribs(attspec))
        update_style_dict(atts, style_attribs(tagspec))

        # finally set the object's key values
        opts.tag = atts.pop('_tag', None) or opts.tag
        opts.atts = atts


    def _attstr(self, atts, opts):
        """
        Format an attribute dict. Uses this object's default attribute quoter.
        """
        return ' '.join([''] + ["{0}={1}".format(k, opts.attquote(v)) for k, v in atts.items()])


    def __call__(self, *args, **kwargs):
        """
        Quote a value in X/HTML style, with optional attributes.
        """

        # if not args and not opts.void:
        #    return self.clone(**kwargs)

        # take the atts kwargs for special interpretation
        kw_atts_atts = style_attribs(kwargs.pop('atts', None))

        # update remaining kwargs
        opts = self.options.push(kwargs)

        # process flat args
        if opts.void:
            spec = args[0] if args else ''
            value = None
        else:
            value, spec = pad(args, 2)

        # combine style attributes from opts, kwargs, and flat args
        # (in reverse order of priority)
        atts = {}
        update_style_dict(atts, style_attribs(opts.atts))
        update_style_dict(atts, kwargs)
        update_style_dict(atts, kw_atts_atts)
        update_style_dict(atts, style_attribs(spec))

        # if there is a local tag, let it come in force
        opts.tag = atts.pop('_tag', None) or opts.tag


        # construct the resulting attribute string
        astr = self._attstr(atts, opts) if atts else ''


        pstr, mstr = self._whitespace(opts)
        ns = opts.ns + ':' if opts.ns else ''
        if opts.void or not args:
            parts = [ mstr, '<', ns, opts.tag, astr, '>', mstr ]
        else:
            parts = [ mstr, '<', ns, opts.tag, astr, '>', pstr,
                      stringify(value),
                      pstr, '</', ns, opts.tag, '>', mstr ]
        return self._output(parts, opts)


    # could improve kwargs handling of HTMLQuoter

    # question is, should call attributes overwrite, or add to, object atts?
    # may not be a single answer - eg, in case of class especially

    # This might be case where replace is the primary option, but there's
    # an option to add (or even subtract) - say using a class Add, Plus, Subtract,
    # Minus, Relative, Rel, Delta, etc as an indicator

    # To be a full production XML quoter, might need a slightly more robust way
    # to name XML styles that include namespace names, including some sort of
    # rules for handling hyphens in the names (which cannot be in Python
    # identifiers), and perhaps for understanding namespaces (with terminating
    # colon) as part of tag specification. When a tag is auto-instantiated, it
    # could perhaps have its ns defined as part of its definition, like tag is.


class HTMLQuoter(XMLQuoter):

    """
    A more sophisticated quoter that supports attributes and void elements for HTML.
    """

    options = XMLQuoter.options.add(
        ns       = Prohibited,  # HTML doesn't have namespaces
    )

    def __init__(self, *args, **kwargs):
        XMLQuoter.__init__(self, *args, **kwargs)


# HTML/XML comments need normal, not tag-based, quoters
_markup_comment = Quoter(prefix='<!--', suffix='-->', padding=1)

html = StyleSet(
        factory = HTMLQuoter,
        instant = True,
        immediate = HTMLQuoter('html'))

html.comment = _markup_comment

# Tags that don't take content. Their payload is specified in their
# tag name and attributes, if any.
_SELFCLOSING = """
    br img hr input link meta area base col command embed keygen
    param source track
""".strip().split()

for t in _SELFCLOSING:
    html[t] = HTMLQuoter(t, void=True)


xml = StyleSet(
        factory = XMLQuoter,
        instant = True,
        immediate = XMLQuoter('xml'))

xml.comment = _markup_comment
xml.cdata = Quoter("<![CDATA[", "]]>")
xml.pcdata = Quoter("<![PCDATA[", "]]>")

# TODO: Should xml.pcdata do any auto-quoting of text handed to it?
# TODO: should there be xml.CDATA and xml.PCDATA synonyms
