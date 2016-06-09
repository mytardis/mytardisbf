from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='mytardisbf',
      version=version,
      description="Bioformats App for MyTardis",
      long_description="""\
Bioformats App for extracting metadata and thumbnails from microscopy images\
in MyTardis""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mytardis bioformats',
      author='Keith Schulze',
      author_email='keith.schulze@monash.edu',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'numpy>=1.9',
          'scipy>=0.15',
          'javabridge>=1.0',
          'python-bioformats>=1.0,<1.0.7'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
