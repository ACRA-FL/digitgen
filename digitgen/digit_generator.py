import numpy as np

from .digit import DigitConfig, DigitSequence
from .utils import CONFIGURATION
from .font import FontConfig
from .utils import (format_annotations, generate_random_digits, add_spaces)


class DigitGenerator(object):
    def __init__(self, digit_size: int,
                 font_type: str = "terminal-grotesque-regular",
                 samples=1,
                 image_size=None,
                 allowed_digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],

                 augmentations=[]) -> None:
        self.digit_size = digit_size
        self.samples = samples
        self.image_size = image_size
        self.allowed_digits = allowed_digits
        self.augmentations = augmentations

        self.font_type = FontConfig(font_type=font_type)
        self.config = CONFIGURATION
        self.config["common_configs"]["font_file_loc"] = self.font_type.get_font_file_location()

        self.generated_digits = None
        self.memory = {}

    def generate_random_numbers(self):
        random_lists = []
        for _ in range(self.samples):
            row = generate_random_digits(self.digit_size)
            random_lists.append(row)

        self.generated_digits = random_lists

    def generate_spaces(self, space_type="None", num_spaces=None, sectors=None, spaces_per_sector=None):
        assert self.generated_digits
        space_lists = []

        for row in self.generated_digits:
            row = add_spaces(row, space_type, num_spaces, sectors, spaces_per_sector, self.digit_size)
            space_lists.append(row)

        self.generated_digits = space_lists

    def generate_dataset(self):
        """
        Generator function of the dataset

        Returns:
            Sequence[tuple[np.array,dict]]: img_array,annotation
        """

        annotations = {"annotations": []}
        arrays = []
        for row in self.generated_digits:
            configurations = [DigitConfig.load_config(
                self.config, x) for x in row]
            digits = DigitSequence(
                configs=configurations, size=self.image_size, memory=self.memory, augmentations=self.augmentations)
            array, annotation = digits.data()
            arrays.append(array)
            format_annotations(annotations, annotation)

        return np.array(arrays), annotations
