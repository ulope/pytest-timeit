#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

import sys
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    with codecs.open(file_path, encoding='utf-8') as f:
        return f.read()


requirements = [
    'pytest>=3.0.0'
]
if sys.version_info < (3, 4):
    requirements.append('statistics>=1.0.3.5')


setup(
    name='pytest-timeit',
    version='0.2.0',
    author='Ulrich Petri',
    author_email='python@ulo.pe',
    maintainer='Ulrich Petri',
    maintainer_email='python@ulo.pe',
    license='MIT',
    url='https://github.com/ulope/pytest-timeit',
    description='A pytest plugin to time test function runs',
    long_description=read('README.rst'),
    py_modules=['pytest_timeit'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'timeit = pytest_timeit',
        ],
    },
    zip_safe=False,
)
