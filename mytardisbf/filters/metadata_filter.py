from mytardisbf import metadata
from mytardisbf.filters import filter_utils


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
        filter_utils.process_meta_file_output\
            .apply_async(args=[metadata.get_meta,
                               instance,
                               self.schema,
                               False])


def make_filter(name, schema):
    return MetadataFilter(name, schema)

make_filter.__doc__ = MetadataFilter.__doc__
