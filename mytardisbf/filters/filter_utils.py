import logging
import os
import bioformats
import javabridge
from bioformats import log4j
from django.conf import settings
from celery.task import task
from tardis.tardis_portal.models import Schema, DatafileParameterSet
from tardis.tardis_portal.models import ParameterName, DatafileParameter
from tardis.tardis_portal.models import DataFileObject

logger = logging.getLogger(__name__)
started = False


def delete_old_parameterset(ps):
    """ Remove a ParameterSet and all associated DatafileParameters

    Parameters
    ----------
    ps: ParameterSet
        A ParameterSet instance to remove
    """
    df_params = DatafileParameter.objects.get(parameterset=ps)
    [dfp.delete() for dfp in df_params]
    ps.delete()


def save_parameters(schema, param_set, params):
    """ Save a given set of parameters as DatafileParameters.

    Parameters
    ----------
    schema: tardis.tardis_portal.models.Schema
        Schema that describes the parameter names.
    param_set: tardis.tardis_portal.models.DatafileParameterSet
        Parameterset that these parameters are to be associated with.
    params: dict
        Dictionary with ParameterNames as keys and the Parameters as values.
        Parameters (values) can be singular strings/numerics or a list of
        strings/numeric. If it's a list, each element will be saved as a
        new DatafileParameter.

    Returns
    -------
    None
    """
    def savep(paramk, paramv):
        param_name = ParameterName.objects.get(schema__id=schema.id,
                                               name=paramk)
        dfp = DatafileParameter(parameterset=param_set, name=param_name)
        if paramv != "":
            if param_name.isNumeric():
                dfp.numerical_value = paramv
            else:
                dfp.string_value = paramv
            dfp.save()

    for paramk, paramv in params.iteritems():
        if isinstance(paramv, list):
            [savep(paramk, v) for v in paramv]
        else:
            savep(paramk, paramv)


@task(name="mytardisbf.filters.tardis_util.process_meta_file_output",
      ignore_result=True)
def process_meta_file_output(func, df, schema_name, overwrite=False, **kwargs):
    """Extract metadata from a Datafile using a provided function and save the
    outputs as DatafileParameters. This function differs from process_meta in
    that it generates an output directory in the metadata store and passes it
    to the metadata processing func so that outputs (e.g., preview images or
    metadata files) can be saved.

    Parameters
    ----------
    func: Function
        Function to extract metadata from a file. Function must have
        input_file_path and output_path as arguments e.g.:
        def meta_proc(input_file_path, output_path, **kwargs):
            ...
        It must return a dict containing ParameterNames as keys and the
        Parameters to be saved as values. Parameters (values) can be singular
        strings/numerics or a list of strings/numeric. If it's a list, each
        element will be saved as a new DatafileParameter.
    df: tardis.tardis_portal.models.Datafile
        Datafile instance to process.
    schema_name: str
        Names of schema which describes ParameterNames
    add: Boolean (default: False)
        Specifies whether or not to add to an existing Parameterset for this
        Datafile rather that overwriting or exiting.
    overwrite: Boolean (default: False)
        Specifies whether to overwrite any exisiting parametersets for
        this datafile.


    Returns
    -------
    None
    """
    # import ipdb; ipdb.set_trace()
    # Need to start a JVM in each thread
    global started
    if not started:
        logger.debug("Starting a new JVM")
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='4G',
                            run_headless=True)
        started = True

    try:
        javabridge.attach()
        log4j.basic_config()
        schema = Schema.objects.get(namespace__exact=schema_name)
        if DatafileParameterSet.objects\
                .filter(schema=schema, datafile=df).exists():
            if overwrite:
                psets = DatafileParameterSet.objects.get(schema=schema,
                                                         datafile=df)
                logger.warning("Overwriting parametersets for %s"
                               % df.filename)
                [delete_old_parameterset(ps) for ps in psets]
            else:
                logger.warning("Parametersets for %s already exist."
                               % df.filename)
                return

        dfo = DataFileObject.objects.filter(datafile__id=df.id,
                                            verified=True).first()
        input_file_path = dfo.get_full_path()

        output_rel_path = os.path.join(
                    os.path.dirname(input_file_path),
                    str(df.id))
        output_path = os.path.join(
            settings.METADATA_STORE_PATH, output_rel_path)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        logger.debug("Processing file: %s" % input_file_path)
        metadata_params = func(input_file_path, output_path, **kwargs)
        if not metadata_params:
            logger.debug("No metadata to save")
            return

        for sm in metadata_params:
            ps = DatafileParameterSet(schema=schema, datafile=df)
            ps.save()

            logger.debug("Saving parameters for: %s" % input_file_path)
            save_parameters(schema, ps, sm)
    except Exception, e:
        logger.debug(e)
    finally:
        javabridge.detach()


@task(name="mytardisbf.filters.tardis_util.process_meta",
      ignore_result=True)
def process_meta(func, df, schema_name, overwrite=False, **kwargs):
    """Extract metadata from a Datafile using a provided function and save the
    outputs as DatafileParameters.

    Parameters
    ----------
    func: Function
        Function to extract metadata from a file. Function must have
        input_file_path as an argument e.g.:
        def meta_proc(input_file_path, **kwargs):
            ...
        It must return a dict containing ParameterNames as keys and the
        Parameters to be saved as values. Parameters (values) can be singular
        strings/numerics or a list of strings/numeric. If it's a list, each
        element will be saved as a new DatafileParameter.
    df: tardis.tardis_portal.models.Datafile
        Datafile instance to process.
    schema_name: str
        Names of schema which describes ParameterNames
    add: boolean (default: False)
        Specifies whether or not to add to an existing Parameterset for this
        Datafile rather that overwriting or exiting.
    overwrite: boolean (default: False)
        Specifies whether to overwrite any exisiting parametersets for
        this datafile.


    Returns
    -------
    None
    """
    # Need to start a JVM in each thread
    global started
    if not started:
        logger.debug("Starting a new JVM")
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='4G',
                            run_headless=True)
        started = True
    try:
        javabridge.attach()
        log4j.basic_config()
        schema = Schema.objects.get(namespace__exact=schema_name)
        if DatafileParameterSet.objects\
                .filter(schema=schema, datafile=df).exists():
            if overwrite:
                psets = DatafileParameterSet.objects.get(schema=schema,
                                                         datafile=df)
                logger.warning("Overwriting parametersets for %s"
                               % df.filename)
                [delete_old_parameterset(ps) for ps in psets]
            else:
                logger.warning("Parametersets for %s already exist."
                               % df.filename)
                return

        dfo = DataFileObject.objects.filter(datafile__id=df.id,
                                            verified=True).first()
        input_file_path = dfo.get_full_path()

        logger.debug("Processing file: %s" % input_file_path)
        metadata_params = func(input_file_path, **kwargs)

        if not metadata_params:
            logger.debug("No metadata to save")
            return

        for sm in metadata_params:
            ps = DatafileParameterSet(schema=schema, datafile=df)
            ps.save()

            logger.debug("Saving parameters for: %s" % input_file_path)
            save_parameters(schema, ps, sm)
    except Exception, e:
        logger.debug(e)
    finally:
        javabridge.detach()
