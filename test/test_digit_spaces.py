import unittest

from digitgen import DigitGenerator
from digitgen import test_annotations


class TestDigitSpaces(unittest.TestCase):
    def test_just_digits(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48))
        digit_gen.generate_digits()
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 10)

    def test_space_sectors(self):
        digit_gen = DigitGenerator(12, samples=100, image_size=(128, 48))
        digit_gen.generate_digits()
        digit_gen.generate_spaces(space_type="space", sectors=3, spaces_per_sector=2)
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 16)

    def test_space_random(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48))
        digit_gen.generate_digits()
        digit_gen.generate_spaces(space_type="random", num_spaces=3)
        ret_arr, ret_ann = digit_gen.generate_dataset()
        test_annotations(ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
        self.assertTrue(len([x for x in ret_ann["annotations"] if x["image_id"] == 0]) == 13)
