import numpy as np

from .augmentation import Augmentation


class GaussianNoise(Augmentation):
    def __init__(self, mean=0, variance=0.1, probability=1):
        super(GaussianNoise, self).__init__(probability)
        self.mean = mean
        self.variance = variance

    def augment(self, image, annotation):
        row, col, ch = image.shape
        sigma = self.variance ** 0.5
        gauss = np.random.normal(self.mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy, annotation


class PoissonNoise(Augmentation):
    def __init__(self, probability=1):
        super(PoissonNoise, self).__init__(probability)

    def augment(self, image, annotation):
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy, annotation


class SPNoise(Augmentation):
    def __init__(self, s_vs_p=0.5, amount=0.004, probability=1):
        super(SPNoise, self).__init__(probability)
        self.s_vs_p = s_vs_p
        self.amount = amount

    def augment(self, image, annotation):
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(self.amount * image.size * self.s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        coords = tuple(coords)
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(self.amount * image.size * (1. - self.s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        coords = tuple(coords)
        out[coords] = 0
        return out, annotation


class SpeckleNoise(Augmentation):
    def __init__(self,probability=1):
        super(SpeckleNoise, self).__init__(probability)

    def augment(self, image, annotation):
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss

        return noisy, annotation
