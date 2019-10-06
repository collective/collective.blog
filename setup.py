# -*- coding: utf-8 -*-
"""Installer for the collective.blog package."""

from setuptools import find_packages
from setuptools import setup
import io

def read(filename):
    with io.open(filename, 'r', encoding='utf-8') as fp:
        return fp.read()

long_description = (
    read('README.rst') +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    read('CONTRIBUTORS.rst') +
    '\n' +
    read('CHANGES.rst') +
    '\n')


setup(
    name='collective.blog',
    version='1.0a1',
    description="A blog addon for Plone 5.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Rene Jochum',
    author_email='rene@jochums.at',
    url='https://pypi.python.org/pypi/collective.blog',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'plone.app.dexterity',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
