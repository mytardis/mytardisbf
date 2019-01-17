#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys, os

with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [
    "numpy",
    "scipy",
    "javabridge==1.0.18",
    "python-bioformats"
]

setup_requirements = [

]

test_requirements = [

]

setup(name='mytardisbf',
      version="0.2.0",
      description="Bioformats App for MyTardis",
      long_description="""\
Bioformats App for extracting metadata and thumbnails from microscopy images\
in MyTardis""",
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mytardis bioformats',
      author='Keith Schulze',
      author_email='keith.schulze@monash.edu',
      url='https://github.com/keithschulze/mytardisbf',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      test_suite='tests',
      tests_require=test_requirements,
      setup_requires=setup_requirements,
      )
