import os
import unittest
import numpy as np
import tempfile

from mytardisbf import previewimage
from scipy.ndimage import imread


class PreviewImageFilterTests(unittest.TestCase):
    """Tests for PreviewImage Filter"""
    def setUp(self):
        self.multi_image_path = "./mytardisbf/tests/data/IMCD3 170615.lif"
        self.rgb = "./mytardisbf/tests/data/IMG_0222.png"
        self.her = "./mytardisbf/tests/data/her.tif"
        self.dv = "./mytardisbf/tests/data/D3D.dv"

    @unittest.skip("requires large dataset not generally available")
    def test_get_preview_image(self):
        zimg = imread("./mytardisbf/tests/data/zoom.png")
        img = previewimage.get_preview_image(self.multi_image_path)
        np.testing.assert_array_equal(img, zimg)

    @unittest.skip("requires large dataset not generally available")
    def test_get_dv_preview(self):
        zdv = imread("./mytardisbf/tests/data/D3D_zoom.png")
        img = previewimage.get_preview_image(self.dv)
        np.testing.assert_array_equal(img, zdv)

    def test_get_rgb_preview(self):
        zrgb = imread("./mytardisbf/tests/data/rgb_zoom.png")
        img = previewimage.get_preview_image(self.rgb)
        np.testing.assert_array_equal(img, zrgb)

    @unittest.skip("requires large dataset not generally available")
    def test_get_16bit_preview(self):
        z16 = imread("./mytardisbf/tests/data/z16.png")
        img = previewimage.get_preview_image(self.her)
        np.testing.assert_array_equal(img, z16)

    @unittest.skip("requires large dataset not generally available")
    def test_save_preview_image(self):
        img = previewimage.get_preview_image(self.dv)
        out_path = os.path.join(tempfile.gettempdir(), "temp.png")
        previewimage.save_image(img, out_path, overwrite=True)

        img2 = imread(out_path)
        np.testing.assert_array_equal(img, img2)
