import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


OMESCHEMA = "http://tardis.edu.au/schemas/ome/1"
BFSCHEMA = "http://tardis.edu.au/schemas/bioformats/2"


class MyTardisBFConfig(AppConfig):
    name = 'mytardisbf'
    verbose_name = "MyTardis Bioformats"
