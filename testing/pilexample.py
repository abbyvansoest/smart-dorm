import sys
from PIL import Image, ImageDraw

im = Image.open("image.png")

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw

# write to stdout
im.save('draw.jpg')