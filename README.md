# MyTardis Bioformats Preview Image and Metadata Filter

MyTardisBF is an App for the [MyTardis](https://github.com/mytardis/mytardis) data management platform that provides tools for extracting preview images and metadata from common microscopy formats. The App uses the [Bioformats](http://www.openmicroscopy.org/site/products/bio-formats) library via [python-bioformats](https://github.com/CellProfiler/python-bioformats) and supports the extraction of preview images and limited metadata information for all images [supported by Bioformats](http://www.openmicroscopy.org/site/support/bio-formats5.1/supported-formats.html). Additionally, the filter supports extraction of metadata and preview images for each series in multi-series image formats like Leica LIF files.

![Screenshot](https://dl.dropboxusercontent.com/u/6648609/MyTardisBF.png)

## Installation
Install MyTardisBF app into you MyTardis python environment:

`pip install -e git+https://github.com/keithschulze/mytardisbf.git`

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