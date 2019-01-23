"""
MyTardis filter class for extracting metadata from image files using Bioformats
"""
from django.conf import settings

from mytardisbf import tasks


class MetadataFilter(object):
    """MyTardis filter for extracting metadata from micrscopy image
    formats using the Bioformats library.

    Attributes
    ----------
    name: str
        Short name for schema
    schema: str
        Name of the schema to load the EXIF data into.
    """
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def __call__(self, sender, **kwargs):
        """Post save call back to invoke this filter.

        Parameters
        ----------
        sender: Model
            class of the model
        instance: model Instance
            Instance of model being saved.
        created: boolean
            Specifies whether a new record is being created.
        """
        instance = kwargs.get('instance')
        bfqueue = getattr(settings, 'BIOFORMATS_QUEUE', 'celery')
        tasks.process_meta_file_output\
            .apply_async(args=[instance.id, self.schema, False], queue=bfqueue)


def make_filter(name, schema):
    return MetadataFilter(name, schema)

make_filter.__doc__ = MetadataFilter.__doc__
