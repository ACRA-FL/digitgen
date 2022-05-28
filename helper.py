from random import random
from PIL import ImageDraw, Image 
import numpy as np

def generate_random_digits(digit_size,allowed_digits,spaces="None"):
    random_array = np.random.rand(digit_size)*len(allowed_digits)
    random_array = random_array.astype(np.int32)
    row = np.take(allowed_digits, random_array)
    row = "".join(list(map(str, row.tolist())))

    if spaces == random

    return row


def test_annotations(array,annotation):
    image = Image.fromarray(array)
    draw = ImageDraw.Draw(image)

    for each in annotation:
        draw.rectangle(each["bbox"],
                    outline=tuple([255,82,82]),
                    width=1)

    image.show()


def format_annotations(full_ann,row_ann):
    if len(full_ann["annotations"]) == 0:
        current_id = 0
        current_img_id = 0
    else:
        current_id = full_ann["annotations"][-1]["id"] + 1
        current_img_id = full_ann["annotations"][-1]["image_id"] + 1
        
    for __id,ann in enumerate(row_ann):
        ann["id"] = current_id+__id
        ann["image_id"] = current_img_id

        full_ann["annotations"].append(ann)
