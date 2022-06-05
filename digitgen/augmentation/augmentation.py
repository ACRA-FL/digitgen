from abc import ABC, abstractmethod


class Augmentation(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def augment(self, image, annotation):
        pass
