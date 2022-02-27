import PIL.Image
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from megadrive_resource_tools.restool import ResTool

letter_dim = 16
font = ImageFont.truetype(r'pixel font-7.ttf', 20)
# img = Image.new('RGB', (letter_dim, letter_dim), color=(0, 255, 255))
# img2 = Image.new('RGB', (letter_dim, letter_dim), color=(0, 255, 255))
# draw = ImageDraw.Draw(img)
# draw.text((0, 0), 'A', (255, 255, 255), font=font)
# img = img.resize((8, 16), resample=PIL.Image.NEAREST)
# img2.paste(img)
# img2.show()
# exit()
with ResTool() as restool:


    # restool.use_palette_from_image('/Users/mattj/projects/wordle-md/dev/tiles.png')
    pal = restool.generate_empty_palette()
    pal[0] = (0, 255, 255)
    pal[1] = (0, 0, 0)
    pal[2] = (58, 58, 60)
    pal[3] = (83, 142, 78)
    pal[4] = (181, 159, 58)
    pal[15] = (255, 255, 255)
    restool.use_palette(pal)

    # restool.use_image_file('/Users/mattj/projects/wordle-md/dev/tiles.png')
    restool.use_image_file('c:/Users/matt/Documents/GitHub/wordle-md/dev/tiles.png')

    with restool.begin_tileset('CURSOR') as tileset:
        # Cursor
        tileset.transfer_region(0, 16, 2, 2)
    # Gray, orange, green, empty
    with restool.begin_tileset('WORD_TILES_FILLED') as tileset:
        for i in range(0, 4):
            tileset.transfer_region(0, 32 + 24 * i, 3, 3)

    with restool.begin_tileset('WORD_TILES_OUTLINE') as tileset:
        for i in range(0, 4):
            tileset.transfer_region(24, 32 + 24 * i, 3, 3)

    with restool.begin_tileset('MISC') as tileset:
        tileset.transfer_region(0, 0, 1, 1)

    sizes = ((16, 16), (12, 16), (8, 16), (4, 16))
    with restool.begin_tileset('LARGE_FONT') as tileset:
        # font = ImageFont.truetype(r'gameovercre1.ttf', 16)

        for i in range(ord('A'), ord('Z') + 1):
            # print(chr(i))
            img = Image.new('RGB', (letter_dim, letter_dim), color=(0, 255, 255))
            draw = ImageDraw.Draw(img)

            bb = draw.textbbox(xy=(0, 0), text=chr(i), font=font)
            draw.text((letter_dim/2 - bb[2] / 2, letter_dim/2 - bb[3] / 2), chr(i), (255, 255, 255), font=font)

            for size in sizes:
                img2 = Image.new('RGB', (letter_dim, letter_dim), color=(0, 255, 255))
                letter_resized = img.resize(size=size, resample=PIL.Image.NEAREST)
                img2.paste(letter_resized, (int(letter_dim/2 - size[0]/2), 0))

                restool.use_image(img2)
                tileset.transfer_region(0, 0, 2, 2)

                # img2.show()

                # letter_resized.show()
            # exit()

    # img.show()
