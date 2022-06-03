import os
from time import process_time

import numpy as np

from .digit import DigitConfig, DigitSequence
from .utils import CONFIGURATION
from .utils import (format_annotations, generate_random_digits,
                    test_annotations)


class DigitGenerator(object):
    def __init__(self, digit_size: int,
                 font_file: str,
                 samples=1,
                 image_size= None,
                 allowed_digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) -> None:
        self.digit_size = digit_size
        self.samples = samples
        self.image_size = image_size
        self.allowed_digits = allowed_digits

        self.config = CONFIGURATION
        self.config["common_configs"]["font_file_loc"] = font_file

        self.memory = {}  # dict.fromkeys(allowed_digits,None)

    def generate(self, space_type="None", num_spaces=None, sectors=None, spaces_per_sector=None):
        """
        Generator function of the dataset

        Returns:
            Sequence[tuple[np.array,dict]]: img_array,annotation
        """
        # print(np.unique(random_array,return_counts=True))

        annotations = {"annotations": []}
        arrays = []
        for _ in range(self.samples):
            row = generate_random_digits(self.digit_size, self.allowed_digits, space_type, num_spaces, sectors,
                                         spaces_per_sector)

            configurations = [DigitConfig.load_config(
                self.config, x) for x in row]
            digits = DigitSequence(
                configs=configurations, size=self.image_size, memory=self.memory)
            array, annotation = digits.data()
            arrays.append(array)
            format_annotations(annotations, annotation)

        return np.array(arrays), annotations


if __name__ == "__main__":
    start = process_time()

    digit_gen = DigitGenerator(10, "D:\\ACRA\\digitgen\\digitgen\\font\\terminal-grotesque.grotesque-regular.ttf", samples=100, image_size=(128, 48))
    ret_arr, ret_ann = digit_gen.generate(space_type="space", sectors=3, spaces_per_sector=2)

    end = process_time()

    print(len(ret_arr), " Timetaken :- ", end - start)
    test_annotations(
        ret_arr[0], [x for x in ret_ann["annotations"] if x["image_id"] == 0])
