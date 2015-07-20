import os
import numpy as np
import bioformats
from scipy.ndimage import zoom


def stretch_contrast(img):
    """Simple linear contrast stretch

    Parameters
    ----------
    img: numpy.ndarray
        N x M array of grayscale image intensities

    Returns
    -------
    img: numpy.ndarray (dtype = np.int8)
        Output image with contrast stretch over the 8-bit range.
    """
    s = np.subtract(img, np.min(img))
    p = 255.0 / (np.max(img) - np.min(img))
    out = np.round(np.multiply(s, p)).astype(np.uint8)
    return out


def get_preview_image(fname, meta_xml=None, maxwh=256, series=0):
    """ Generate a thumbnail of an image at the specified path. Gets the
    middle Z plane of channel=0 and timepoint=0 of the specified series.

    Parameters
    ----------
    fname: str
        Path to image file.
    meta_xml: str
        OME XML metadata.
    maxwh: int
        Maximum width or height of the output thumbnail. If the extracted
        image is larger in either x or y, the image will will be downsized
        to fit.
    series: int
        Series for multi-stack formats (default=0)

    Returns
    -------
    img: numpy.ndarray
        N x M array of grayscale pixel intentsities.
    """
    name, ext = os.path.splitext(os.path.basename(fname))

    if ext[1:] not in bioformats.READABLE_FORMATS:
        raise Exception("Format not supported: %s" % ext[1:])

    if not meta_xml:
        meta_xml = bioformats.get_omexml_metadata(fname)
    ome = bioformats.OMEXML(meta_xml)

    if series > ome.get_image_count():
        raise Exception("Specified series number %s exceeds number of series "
                        "in the image file: %s" % (series, fname))

    # Get metadata for first series
    meta = ome.image(0).Pixels

    # Determine resize factor
    sizex = meta.SizeX
    sizey = meta.SizeY
    if sizex > maxwh or sizey > maxwh:
        f = min(float(maxwh) / float(sizex), float(maxwh) / float(sizey))
    else:
        f = max(float(maxwh) / float(sizex), float(maxwh) / float(sizey))

    # Determine which Z slice
    z = 0

    # Determine middle Z plane
    # Note: SizeZ doesn't seem to be reliable. Might need to check BF.
    # Stick with first slice for now.
    # if meta.SizeZ > 1:
    #     z = int(math.floor(float(meta.SizeZ)/2))

    # Load image plane
    if meta.channel_count == 1 and meta.SizeC == 4:
        # RGB Image
        img = bioformats.load_image(fname, t=0, z=z, series=series,
                                    rescale=False)
        return zoom(img, (f, f, 1))
    else:
        # Grayscale, grab channel 0 only
        img = bioformats.load_image(fname, c=0, t=0, z=z, series=series,
                                    rescale=False)
        # if img.dtype in (np.uint16, np.uint32, np.int16, np.int32):
        img = stretch_contrast(img)
        return zoom(img, f)


def save_image(img, output_path, overwrite=False):
    """Extract and save a preview image for an input image.

    Parameters
    ----------
    img: ndarray
        N x M array of grayscale pixel intentsities.
    output_path: str
        Path to which the output file is to be saved.
    overwrite: boolean, (default False)
        Specifies whether or not to overwrite an existing file if a
        file already exist at the output path.
    """
    if os.path.exists(output_path):
        if not overwrite:
            raise Exception("Ouput file %s already exists and parameter"
                            "overwrite=False" % output_path)
        else:
            os.remove(output_path)

    bioformats.write_image(output_path, img, bioformats.PT_UINT8)
