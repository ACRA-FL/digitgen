import random
import scipy.ndimage.filters as fi
import numpy as np

from .augmentation import SingleDigitAugmentation


class GaussianNoise(SingleDigitAugmentation):
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
        np.clip(noisy, 0, 255)
        return noisy, annotation


class PoissonNoise(SingleDigitAugmentation):
    def __init__(self, probability=1):
        super(PoissonNoise, self).__init__(probability)

    def augment(self, image, annotation):
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        np.clip(noisy, 0, 255)
        return noisy, annotation


class SPNoise(SingleDigitAugmentation):
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
        np.clip(out, 0, 255)
        return out, annotation


class SpeckleNoise(SingleDigitAugmentation):
    def __init__(self, probability=1):
        super(SpeckleNoise, self).__init__(probability)

    def augment(self, image, annotation):
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        np.clip(noisy, 0, 255)
        return noisy, annotation


class ShadowPatch(SingleDigitAugmentation):
    def __init__(self, alpha=0.7, probability=1):
        super(ShadowPatch, self).__init__(probability)
        self.alpha = alpha

    def augment(self, image, annotation):
        t = random.randint(0, 2)
        if t == 1:
            image_size = image.shape
            kernel_size = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
            shadow = np.ones(kernel_size)
            x_displacement = random.randint(0, (image_size[0] - kernel_size[0]) // 2)
            x_remain = image_size[0] - kernel_size[0] - x_displacement
            y_displacement = random.randint(0, (image_size[1] - kernel_size[1]) // 2)
            y_remain = image_size[1] - kernel_size[1] - y_displacement
            shadow_patch = np.pad(shadow, ((x_displacement, x_remain), (y_displacement, y_remain)), 'constant',
                                  constant_values=[0]) * 255
            image = np.clip(image - (1 - self.alpha) * shadow_patch, 0, 255)
        return image, annotation


class FlashSpot(SingleDigitAugmentation):
    def __init__(self, probability=1, alpha=0.5):
        super(FlashSpot, self).__init__(probability)
        self.alpha = alpha

    @staticmethod
    def __gkernel(kernelLen=21, nsig=3):
        inp = np.zeros((kernelLen, kernelLen))
        kernel = fi.gaussian_filter(inp, nsig)
        return np.clip(kernel / kernel.max(), 0, 1) * 255

    def augment(self, image, annotation):
        t = random.randint(0, 2)
        if t == 1:
            kernel_size = random.randint(15, 35)
            nsig = random.randint(1, 7)
            image_size = image.shape
            flash = FlashSpot.__gkernel(kernel_size, nsig)
            x_displacement = random.randint(0, (image_size[0] - kernel_size) // 2)
            x_remain = image_size[0] - kernel_size - x_displacement
            y_displacement = random.randint(0, (image_size[1] - kernel_size) // 2)
            y_remain = image_size[1] - kernel_size - y_displacement
            flash_patch = np.pad(flash, ((x_displacement, x_remain), (y_displacement, y_remain)), 'constant',
                                 constant_values=[0])
            image = np.clip(image + self.alpha * flash_patch, 0, 255)
        return super().augment(image, annotation)
