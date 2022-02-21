import os

from PIL import Image


def get_file(file_name):
    return file_name
    # return args.base_dir + "/" + file_name


class Tileset:
    def __init__(self, name):
        self.name = name


class ResTool:

    def __init__(self, src_files_directory='.'):
        print("Working directory:", os.getcwd())
        self.src_files_directory = src_files_directory
        self.pal_data = None
        self.current_img = None

        self.tile_file = open("{}/res_tiles_generated.s".format(self.src_files_directory), "w")
        self.header_file = open("{}/res_generated.h".format(self.src_files_directory), "w")
        self.res_file = open("{}/res_generated.c".format(self.src_files_directory), "w")

        self.write_res("#include")

        self.tile_sets = []

        self.total_tile_index = 0

        self.write_tile(".align 2")
        self.write_tile(".globl TILES")
        self.write_tile("TILES:")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closing...")
        self.tile_file.close()
        self.header_file.close()
        self.res_file.close()

    def generate_empty_palette(self, default_color=(0, 0, 0)):
        return [default_color] * 16

    def write_tile(self, s):
        self.tile_file.write("{}\n".format(s))

    def write_res(self, s):
        self.res_file.write("{}\n".format(s))

    def use_palette(self, pal):
        self.pal_data = pal
        print("pal", self.pal_data)

    def use_palette_from_image(self, file_path):
        path = get_file(file_path)
        print("Using palette ", path)

        img = Image.open(path)
        self.use_palette([x for x in img.getdata()])

    def use_image(self, image):
        self.current_img = image

    def use_image_file(self, img_file):
        path = get_file(img_file)
        print("Using image file", path)
        self.use_image(Image.open(path))

    def begin_tileset(self, name) -> Tileset:
        tileset = Tileset(name)
        # self.current_set = {"name": name, "num_tiles": 0, "tile_no": self.total_tile_index}
        self.tile_sets.append(tileset)
        tile_index = 0
        return tileset

    def transfer_region(self, sprite_src_x, sprite_src_y, sprite_tile_w, sprite_tile_h):
        # width and height are in tiles

        for x in range(0, sprite_tile_w):
            for y in range(0, sprite_tile_h):
                # print(x, y, sprite_tile_w, sprite_tile_h)
                left = sprite_src_x + x * 8
                top = sprite_src_y + y * 8
                r = (left, top, left + 8, top + 8)
                region = self.current_img.crop(r)
                val = 0
                # print(img_data, len(img_data))
                for pixel_idx, pixel in enumerate(region.getdata()):

                    try:
                        idx = self.pal_data.index(pixel)
                    except ValueError:
                        print("Warning: Color {} not found in palette".format(pixel))
                        idx = 0

                    val = (val << 4) | idx

                    # sys.stdout.write("{}, ".format(hex(idx)))

                    if (pixel_idx + 1) % 8 == 0:
                        s = "dc.l 0x{:08X}".format(val, 10)
                        # s = "dc.l ${0:#0{1}x}".format(val, 10)
                        self.write_tile(s)
                        # if pixel_idx != len(img_data)-1:
                        # write_out(s)
                        val = 0

    # def begin_state(self, name):
    #     current_state = {"name": name, "sprites": ["", "", "", ""], "set": self.current_set["name"]}
    #     sprite_states.append(current_state)
