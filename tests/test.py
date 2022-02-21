from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from megadrive_resource_tools.restool import ResTool

with ResTool() as restool:
    letter_dim = 16

    # restool.use_palette_from_image('/Users/mattj/projects/wordle-md/dev/tiles.png')
    pal = restool.generate_empty_palette()
    pal[0] = (0, 255, 255)
    pal[1] = (0, 0, 0)
    pal[2] = (58, 58, 60)
    pal[3] = (83, 142, 78)
    pal[4] = (181, 159, 58)
    pal[15] = (255, 255, 255)
    restool.use_palette(pal)

    restool.begin_tileset('MAIN')

    restool.use_image_file('/Users/mattj/projects/wordle-md/dev/tiles.png')

    # Cursor
    restool.transfer_region(0, 16, 2, 2)

    for i in range(0, 4):
        # Gray, orange, green, empty
        restool.transfer_region(32 + 24 * i, 8, 3, 3)

    # font = ImageFont.truetype(r'gameovercre1.ttf', 16)
    font = ImageFont.truetype(r'pixel font-7.ttf', 20)

    for i in range(ord('A'), ord('Z') + 1):
        # print(chr(i))
        img = Image.new('RGB', (letter_dim, letter_dim), color=(0, 255, 255))
        draw = ImageDraw.Draw(img)

        bb = draw.textbbox(xy=(0, 0), text=chr(i), font=font)
        draw.text((letter_dim/2 - bb[2] / 2, letter_dim/2 - bb[3] / 2), chr(i), (255, 255, 255), font=font)

        restool.use_image(img)
        restool.transfer_region(0, 0, 2, 2)

    img.show()
