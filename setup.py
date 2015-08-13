#!/usr/bin/env python

from setuptools import setup
from codecs import open
import sys

_PY26 = sys.version_info[:2] == (2, 6)
STUF = 'stuf==0.9.14' if _PY26 else 'stuf>=0.9.16'


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]


setup(
    name='quoter',
    version='1.3.5',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Simple, systematic way to quote, join, and textually wrap Python data",
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/quoter',
    license='Apache License 2.0',
    packages=['quoter'],
    setup_requires=[],
    install_requires=['six>=1.9', STUF, 'options>=1.2.2'],
    tests_require=['tox', 'pytest', 'six>=1.9'],
    test_suite="test",
    zip_safe=False,  # it really is, but this will prevent weirdness
    keywords='quote wrap prefix suffix endcap repr representation html xml join',
    classifiers=lines("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Text Processing :: Filters
        Topic :: Text Processing :: Markup
        Topic :: Text Processing :: Markup :: HTML
        Topic :: Text Processing :: Markup :: XML
    """)
)
