"""
Module to assist in the super-common operation of
wrapping values with prefix and suffix strings.
"""

import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .util import *
from .quoter import *

class XMLQuoter(Quoter):

    """
    A more sophisticated quoter for XML elements that manages tags,
    namespaces, and the idea that some elements may not have contents.
    """

    styles = {}         # remember named styles

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
        # Restating basic init to avoid errors of self.__getattribute__
        # that can flummox superclass instantiation
        Quoter.__init__(self)

        # take the atts kwargs for special interpretation
        kw_atts_atts = style_attribs(kwargs.pop('atts', None))

        # update remaining kwargs
        opts = self.options = self.__class__.options.push(kwargs)
        self._register_name(opts.name)

        # process flat args
        tagspec, attspec = pad(args, 2)

        # combine style attributes from kwargs and flat args
        # (in reverse order of priority)
        atts = {}
        update_style_dict(atts, kw_atts_atts)
        update_style_dict(atts, kwargs)
        update_style_dict(atts, style_attribs(attspec))
        update_style_dict(atts, style_attribs(tagspec))

        #print "args:", repr(args)
        #print "tagspec, attspec:", repr(tagspec), repr(attspec)
        #print "atts:", atts

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
        stylename = kwargs.pop('style', None)
        if stylename:
            cls = self.__class__
            return cls.styles[stylename](*args, **kwargs)
        else:
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

    styles = {}         # remember named styles

    options = XMLQuoter.options.add(
        ns       = Prohibited,
    )

    def __init__(self, *args, **kwargs):
        XMLQuoter.__init__(self, *args, **kwargs)


# HTML/XML comments need normal, not tag-based, quoters
_markup_comment = Quoter(prefix='<!--', suffix='-->', padding=1)

html = HTMLQuoter('html')
setattr(HTMLQuoter, 'comment', _markup_comment)
HTMLQuoter.styles['comment'] = _markup_comment

# Tags that don't take content. Their payload is specified in their
# tag name and attributes, if any.
_SELFCLOSING = """
    br img hr input link meta area base col command embed keygen
    param source track
""".strip().split()

for t in _SELFCLOSING:
    hq = HTMLQuoter(t, void=True)
    setattr(HTMLQuoter, t, hq)
    XMLQuoter.styles[t] = hq


xml = XMLQuoter('xml')
setattr(XMLQuoter, 'comment', _markup_comment)
XMLQuoter.styles['comment'] = _markup_comment


# Eventually working way toward a CSS box model style formatting in which there
# can be a marginleft, marginright, paddingleft, and paddingright (i.e.
# separating left and right magin/padding specs). It might even be possible
# to provide borders (top and bottom), and to reconsider prefix and suffix
# as left and right borders. Alignment of content within a cell and various
# forms of multi-line justification might also be feasible.

# With named styles being stored in the Quoter/subclass __dict__, it is
# unclear there is any benefit to having a separate styles class attribute.
# Removing it may take some extra testing changes, but would be a simplifying
# cleanup.

# Consider abstracting the "StyleSet" functionality of a group of named
# styles from the Quoter functionality. Possibly a sidecar to the the
# ``options`` module.
