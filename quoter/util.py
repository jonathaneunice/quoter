
import sys

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


def blanknone(v):
    """
    Return a value, or empty string if it's None.
    """
    return '' if v is None else v
