import os
from PIL import Image, ImageDraw


def saveWalls(img, names, path):
    for n in names:
        img.save(path + n + ".png")
        img = img.rotate(angle=90)


if __name__ == '__main__':
    c = 64
    d = 54
    r = c-d
    name = "pack_1"

    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    WHITE = (255, 255, 255, 255)
    BLACK = (0, 0, 0, 0)

    try:
        os.mkdir(name)
    except FileExistsError:
        pass

    path = name+"/"

    img = Image.new('RGBA', (c, c), color=WHITE)
    img.save(path+"0.png", format='png')

    img = Image.new('RGBA', (c, c), color=WHITE)
    imgd = ImageDraw.ImageDraw(img)

    imgd.ellipse((-r-1, -r-1, r-1, r-1), fill=BLACK)

    saveWalls(img, ["1", "2", "3", "4"], path)

    img = Image.new('RGBA', (c, c), color=BLACK)
    imgd = ImageDraw.ImageDraw(img)
    imgd.rectangle((0, 0, d-1, d-r), fill=WHITE)
    imgd.rectangle((0, 0, d-r, d-1), fill=WHITE)
    imgd.ellipse((d-2*r-1, d-2*r-1, d-1, d-1), fill=WHITE)

    saveWalls(img, ["5", "6", "7", "8"], path)

    img = Image.new('RGBA', (c, c), color=WHITE)
    imgd = ImageDraw.ImageDraw(img)
    imgd.rectangle((0, c, c, d), fill=BLACK)

    saveWalls(img, ["a", "b", "c", "d"], path)

    img = Image.new('RGBA', (c, c), color=BLACK)
    imgd = ImageDraw.ImageDraw(img)
    imgd.rectangle((r, r*2, d-1, d-r), fill=WHITE)
    imgd.rectangle((r*2, r, d-r, d-1), fill=WHITE)

    imgd.ellipse((r, r, r*3, r*3), fill=WHITE)
    imgd.ellipse((r, d-r*2-1, r*3, d-1), fill=WHITE)
    imgd.ellipse((d-r*2-1, r, d-1, r*3), fill=WHITE)
    imgd.ellipse((d-r*2-1, d-2*r-1, d-1, d-1), fill=WHITE)

    img.save(path+"e.png", format='png')

