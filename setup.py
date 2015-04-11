#!/usr/bin/env python

import os.path
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.dirname(__file__))


setup(
    name="django-states",
    version="1.6.4",
    url='https://github.com/citylive/django-states2',
    license='BSD',
    description="State machine for django models",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Jonathan Slenders, Gert van Gool, Maarten Timmerman, Steven (rh0dium)',
    author_email='jonathan.slenders@mobilevikings.com',
    packages=find_packages('.', exclude=['test_proj',]),
    #package_dir={'': 'templates/*'},
    test_suite='test_proj.runtests.main',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
