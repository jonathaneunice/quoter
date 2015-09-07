

from options import attrs
import sys
from inspect import getmembers, ismethod
from .base import QuoterBase
from .util import listing


class StyleSet(object):

    """
    Container for named styles.
    """

    def __init__(self, factory=None, instant=False, immediate=None,
                       promote=None):
        self._factory = factory
        self._instant = instant
        self._immediate = immediate
        self._styles = {}
        if immediate:
            self._promote_methods(promote)

    def _promote_methods(self, other_methods):
        """
        If this ``StyleSet`` logically stands in for / proxies an immediately
        callable function/object (e.g. ``join``), there are cases when
        calls to this instance's attributes such as ``clone``, ``but``, and
        ``fork`` should actually be calls on the prototype. This method
        sets up that correspondence / forwarding arrangement.

        :param list|str other_methods: List (or whitespace separated string listing)
            of methods to explicitly promote/proxy to the ``self._immediate`` prototype.
        """
        prototype = self._immediate
        methods = set(k for k, v in getmembers(prototype, predicate=ismethod)
                                 if not k.startswith('_'))
        if other_methods:
            methods.update(listing(other_methods))
        for m in methods:
            self.__dict__[m] = getattr(prototype, m)

        # is explicit promotion even required?

    def __getitem__(self, name):
        """
        Support for bracket indexing the style name.
        """
        return self._styles[name]

    def __setitem__(self, name, value):
        """
        Support for bracket indexing the style name when assigning.
        """
        self._styles[name] = value

    def __getattr__(self, name):
        """
        Support for attribute getting the style name. This is the core of
        style auto-generation. If an attribute / style exists, it's just
        handed back. But if it isn't, a closure is generated that, when
        called, will use the factory to create the style, and then immediately
        install the named style.
        """

        style = self._styles.get(name)
        if style:
            return style
        else:
            if self._instant:
                f = self._styles[name] = self._factory(name)
                return f
            else:
                raise ValueError("style {0} not yet defined".format(name))
                # f = self._styles[name] = self._factory(*args, **kwargs)
                # return f

                # FIXME: this one probably requires the linkback strategy
                # TODO: or declare this alternate call style dead

    def __setattr__(self, name, value):
        """
        Support for attribute setting the style name.
        """
        if name.startswith("_"):
            self.__dict__[name] = value
        else:
            self._styles[name] = value

    def _define(self, names, *args, **kwargs):
        """
        Callable version of style defnition.
        Returns value if you want to use it in an assigment.

        :param str names: One or more names (aliases) for the style,
            whitespace separated.
        :param *args: Variable arguments passed to the style factory. If first
            arg is a ``Quoter`` instance, this is your style. Otherwise,
            send all the args and kwargs to the factory.
        :param **kwargs: Keyword arguments passed to the style factory
        :returns: The defined style
        """
        if len(args) == 1 and isinstance(args[0], QuoterBase):
            s = args[0]
        else:
            s = self._factory(*args, **kwargs)
        for name in names.strip().split():
            self._styles[name] = s
        return s

    def __call__(self, *args, **kwargs):
        """
        Handle case styleset is called in immediate mode.
        """
        if self._immediate:
            return self._immediate(*args, **kwargs)
        else:
            raise KeyError("No immediate call specified.")

    def __repr__(self):
        clsname = self.__class__.__name__
        return "{0}({1})".format(clsname, attrs(self._styles))
