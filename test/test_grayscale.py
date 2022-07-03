import unittest
import numpy as np
from digitgen import DigitGenerator


class TestGrayScale(unittest.TestCase):
    def test_default_grayscale_generation(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48), gray_scale=False)
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        ret_arr, ret_ann = digit_gen.generate_dataset()

        self.assertTrue(ret_arr.shape == (100, 48, 128, 3))

        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48), gray_scale=True)
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        ret_arr, ret_ann = digit_gen.generate_dataset()

        self.assertTrue(ret_arr.shape == (100, 48, 128))
