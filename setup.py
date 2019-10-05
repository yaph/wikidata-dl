#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from wikidata_dl import __author__, __email__, __version__


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['python-dateutil', 'requests', 'wptools']

setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author=__author__,
    author_email=__email__,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Download data from Wikidata based on input SPARQL query.',
    entry_points={
        'console_scripts': [
            'wikidata-dl=wikidata_dl.cli:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='wikidata, download, dl, command line, cli, sparql',
    name='wikidata_dl',
    packages=find_packages(include=['wikidata_dl', 'wikidata_dl.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/yaph/wikidata-dl',
    version=__version__,
    zip_safe=False,
)