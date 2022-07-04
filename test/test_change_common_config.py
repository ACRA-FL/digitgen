import unittest
import numpy as np
from digitgen import DigitGenerator
from digitgen import test_annotations


class TestChangeCommonConfig(unittest.TestCase):
    def test_default_transpose_generation(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48))
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])

        self.assertTrue(ret_arr.shape == (100, 48, 128, 3))

        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48))
        digit_gen.change_common_config({"background_color": (0, 0, 0), "digit_color": (255, 255, 255)})
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])

        self.assertTrue(ret_arr.shape == (100, 48, 128, 3))
