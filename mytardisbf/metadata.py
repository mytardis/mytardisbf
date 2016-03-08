import logging
import os
import bioformats
import javabridge
from mytardisbf import previewimage
from xml.etree import ElementTree as et

logger = logging.getLogger(__name__)


# OME XML Namespace lookups
IMAGE = '{http://www.openmicroscopy.org/Schemas/OME/2013-06}Image'
PIXEL = '{http://www.openmicroscopy.org/Schemas/OME/2013-06}Pixels'
CHANNEL = '{http://www.openmicroscopy.org/Schemas/OME/2013-06}Channel'


def get_original_metadata(omexml):
    """ Get the original metadata from structured annotations in OME XML.
    Note: this is currently not used at this stage.

    Parameters
    ----------
    omexml: str
        OME XML metadata

    Returns
    -------
    orig_meta: dict
        Dict containing key and value pairs for each original
        metadata element
    """
    meta_xml = et.fromstring(omexml.encode('utf-8'))
    sa = '{http://www.openmicroscopy.org/Schemas/SA/2013-06}StructuredAnnotations/'\
         '{http://www.openmicroscopy.org/Schemas/SA/2013-06}XMLAnnotation/'\
         '{http://www.openmicroscopy.org/Schemas/SA/2013-06}Value/'\
         '{http://www.openmicroscopy.org/Schemas/SA/2013-06}OriginalMetadata'

    return dict([(elem.find('{http://www.openmicroscopy.org/Schemas/SA/2013-06}Key').text,
                 elem.find('{http://www.openmicroscopy.org/Schemas/SA/2013-06}Value').text)
                 for elem in meta_xml.findall(sa)])


def get_meta(input_file_path, output_path, **kwargs):
    """ Extract specific metadata typically used in bio-image analysis. Also
    outputs a preview image to the output directory.

    Parameters
    ----------
    input_file_path: str
        Input file path
    output_path: str

    Returns
    -------
    meta: [dict]
        List of dicts containing with keys and values for specific metadata
    """
    pix_exc = set(["id", "significantbits", "bigendian", "interleaved"])
    channel_exc = set(["color", "id", "color", "contrastmethod", "fluor",
                       "ndfilter", "illuminationtype", "name",
                       "pockelcellsetting", "acquisitionmode"])
    input_fname, ext = os.path.splitext(os.path.basename(input_file_path))
    if ext[1:] not in bioformats.READABLE_FORMATS:
        logger.debug("Unsupported format: %s.%s" % (input_fname, ext))
        return

    try:
        omexml = bioformats.get_omexml_metadata(input_file_path).encode('utf-8')
    except javabridge.jutil.JavaException:
        logger.debug("Unable to read OME Metadata from: %s.%s"
                     % (input_fname, ext))
        return

    meta_xml = et.fromstring(omexml)
    meta = list()
    for i, img_meta in enumerate(meta_xml.iter(IMAGE)):
        smeta = dict()
        output_file_path = os.path.join(output_path,
                                        input_fname+"_s%s.png" % i)
        logger.debug("Generating series %s preview from image: %s"
                     % (i, input_fname+ext))
        img = previewimage.get_preview_image(input_file_path, omexml, series=i)
        logger.debug("Saving series %s preview from image: %s"
                     % (i, input_fname+ext))
        previewimage.save_image(img, output_file_path, overwrite=True)
        logger.debug("Extracting metadata for series %s preview from image: %s"
                     % (i, input_fname+ext))
        smeta['id'] = img_meta.attrib['ID']
        smeta['name'] = img_meta.attrib['Name']
        smeta['previewImage'] = output_file_path
        for pix_meta in img_meta.iter(PIXEL):
            for k, v in pix_meta.attrib.iteritems():
                if k.lower() not in pix_exc:
                    smeta[k.lower()] = v
            for c, channel_meta in enumerate(pix_meta.iter(CHANNEL)):
                for kc, vc in channel_meta.attrib.iteritems():
                    if kc.lower() not in channel_exc:
                        if kc.lower() not in smeta:
                            smeta[kc.lower()] = ["Channel %s: %s" % (c, vc)]
                        else:
                            smeta[kc.lower()].append("Channel %s: %s" % (c, vc))

        meta.append(smeta)

    return meta


def get_ome_metadata(input_file_path, output_path, **kwargs):
    """ Extracts metadata from an input file and save it to a file at
    the specified output_path.
    Note: this is currently not used at this stage.

    Parameters
    ----------
    input_file_path: str
        Path to the input file

    """
    input_fname, ext = os.path.splitext(os.path.basename(input_file_path))
    if ext[1:] not in bioformats.READABLE_FORMATS:
        raise Exception("Unsupported format: %s.%s" % (input_fname, ext))

    meta_xml = bioformats.get_omexml_metadata(input_file_path)

    output_file_path = os.path.join(output_path, input_fname+".xml")
    with open(output_file_path, "w") as f:
        f.write(meta_xml.encode('utf-8'))

    return {"ome": output_file_path}
