import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class MyTardisBFConfig(AppConfig):
    name = 'mytardisbf'
    verbose_name = "MyTardis Bioformats"

    def ready(self):
        try:
            import javabridge
            import bioformats
        except ImportError as ie:
            logger.debug(ie)

        import ipdb; ipdb.set_trace()
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='4G')
