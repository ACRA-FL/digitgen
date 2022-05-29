from PIL import ImageDraw, Image 
import numpy as np
from numpy import random

def randomly_insert(row,num_times,character):
    arr_char = np.full((num_times),character)
    tot_arr = np.concatenate((row,arr_char))
    random.shuffle(tot_arr)
    return tot_arr

def split_insert(row,sectors,spaces_per_sector,digit_size,character):
    gap = digit_size//(sectors-1)
    for gap_num in range(1,sectors):
        np.insert(row, gap_num*gap, character)
        
    return row


def add_spaces(row,space_type,spaces,sectors,spaces_per_sector,digit_size):
    if space_type == "random":
        assert spaces
        row = randomly_insert(row,spaces," ")

    if space_type == "space":
        assert sectors
        assert spaces_per_sector

        row = split_insert(row,sectors,spaces_per_sector,digit_size," ")




    return row



def generate_random_digits(digit_size,allowed_digits,space_type,spaces,sectors,spaces_per_sector):
    random_array = np.random.rand(digit_size)*len(allowed_digits)
    random_array = random_array.astype(np.int32)
    row = np.take(allowed_digits, random_array)

    row = add_spaces(row,space_type,spaces,sectors,spaces_per_sector,digit_size)

    row = "".join(list(map(str, row.tolist())))

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
