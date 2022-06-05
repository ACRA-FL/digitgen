import unittest

import numpy as np

from digitgen import test_annotations
from digitgen.augmentation import GaussianNoise, SPNoise
from digitgen.digit import DigitSequence, DigitConfig
from digitgen.font import FontConfig
from digitgen.utils import CONFIGURATION


class TestNoiseAugmentation(unittest.TestCase):
    def setUp(self) -> None:
        self.font_type = FontConfig()
        self.config = CONFIGURATION
        self.config["common_configs"]["font_file_loc"] = self.font_type.get_font_file_location()

    def test_gaussian_noise(self):
        configurations = [DigitConfig.load_config(self.config, x) for x in "123 7583847 475845 5849"]
        digits = DigitSequence(configs=configurations)
        array, annotation = digits.data()
        test_annotations(array, annotation)

        configurations = [DigitConfig.load_config(self.config, x) for x in "123 7583847 475845 5849"]
        digits = DigitSequence(configs=configurations, augmentations=[GaussianNoise(), SPNoise()])
        array, annotation = digits.data()
        test_annotations(array, annotation)
        self.assertTrue(np.unique(array).shape[0] > 2)
