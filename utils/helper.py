from PIL import ImageDraw, Image 

def test_annotations(array,annotation):
    image = Image.fromarray(array)
    draw = ImageDraw.Draw(image)

    for each in annotation["annotations"]:
        draw.rectangle(each["bbox"],
                    outline=tuple([255,82,82]),
                    width=1)

    image.show()