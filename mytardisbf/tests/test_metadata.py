import json
import unittest
import numpy as np
import tempfile

from mytardisbf import metadata
from scipy.ndimage import imread


class MetadataTest(unittest.TestCase):
    """Unit tests for metadata methods"""
    def setUp(self):
        self.dv = "./mytardisbf/tests/data/D3D.dv"
        self.dv_zoom = "./mytardisbf/tests/data/D3D_zoom.png"
        self.dv_meta = "./mytardisbf/tests/data/D3D.json"

    def test_get_meta(self):
        td = tempfile.gettempdir()
        meta = metadata.get_meta(self.dv, td)[0]
        meta_rd = open(self.dv_meta).read()
        meta_rd = json.loads(meta_rd)
        self.assertEqual(meta, meta_rd)

    def test_get_meta_preview(self):
        td = tempfile.gettempdir()
        meta = metadata.get_meta(self.dv, td)[0]
        img = imread(meta['previewImage'])
        img_rd = imread(self.dv_zoom)
        np.testing.assert_array_equal(img, img_rd)
