import os.path

import numpy as np
import requests
from PIL import ImageDraw, Image
from numpy import random
import gdown

from .config import CHUNK_SIZE


def randomly_insert(row, num_times, character):
    arr_char = np.full(num_times, character)
    tot_arr = np.concatenate((row, arr_char))
    random.shuffle(tot_arr)
    return tot_arr


def split_insert(row, sectors, spaces_per_sector, digit_size, character):
    gap = digit_size // sectors
    for gap_num in range(1, sectors):
        for _ in range(spaces_per_sector):
            row = np.insert(row, gap_num * gap + (gap_num - 1) * spaces_per_sector, character)

    return row


def add_spaces(row, space_type, spaces, sectors, spaces_per_sector, digit_size):
    if space_type == "random":
        assert spaces
        row = randomly_insert(row, spaces, " ")

    if space_type == "space":
        assert sectors
        assert spaces_per_sector

        row = split_insert(row, sectors, spaces_per_sector, digit_size, " ")

    return row


def generate_random_digits(digit_size, allowed_digits, space_type, spaces, sectors, spaces_per_sector):
    random_array = np.random.rand(digit_size) * len(allowed_digits)
    random_array = random_array.astype(np.int32)
    row = np.take(allowed_digits, random_array)

    row = add_spaces(row, space_type, spaces, sectors, spaces_per_sector, digit_size)

    row = "".join(list(map(str, row.tolist())))

    return row


def test_annotations(array, annotation):
    array = array.astype(np.uint8)
    image = Image.fromarray(array)
    draw = ImageDraw.Draw(image)

    for each in annotation:
        draw.rectangle(each["bbox"],
                       outline=tuple([255, 82, 82]),
                       width=1)

    image.show()


def format_annotations(full_ann, row_ann):
    if len(full_ann["annotations"]) == 0:
        current_id = 0
        current_img_id = 0
    else:
        current_id = full_ann["annotations"][-1]["id"] + 1
        current_img_id = full_ann["annotations"][-1]["image_id"] + 1

    for __id, ann in enumerate(row_ann):
        ann["id"] = current_id + __id
        ann["image_id"] = current_img_id

        full_ann["annotations"].append(ann)


def download_font_from_gdrive(__id,download_loc):
    try:
        if not os.path.exists(download_loc):
            gdown.download(id=__id, output=download_loc)

        return True
    except Exception as e:
        return False
