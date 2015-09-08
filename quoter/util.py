
import sys
import re
from itertools import chain

_PY3 = sys.version_info[0] > 2
if _PY3:
    basestring = unicode = str


def is_string(v):
    return isinstance(v, basestring)


def stringify(v):
    """
    Return a string. If it's already a string, just return that. Otherwise,
    stringify it. Under Python 3, this makes perfect sense. Under Python 2,
    if the string contains Unicode octets (e.g. UTF-8 bytes, because it's
    really a byte string pretending to be a full string), casting to unicode
    isn't safe. Solution: Use only for Unicode strings.
    """
    return v if isinstance(v, basestring) else unicode(v)


def halfstr(s):
    """
    Split the given string, returning each half in a list.
    """
    length = len(s)
    half = length // 2
    if half * 2 != length:
        raise ValueError('string {0!r} not of even length'.format(s))
    return [s[:half], s[half:]]


def listing(l):
    """
    Return a list from either None, an iterable, or a whitespace-separated
    string listing.
    """
    if not l:
        return []
    return l.strip().split() if isinstance(l, basestring) else list(l)


def is_sequence(arg):
    """
    Is a list, set etc. Not a string.
    """
    if hasattr(arg, "__iter__") or hasattr(arg, "__getitem__"):
        if not hasattr(arg, "strip"):
            return True
    return False


def blanknone(v):
    """
    Return a value, or empty string if it's None.
    """
    return '' if v is None else v


def pad(seq, n, fillvalue=None):
    """
    You want a sequence at least n items long, say for an unpacking
    operation. You might not have n items. This will right-pad your
    sequence into one of the desired length, using your
    desired fillvalue (by default, None).
    """

    length = len(seq)
    if length == n:
        return seq
    else:
        needed = n - length
        return seq + type(seq)([fillvalue] * needed)

    # itertools equivalent:
    # return chain(iterable, repeat(fillvalue, n-len(iterable)))


def parse_css_selector(spec):
    """
    Parse a CSS-style selector (similar to what jQuery and CSS use).
    Returns an dict with tag_, id, and class, and other key, value
    fields.
    """
    if spec is None:
        return {}

    # use regular expressions to parse the selector spec
    tagnames = re.findall(r'^(\w+)',      spec)
    classes  = re.findall(r'\.([\w\-]+)', spec)
    ids      = re.findall(r'\#([\w\-]+)', spec)
    attrs    = re.findall(r'\[([\w-]+=[^]]*)\]', spec)

    # make some basic assertions
    assert len(tagnames) <= 1
    assert len(ids) <= 1

    # construct the result dict
    atts = {}
    if ids:
        atts['id'] = ids[0]
    if classes:
        atts['class'] = ' '.join(classes)
    if tagnames:
        atts['_tag'] = tagnames[0]
    for a in attrs:
        k, v = a.split('=')
        atts[k] = v
    return atts


def style_attribs(spec):
    """
    If spec is a dictionary, assume it's the one we want. Else,
    parse it.
    """
    if spec is None:
        return {}
    elif isinstance(spec, dict):
        return spec
    else:
        return parse_css_selector(spec)


def combine_classes(c1=None, c2=None):
    c1list = (c1 or '').strip().split()
    c2list = (c2 or '').strip().split()

    if not (c1list or c2list):
        return None
    classes = []
    seen = set()
    for c in chain(c1list, c2list):
        if c not in seen:
            classes.append(c)
            seen.add(c)
    return ' '.join(classes)


def update_style_dict(d, other, reverse_class=True):
    """
    Update one style dict d, with the other style dict.
    Very like a dictionary update, except that the class attribute
    can be multi-valued and additive, not replaced.

    reverse_class, if True, means to process the other's
    class value (if any) before the receiving dictionary's.
    This may seem an odd, even wrong, choice. It's actually
    the right choice in the case one is applying a series of
    updates and wishes the last update to be the higest
    priority, over-rides all others update (but still have its
    class names to appear first in the list). If you don't like
    this choice, set it to False and no harm done. Either way
    is proper CSS.
    """
    if other is None or len(other) == 0: # nothing to merge; quick exit
        return
    dclass = d.get('class')
    oclass = other.get('class')
    d.update(other)
    if dclass or oclass:
        clslist = [oclass, dclass] if reverse_class else [dclass, oclass]
        d['class'] = combine_classes(*clslist)
