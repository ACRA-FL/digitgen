import random
import cv2 as cv

from .augmentation import SequenceAugmentation


class AscendingImageWidthChange(SequenceAugmentation):
    def __init__(self, width_increment=2, range_type="pixels"):
        super(AscendingImageWidthChange, self).__init__(probability=1)
        self.width_increment = width_increment
        self.range_type = range_type

    def augment(self, images, annotations):
        index_range = range(len(images))
        shift_factor = 0
        add_factor = 0

        if self.range_type == "pixels":
            for __id in index_range:
                img, ann = images[__id], annotations[__id]
                images[__id] = cv.resize(img, dsize=(img.shape[1] + add_factor, img.shape[0]))

                ann["bbox"][0] += shift_factor
                shift_factor += add_factor
                ann["bbox"][2] += shift_factor

                add_factor += self.width_increment


        elif self.range_type == "percentage":
            for __id in index_range:
                img, ann = images[__id], annotations[__id]
                rand_int = int(img.shape[1] * self.width_increment)

                images[__id] = cv.resize(img, dsize=(img.shape[1] + add_factor, img.shape[0]))

                ann["bbox"][0] += shift_factor
                shift_factor += add_factor
                ann["bbox"][2] += shift_factor

                add_factor += rand_int

        return images, annotations


class RandomImageWidthChange(SequenceAugmentation):
    def __init__(self, width_range=None, range_type="pixels"):
        super(RandomImageWidthChange, self).__init__(probability=1)
        if width_range is None:
            width_range = [0, 10]
        self.width_range = width_range
        self.range_type = range_type

    def augment(self, images, annotations):
        if self.range_type == "pixels":
            shift_factor = 0
            for __id in range(len(images)):
                rand_int = random.randint(self.width_range[0], self.width_range[1])

                img, ann = images[__id], annotations[__id]
                images[__id] = cv.resize(img, dsize=(img.shape[1] + rand_int, img.shape[0]))

                ann["bbox"][0] += shift_factor
                shift_factor += rand_int
                ann["bbox"][2] += shift_factor

        elif self.range_type == "percentage":
            shift_factor = 0
            for __id in range(len(images)):
                rand_int = random.randint(self.width_range[0], self.width_range[1])

                img, ann = images[__id], annotations[__id]
                rand_int = img.shape[1] * rand_int // 100

                images[__id] = cv.resize(img, dsize=(img.shape[1] + rand_int, img.shape[0]))

                ann["bbox"][0] += shift_factor
                shift_factor += rand_int
                ann["bbox"][2] += shift_factor

        return images, annotations
