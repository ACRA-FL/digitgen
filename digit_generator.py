import json
from random import sample
from time import time
from digits import DigitSequence, DigitConfig
import numpy as np
from collections.abc import Sequence
from helper import test_annotations, format_annotations
import time
from config import CONFIGURATION


class DigitGenerator(object):
    def __init__(self,digit_size:int,
                    font_file:str,
                    samples=1,
                    image_size: Sequence[tuple[int,int]] = None,
                    allowed_digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) -> None:
        self.digit_size = digit_size
        self.samples = samples
        self.image_size = image_size
        self.allowed_digits = allowed_digits

        self.config = CONFIGURATION

        self.memory = {}#dict.fromkeys(allowed_digits,None)

    def generate(self) -> Sequence[tuple[np.array,dict]]:
        """
        Generator function of the dataset

        Returns:
            Sequence[tuple[np.array,dict]]: img_array,annotation
        """
        # print(np.unique(random_array,return_counts=True))

        annotations = {"annotations":[]}
        arrays = []
        for _ in self.samples:

            configurations = [DigitConfig.load_config(self.config, x) for x in row]
            digits = DigitSequence(configs=configurations, size=self.image_size, memory=self.memory)
            array, annotation = digits.data()
            arrays.append(array)
            format_annotations(annotations,annotation)

        return np.array(arrays), annotations





if __name__ == "__main__":
    start = time.process_time()

    digit_gen = DigitGenerator(10,"D:\\ACRA\\ImageGenerationPipeline\\Experiments\\digit_configurations.json", samples=100000, image_size=(128,48))
    ret_arr,ret_ann = digit_gen.generate()

    end = time.process_time()

    print(len(ret_arr)," Timetaken :- ",end-start)
    test_annotations(ret_arr[0],[x for x in ret_ann["annotations"] if x["image_id"] == 0])
