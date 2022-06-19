import json
from abc import ABC, abstractmethod
from typing import List

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def resize_and_align_bounding_box(bbox: list, original_image: np.array, target_width: int, target_height: int):
    y_, x_, _ = original_image.shape

    x_scale = target_width / x_
    y_scale = target_height / y_

    origLeft, origTop, origRight, origBottom = tuple(bbox)

    x = int(np.round(origLeft * x_scale))
    y = int(np.round(origTop * y_scale))
    xmax = int(np.round(origRight * x_scale))
    ymax = int(np.round(origBottom * y_scale))

    return [x - 0.5, y - 0.5, xmax + 0.5, ymax + 0.5]


class DigitConfig(object):
    """
    Class Handling the configurations of the individual Digit image generation.
    """

    def __init__(self, digit: str,
                 category_id: int,
                 font_scale: int = None,
                 img_size: list = None,
                 start_point: list = None,
                 font_file_loc: str = None,
                 background_color: list = None,
                 digit_color: list = None,
                 bbox_color: list = None,
                 bbox_width: list = None,
                 bbox: list = None) -> None:
        self.digit = digit
        self.font_scale = font_scale
        self.img_size = img_size
        self.start_point = start_point
        self.font_file_loc = font_file_loc
        self.digit_color = digit_color
        self.background_color = background_color
        self.bbox_color = bbox_color
        self.bbox_width = bbox_width
        self.bbox = bbox
        self.category_id = category_id

    def __repr__(self) -> str:
        display_string = f"\nDigitConfig \n digit :- {self.digit}" \
                         + f" \n font scale :- {self.font_scale}\n size :- {self.img_size} \n start_Point :- {self.start_point} " \
                         + f"\n font_file_loc :- {self.font_file_loc} \n background_color :- {self.background_color} \n bbox :- {self.bbox}" \
                         + f"\n digit_color :- {self.digit_color} \n bbox_color :- {self.bbox_color} \n bbox_width :- {self.bbox_width}\n"
        return display_string

    @staticmethod
    def load_config(config_file, digit: str, category_id: int):
        """
        Load DigitConfig object using configuration file

        Args:
            config_file (dict/str): Either the config file location or dictionary loaded wit config
            digit (str): which digit config is needed
            category_id(int): Id of the category
        """
        if isinstance(config_file, str):
            with open(config_file, "r+", encoding="utf-8") as f0:
                config_file = json.load(f0)
        try:
            digit_config = config_file["digit_config"][digit]
        except KeyError as k:
            digit_config = config_file["digit_config"]["default"]

        common_config = config_file["common_configs"]
        return DigitConfig(
            digit=digit,
            category_id=category_id,
            font_scale=digit_config["fontscale"],
            img_size=digit_config["size"],
            start_point=digit_config["start_point"],
            bbox=digit_config["bbox"][:],
            font_file_loc=common_config["font_file_loc"],
            bbox_color=common_config["bbox_color"],
            bbox_width=common_config["bbox_width"]
        )


class DigitOperator(ABC):
    def __init__(self, resize=None, digit_augmentations=None,
                 sequence_augmentations=None) -> None:
        super().__init__()
        if digit_augmentations is None:
            digit_augmentations = []
        if sequence_augmentations is None:
            sequence_augmentations = []
        self.digit_augmentation = digit_augmentations
        self.sequence_augmentation = sequence_augmentations
        self.resize = resize

    @abstractmethod
    def to_array(self) -> np.array:
        """
        create digit image as np.array

        Returns:
            np.array: digit image
        """

    def to_image(self) -> Image:
        """
        create digit as a PIL Image.

        Returns:
            Image: digit PIL Image
        """
        img_array = self.to_array()
        # print(img_array.shape)
        return Image.fromarray(img_array)

    def show(self) -> None:
        """
        Show Digit
        """
        img = self.to_image()
        img.show()

    def save(self, location: str) -> None:
        """
        Save Digit Image

        Args:
            location (str): location to save image.
        """
        img = self.to_image()
        img.save(location)

    @abstractmethod
    def to_annotation(self) -> dict:
        """
        Generate Bboxes 

        Returns:
            dict: dictionary of bounding boxes
        """

    @abstractmethod
    def draw_bbox(self, save_loc: str = None) -> None:
        pass

    def apply_augmentations(self, array, annotations):
        if type(array) == list:
            if len(self.digit_augmentation) > 0:
                for i in range(len(annotations)):
                    for aug in self.digit_augmentation:
                        array[i], annotations[i] = aug.apply_augmentation(array[i], annotations[i])

            if len(self.sequence_augmentation) > 0:
                for aug in self.sequence_augmentation:
                    array, annotations = aug.apply_augmentation(array, annotations)

        else:
            if len(self.digit_augmentation) > 0:
                for aug in self.digit_augmentation:
                    array, annotations = aug.apply_augmentation(array, annotations)

        return array, annotations

    def data(self):
        array = self.to_array()
        annotation = self.to_annotation()

        array, annotation = self.apply_augmentations(array, annotation)

        if type(array) == list:
            array = np.hstack(array)

        if self.resize:
            for ann in annotation:
                ann["bbox"] = resize_and_align_bounding_box(ann["bbox"], array, self.resize[0], self.resize[1])

            array = cv2.resize(array, dsize=tuple(self.resize))

        return array, annotation


class Digit(DigitOperator):
    """
    Class That generate single Digit Image
    """

    def __init__(self, config: DigitConfig, size=None, memory: dict = {}, digit_augmentations=[],
                 sequence_augmentations=[]) -> None:
        super().__init__(digit_augmentations=digit_augmentations, sequence_augmentations=sequence_augmentations,
                         resize=size)
        self.config = config
        self.memory = memory

    def to_annotation(self) -> dict:
        """
        Generate the bbox of the digit

        Returns:
            dict: bbox as a dictionary
        """

        annotation = {
            "category_id": self.config.category_id,
            "bbox": self.config.bbox
        }

        return annotation

    def draw_bbox(self, save_loc: str = None) -> None:
        """
        Draws the bbox and show image

        Args:
            save_loc (str, optional): Location to save image if needed. Defaults to None.
        """
        image = self.to_image()
        bbox = self.config.bbox
        draw = ImageDraw.Draw(image)
        draw.rectangle(bbox,
                       outline=tuple(self.config.bbox_color),
                       width=self.config.bbox_width)

        image.show()
        if save_loc:
            image.save(save_loc)

    def __gen_img_array(self):
        """
        create digit image as np.array

        Returns:
            np.array: digit image
        """
        pil_im = Image.new("RGB", self.config.img_size, color=self.config.background_color)

        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype(self.config.font_file_loc, self.config.font_scale)

        draw.text(self.config.start_point, self.config.digit, font=font, fill=self.config.digit_color)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        return cv2_im_processed

    def to_array(self) -> np.array:
        try:
            return self.memory[self.config.digit]
        except KeyError:
            self.memory[self.config.digit] = self.__gen_img_array()
            return self.memory[self.config.digit]


class DigitSequence(DigitOperator):
    """
    Class That generate Sequence of Digit Image
    """

    def __init__(self, configs, size=None, memory: dict = {}, digit_augmentations=[],
                 sequence_augmentations=[]) -> None:
        super().__init__(digit_augmentations=digit_augmentations, sequence_augmentations=sequence_augmentations,
                         resize=size)
        self.configs = configs
        self.__set_offset()
        self.digits = [Digit(config=x, memory=memory) for x in self.configs]

    def to_array(self) -> np.array:
        digits_stack = [digit.to_array() for digit in self.digits]
        return digits_stack

    def __set_offset(self) -> None:
        offset_x = 0

        for each in self.configs:
            x, xmax = (each.bbox[0] + offset_x, each.bbox[2] + offset_x)
            each.bbox[0] = x
            each.bbox[2] = xmax

            offset_x += each.img_size[0]

    def to_annotation(self) -> List[dict]:
        lis_annotations = [digit.to_annotation() for digit in self.digits]
        return lis_annotations

    def draw_bbox(self, save_loc: str = None) -> None:
        """
        Draws the bbox and show image

        Args:
            save_loc (str, optional): Location to save image if needed. Defaults to None.
        """
        image = self.to_image()
        draw = ImageDraw.Draw(image)

        for each in self.configs:
            draw.rectangle(each.bbox,
                           outline=tuple(each.bbox_color),
                           width=each.bbox_width)

        image.show()
        if save_loc:
            image.save(save_loc)
