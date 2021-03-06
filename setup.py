#!/usr/bin/env python

from setuptools import setup
from codecs import open


def lines(text):
    """
    Returns each non-blank line in text enclosed in a list.
    See http://pypi.python.org/pypi/textdata for more sophisticated version.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]


setup(
    name='quoter',
    version='1.6.8',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Powerful way to construct text, HTML, and XML, plus a kick-ass join",
    long_description=open('README.rst', encoding='utf-8').read(),
    url='https://bitbucket.org/jeunice/quoter',
    license='Apache License 2.0',
    packages=['quoter'],
    setup_requires=[],
    install_requires=['six>=1.10', 'options>=1.4.6'],
    tests_require=['tox', 'pytest', 'pytest-cov', 'coverage'],
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
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Text Processing :: Filters
        Topic :: Text Processing :: Markup
        Topic :: Text Processing :: Markup :: HTML
        Topic :: Text Processing :: Markup :: XML
    """)
)
