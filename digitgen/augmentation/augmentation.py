from abc import ABC, abstractmethod
from random import random


class Augmentation(ABC):
    def __init__(self, probability) -> None:
        super().__init__()
        self.probability = probability

    @abstractmethod
    def augment(self, images, annotations):
        pass

    def apply_augmentation(self, images, annotations):
        value = random()
        if value <= self.probability:
            return self.augment(images, annotations)

        return images, annotations


class SingleDigitAugmentation(Augmentation):
    def __init__(self, probability) -> None:
        super().__init__(probability)

    @abstractmethod
    def augment(self, image, annotation):
        pass


class SequenceAugmentation(Augmentation):
    def __init__(self, probability) -> None:
        super().__init__(probability)

    @abstractmethod
    def augment(self, image, annotation):
        pass
