from abc import ABC, abstractmethod
from random import random


class Augmentation(ABC):
    def __init__(self, probability) -> None:
        super().__init__()
        self.probability = probability

    @abstractmethod
    def augment(self, image, annotation):
        pass

    def apply_augmentation(self, image, annotation):
        value = random()
        if value <= self.probability:
            return self.augment(image, annotation)

        return image, annotation
