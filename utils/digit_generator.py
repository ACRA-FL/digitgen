import json
from digits import DigitSequence, DigitConfig
import numpy as np
from collections.abc import Sequence
from PIL import ImageFont, ImageDraw, Image 


def random_digit_sequence_generator(digit_size,
                                    config_file,
                                    batch=1,
                                    image_size: Sequence[tuple[int,
                                                               int]] = None,
                                    allowed_digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "]):

    while True:
        random_array = np.random.rand(batch, digit_size)*len(allowed_digits)
        random_array = random_array.astype(np.int32)
        # print(np.unique(random_array,return_counts=True))

        annotations = []
        arrays = []
        for row in random_array:
            row = np.take(allowed_digits, row)
            row = "".join(list(map(str, row.tolist())))

            configurations = [DigitConfig.load_config(config_file, x) for x in row]
            digits = DigitSequence(configs=configurations, size=image_size)
            array, annotation = digits.data()
            arrays.append(array)
            annotations.append(annotation)

        yield arrays, annotations

def test_annotations(array,annotation):
    image = Image.fromarray(array)
    draw = ImageDraw.Draw(image)

    for each in annotation["annotations"]:
        draw.rectangle(each["bbox"],
                    outline=tuple([255,82,82]),
                    width=1)

    image.show()

if __name__ == "__main__":
    with open("D:\\ACRA\\ImageGenerationPipeline\\Experiments\\digit_configurations.json","r+",encoding="utf-8") as f0:
        config_file = json.load(f0)

    digit_gen = random_digit_sequence_generator(
        10, config_file, batch=10, image_size=(128,128))
    ret_arr, ret_ann = next(digit_gen)
    ret_arr, ret_ann = next(digit_gen)
    #print(ret_arr[0].shape)
    #print(ret_ann[0])
    test_annotations(ret_arr[0],ret_ann[0])
