==========
mytardisbf
==========

.. image:: https://img.shields.io/travis/keithschulze/mytardisbf.svg
        :target: https://travis-ci.org/keithschulze/mytardisbf

.. image:: https://readthedocs.org/projects/mytardisbf/badge/?version=latest
        :target: https://mytardisbf.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

=========================================================
MyTardis Bioformats Preview Image and Metadata Extraction
=========================================================

MyTardisBF is an App for the [MyTardis](https://github.com/mytardis/mytardis) data management platform that provides tools for extracting preview images and metadata from common microscopy formats. The App uses the [Bioformats](http://www.openmicroscopy.org/site/products/bio-formats) library via [python-bioformats](https://github.com/CellProfiler/python-bioformats) and supports the extraction of preview images and limited metadata information for all images [supported by Bioformats](http://www.openmicroscopy.org/site/support/bio-formats5.1/supported-formats.html). Additionally, the filter supports extraction of metadata and preview images for each series in multi-series image formats like Leica LIF files.

![Screenshot](https://user-images.githubusercontent.com/503034/27212048-cdece934-52a0-11e7-8d9e-c1d85bec9e11.png)

Installation
------------

These instructions assume that you have installed and configured MyTardis. If you haven't please follow the instructions in the latest [MyTardis documentation](https://mytardis.readthedocs.io/en/develop/admin/install.html).
First install `numpy` into your MyTardis python environment::

  pip install -U numpy

Then install the latest relesase of the `mytardisbf` app::

  pip install -e git+https://github.com/keithschulze/mytardisbf.git@0.1.1#egg=mytardisbf

or for the latest development version::

  pip install -e git+https://github.com/keithschulze/mytardisbf.git#egg=mytardisbf

If you using a virtualenv, remember to activate it first.

Add the following to your MyTardis settings file eg. `/path/to/mytardis/tardis/settings.py`:

Add `mytardisbf` to your `INSTALLED_APPS`::

  INSTALLED_APPS = INSTALLED_APPS + (
      'mytardisbf',
  )

Enable the filter middleware for all actions::

  MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('tardis.tardis_portal.filters.FilterInitMiddleware',)
  FILTER_MIDDLEWARE = (("tardis.tardis_portal.filters", "FilterInitMiddleware"),)

Then add the definition for the MyTardisBF filter::

  POST_SAVE_FILTERS = [
     ("mytardisbf.filters.metadata_filter.make_filter",
     ["BioformatsMetadata", "http://tardis.edu.au/schemas/bioformats/2"]),
  ]

The Bioformats filter can be run outside of the default celery queue. To specify a different celery queue, add the following to MyTardis's `settings.py`::

  BIOFORMATS_QUEUE = "nameofqueue"

where `nameofqueue` is the name of the celery queue in which you want to run the filter.

The maximum heap space use by the JVM in each celery worker can also be configured::

  MTBF_MAX_HEAP_SIZE = "1G"

==========
Developers
==========

Get the source::

  git clone https://github.com/keithschulze/mytardisbf.git
  cd mytardisbf

To test in with MyTardis::

  # Activate your MyTardis virtualenv
  pip install -e .

Configuration of the App and Filters in MyTardis is the same as decribed above for normal Installation.

Testing
-------

Note that many of the original unittests are skipped because the test image files were large and therefore not included in this repository. Nosetests is required: `pip install nose`

In order to run unittests, you will need to enable the javabridge nosetest plugin.

Add the following to `setup.cfg`::

  [nosetests]
  with-javabridge = True
  classpath = /path/to/loci_tools.jar

Note: `loci_tools.jar` can be downloade from the [python-bioformats](https://github.com/CellProfiler/python-bioformats/blob/master/bioformats/jars/loci_tools.jar) github page or in the `python-bioformats` package inside with virtualenv where you installed it (this can be tricky to locate).
