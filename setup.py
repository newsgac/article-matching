#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('VERSION') as version_file:
    project_version = version_file.read()

setup(
    name='article-matching',
    version=project_version,
    description="Matching KB newspaper articles to metadata in the project NEWSGAC",
    long_description=readme + '\n\n',
    author="Erik Tjong Kim Sang",
    author_email='e.tjongkimsang@esciencecenter.nl',
    url='https://github.com/eriktks/article-matching',
    packages=[
        'article-matching',
    ],
    package_dir={'article-matching':
                 'article-matching'},
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='article-matching',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
