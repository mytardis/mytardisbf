import logging
from django.apps import AppConfig
from tardis.tardis_portal.models import Schema

logger = logging.getLogger(__name__)


BFSCHEMA2 = "http://tardis.edu.au/schemas/bioformats/2"


class MyTardisBFConfig(AppConfig):
    name = 'mytardisbf'
    verbose_name = "MyTardis Bioformats"

    def ready(self):
        if not Schema.objects.filter(namespace__exact=BFSCHEMA2):
            from django.core.management import call_command
            call_command('loaddata', 'bioformats')

