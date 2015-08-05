# MyTardis Bioformats Preview Image and Metadata Filter

MyTardisBF is an App for the [MyTardis](https://github.com/mytardis/mytardis) data management platform that provides tools for extracting preview images and metadata from common microscopy formats. The App uses the [Bioformats](http://www.openmicroscopy.org/site/products/bio-formats) library via [python-bioformats](https://github.com/CellProfiler/python-bioformats) and supports the extraction of preview images and limited metadata information for all images [supported by Bioformats](http://www.openmicroscopy.org/site/support/bio-formats5.1/supported-formats.html). Additionally, the filter supports extraction of metadata and preview images for each series in multi-series image formats like Leica LIF files.

![Screenshot](https://dl.dropboxusercontent.com/u/6648609/MyTardisBF.png)

## Installation
Install MyTardisBF app into you MyTardis python environment:

`pip install -e git+https://github.com/keithschulze/mytardisbf.git@runinqueue#egg=mytardisbf`

If you using a virtualenv, remember to activate it first.

Add the following to your MyTardis settings file eg. `/path/to/mytardis/tardis/settings.py`:

Add `mytardisbf` to your `INSTALLED_APPS`:

```
INSTALLED_APPS = INSTALLED_APPS + (
    'mytardisbf',
)
```

Enable the filter middleware for all actions:

```
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('tardis.tardis_portal.filters.FilterInitMiddleware',)
FILTER_MIDDLEWARE = (("tardis.tardis_portal.filters", "FilterInitMiddleware"),)
```

Then add the definition for the MyTardisBF filter:

```
POST_SAVE_FILTERS = [
   ("mytardisbf.filters.metadata_filter.make_filter",
   ["BioformatsMetadata", "http://tardis.edu.au/schemas/bioformats/2"]),
]
```

The Bioformats filter can be run outside of the default celery queue. To specify a different celery queue, add the following to MyTardis's `settings.py`:

```
BIOFORMATS_QUEUE = "nameofqueue"
```
where `nameofqueue` is the name of the celery queue in which you want to run the filter.

# Developers
## Get the source
```
git clone https://github.com/keithschulze/mytardisbf.git
cd mytardisbf
```

To test in with MyTardis:
```
# Activate your MyTardis virtualenv
pip install -e .
```

Configuration of the App and Filters in MyTardis is the same as decribed above for normal Installation.

## Testing
Note that many of the original unittests are skipped because the test image files were large and therefore not included in this repository. Nosetests is required: `pip install nose`

In order to run unittests, you will need to enable the javabridge nosetest plugin.

Add the following to `setup.cfg`:

```
[nosetests]
with-javabridge = True
classpath = /path/to/.virtualenvs/mytardis/lib/python2.7/site-packages/javabridge/jars/rhino-1.7R4.jar:/path/to/.virtualenvs/mytardis/lib/python2.7/site-packages/javabridge/jars/runnablequeue.jar:/path/to/.virtualenvs/mytardis/lib/python2.7/site-packages/javabridge/jars/cpython.jar:/path/to/.virtualenvs/mytardis/lib/python2.7/site-packages/bioformats/jars/loci_tools.jar
```
Note: you will need to adjust the `/path/to/.virtualenvs/mytardis` to the location of your mytardis python environment or a python environment that has the dependencies for this app.
