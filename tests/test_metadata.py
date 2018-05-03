import json
import unittest
import tempfile
import numpy as np

from mytardisbf import metadata
from scipy.ndimage import imread


class MetadataTest(unittest.TestCase):
    """Unit tests for metadata methods"""
    def setUp(self):
        self.dv = "./mytardisbf/tests/data/D3D.dv"
        self.dv_zoom = "./mytardisbf/tests/data/D3D_zoom.png"
        self.dv_meta = "./mytardisbf/tests/data/D3D.json"

    @unittest.skip("requires large dataset not generally available")
    def test_get_meta(self):
        td = tempfile.gettempdir()
        meta = metadata.get_meta(self.dv, td)[0]
        meta_rd = open(self.dv_meta).read()
        meta_rd = json.loads(meta_rd)
        self.assertEqual(meta, meta_rd)

    @unittest.skip("requires large dataset not generally available")
    def test_get_meta_preview(self):
        td = tempfile.gettempdir()
        meta = metadata.get_meta(self.dv, td)[0]
        img = imread(meta['previewImage'])
        img_rd = imread(self.dv_zoom)
        np.testing.assert_array_equal(img, img_rd)

    def test_get_non_ome_xml(self):
        td = tempfile.gettempdir()
        out = metadata.get_meta("./mytardisbf/tests/data/a.xml", td)
        self.assertEqual(out, None)
