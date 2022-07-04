import numpy as np

from .digit import DigitConfig, DigitSequence
from .utils import CONFIGURATION
from .utils import convert_to_grayscale
from .font import FontConfig
from .utils import (format_annotations, generate_random_digits, generate_random_digits_with_probability, add_spaces,
                    category_id, generate_random_digits_with_positional_probability, change_between_configs)

from .augmentation import SequenceAugmentation, SingleDigitAugmentation


class DigitGenerator(object):
    def __init__(self, digit_size: int,
                 font_type: str = "terminal-grotesque-regular",
                 samples=1,
                 gray_scale=False,
                 transpose=False,
                 image_size=None,
                 augmentations=None) -> None:
        if augmentations is None:
            augmentations = []
        self.allowed_digits = None
        self.digit_size = digit_size
        self.samples = samples
        self.image_size = image_size
        self.digit_augmentations = []
        self.sequence_augmentation = []
        self.gray_scaled = gray_scale
        self.transpose = transpose

        for aug in augmentations:
            if isinstance(aug, SingleDigitAugmentation):
                self.digit_augmentations.append(aug)
            elif isinstance(aug, SequenceAugmentation):
                self.sequence_augmentation.append(aug)
            else:
                raise NotImplementedError

        self.font_type = FontConfig(font_type=font_type)
        self.config = CONFIGURATION
        self.config["common_configs"]["font_file_loc"] = self.font_type.get_font_file_location()

        self.generated_digits = None
        self.generated_configs = []
        self.memory = {}
        self.id2category = None
        self.category2id = None

    def change_common_config(self, changes: dict):
        for k, v in changes.items():
            print(k, self.config["common_configs"][k])
            self.config["common_configs"][k] = v
            print(k, self.config["common_configs"][k])

    def generate_digits(self, allowed_digits=None):
        if allowed_digits is None:
            allowed_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        random_lists = []
        for _ in range(self.samples):
            row = generate_random_digits(self.digit_size, allowed_digits)
            random_lists.append(row)

        self.allowed_digits = allowed_digits
        self.generated_digits = random_lists

    def generate_digits_with_choice_probability(self, probability: dict):
        random_lists = []
        for _ in range(self.samples):
            row = generate_random_digits_with_probability(self.digit_size, probability)
            random_lists.append(row)

        self.allowed_digits = list(probability.keys())
        self.generated_digits = random_lists

    def generate_digits_with_position_probability(self, probability: dict):
        random_lists = []
        for _ in range(self.samples):
            row = generate_random_digits_with_positional_probability(self.digit_size, probability)
            random_lists.append(row)

        all_values = []
        for __probability in probability.values():
            all_values += __probability.keys()

        self.allowed_digits = list(tuple(all_values))
        self.generated_digits = random_lists

    def generate_spaces(self, space_type="None", num_spaces=None, sectors=None, spaces_per_sector=None):
        assert self.generated_digits
        space_lists = []

        for row in self.generated_digits:
            row = add_spaces(row, space_type, num_spaces, sectors, spaces_per_sector, self.digit_size)
            space_lists.append(row)

        self.allowed_digits.append(" ")
        self.generated_digits = space_lists

    def generate_digit_config(self):
        id2category, category2id = category_id(self.allowed_digits)

        self.id2category = id2category
        self.category2id = category2id

        for row_id in range(self.samples):
            row = self.generated_digits[row_id]
            configurations = [DigitConfig.load_config(
                self.config, x, category2id[x]) for x in row]

            self.generated_configs.append(configurations)

    def add_width_digits(self, mode="constant", pixel_value=5, pixel_range=None):
        if pixel_range is None:
            pixel_range = [0, 20]

        change_between_configs(self.generated_configs, mode, pixel_value, pixel_range, self.samples,
                               self.digit_size)

    def generate_dataset(self):
        """
        Generator function of the dataset

        Returns:
            Sequence[tuple[np.array,dict]]: img_array,annotation
        """

        annotations = {"annotations": []}
        arrays = []
        for row in self.generated_configs:
            digits = DigitSequence(
                configs=row, size=self.image_size, memory=self.memory,
                sequence_augmentations=self.sequence_augmentation, digit_augmentations=self.digit_augmentations)
            array, annotation = digits.data()

            if self.transpose:
                array = np.transpose(array, axes=(1, 0, 2))

            arrays.append(array)
            format_annotations(annotations, annotation, self.id2category)

        arrays = np.array(arrays)
        if self.gray_scaled:
            arrays = convert_to_grayscale(arrays)
        return arrays, annotations
