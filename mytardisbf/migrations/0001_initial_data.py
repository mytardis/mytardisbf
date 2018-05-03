# -*- coding: utf-8 -*-

from django.db import migrations
from tardis.tardis_portal.models import (
    Schema,
    ParameterName,
    DatafileParameter,
    DatafileParameterSet
)
from mytardisbf.apps import (
    OMESCHEMA,
    BFSCHEMA
)

def forward_func(apps, schema_editor):
    """Create mytardisbf schemas and parameternames"""
    db_alias = schema_editor.connection.alias

    ome_schema, _ = Schema.objects\
        .using(db_alias)\
        .update_or_create(
            name="OME Metadata",
            namespace="http://tardis.edu.au/schemas/bioformats/1",
            subtype=None,
            hidden=True,
            type=3,
            immutable=True,
            defaults={
                'namespace': OMESCHEMA
            }
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="ome",
            data_type=5,
            is_searchable=False,
            choices="",
            comparison_type=1,
            full_name="OME Metadata",
            units="xml",
            order=1,
            immutable=True,
            schema=ome_schema,
            defaults={
                "full_name": "OMEXML Metadata"
            }
        )

    series_schema, _ = Schema.objects\
        .using(db_alias)\
        .update_or_create(
            name="Series Metadata",
            namespace=BFSCHEMA,
            subtype="",
            hidden=False,
            type=3,
            immutable=True
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="id",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=8,
            full_name="ID",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema,
            defaults={
                "is_searchable": False
            }
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="name",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=8,
            full_name="Name",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="type",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=8,
            full_name="Pixel Type",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema,
            defaults={
                "name": "pixel_type"
            }
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="dimensionorder",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=8,
            full_name="Dimension Order",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="sizex",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="SizeX",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="sizey",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="SizeY",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="sizeZ",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="SizeZ",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="sizec",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="SizeC",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="sizet",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="SizeT",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="physicalsizex",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Voxel Size X",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="physicalsizey",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Voxel Size Y",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="physicalsizez",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Voxel Size Z",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="timeincrement",
            data_type=1,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Time Increment",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="excitationwavelength",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Excitation Wavelength",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="samplesperpixel",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Samples per Pixel",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="emissionwavelength",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Emission Wavelength",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="pinholesize",
            data_type=2,
            is_searchable=True,
            choices="",
            comparison_type=1,
            full_name="Pinhole Size",
            units="",
            order=9999,
            immutable=True,
            schema=series_schema
        )

    ParameterName.objects\
        .using(db_alias)\
        .update_or_create(
            name="previewImage",
            data_type=5,
            is_searchable=False,
            choices="",
            comparison_type=1,
            full_name="Preview",
            units="image",
            order=1,
            immutable=True,
            schema=series_schema,
            defaults={
                "name": "preview_image"
            }
        )


def reverse_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    ome_schema = Schema.objects\
        .using(db_alias)\
        .get(namespace=OMESCHEMA)

    ome_pn = ParameterName.objects\
        .using(db_alias)\
        .get(schema=ome_schema)

    DatafileParameter.objects\
        .using(db_alias)\
        .filter(name=ome_pn)\
        .delete()

    DatafileParameterSet.objects\
        .using(db_alias)\
        .filter(schema=ome_schema)\
        .delete()

    ome_pn.delete()
    ome_schema.delete()

    bf_schema = Schema.objects\
        .using(db_alias)\
        .get(namespace=BFSCHEMA)

    bf_param_names = [
        "id", "name", "pixel_type", "dimensionorder", "sizex", "sizey", "sizez",
        "sizec", "sizet", "physicalsizex", "physicalsizey", "physicalsizez",
        "timeincrement", "excitationwavelength", "samplesperpixel",
        "emissionwavelength", "pinholesize", "preview_image"
    ]

    def delete_param_names(param_name_str):
        pn = ParameterName.objects\
            .using(db_alias)\
            .get(schema=bf_schema, name=param_name_str)

        DatafileParameter.objects\
            .using(db_alias)\
            .filter(name=pn)\
            .delete()

        pn.delete()

    [delete_param_names(pn) for pn in bf_param_names]

    DatafileParameterSet.objects\
        .using(db_alias)\
        .filter(schema=bf_schema)\
        .delete()

    bf_schema.delete()


class Migration(migrations.Migration):
    """MyTardis Schema and ParameterName migrations"""
    dependencies = [
        ("tardis_portal", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func),
    ]
