import unittest
import numpy as np
from digitgen import DigitGenerator


class TestDigitSpaces(unittest.TestCase):
    def test_random_digit_generation(self):
        digit_gen = DigitGenerator(10, samples=100, image_size=(128, 48))
        digit_gen.generate_digits()
        counts = np.unique(digit_gen.generated_digits, return_counts=True)[1]
        _max = max(counts)
        _min = min(counts)
        self.assertTrue(_max < 100 * 1.5 and _min > 100 * 0.5)

    def test_inline_probability(self):
        digit_gen = DigitGenerator(10, samples=1000, image_size=(128, 48))
        digit_gen.generate_digits_with_choice_probability({"0": 0.5, "1": 0.1, "2": 0.2, "3": 0.2})
        counts = np.unique(digit_gen.generated_digits, return_counts=True)[1]
        self.assertTrue(5000 * 1.2 > counts[0] > 5000 * 0.8)

    def test_position_probability(self):
        digit_gen = DigitGenerator(10, samples=1000, image_size=(128, 48))
        digit_gen.generate_digits_with_position_probability(
            {0: {"0": 0.5, "1": 0.1, "2": 0.2, "3": 0.2}, 1: {"4": 1}, 2: {"5": 0.5, "8": 0.5},
             "default": {"0": 0.1, "1": 0.1, "2": 0.1, "3": 0.1, "4": 0.1, "5": 0.1, "6": 0.1, "7": 0.1, "8": 0.1,
                         "9": 0.1}})
        for d in digit_gen.generated_digits:
            self.assertTrue(d[1] == "4")
            self.assertTrue(d[2] in ["5", "8"])
