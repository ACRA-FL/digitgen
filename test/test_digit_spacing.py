import unittest
import numpy as np
from digitgen import DigitGenerator
from digitgen import test_annotations


class TestSpaceBetweenDigits(unittest.TestCase):
    def test_normal(self):
        digit_gen = DigitGenerator(10, samples=10, image_size=(512, 48))
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 10)

    def test_constant_space_between_digits(self):
        digit_gen = DigitGenerator(10, samples=20, image_size=(512, 48))
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        digit_gen.add_width_digits(pixel_value=5)
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 10)

    def test_random_space_between_digits(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(512, 48))
        digit_gen.generate_digits()
        digit_gen.generate_digit_config()
        digit_gen.add_width_digits(mode="random", pixel_range=[0, 10])
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 10)
