from PIL import Image
import argparse
import sys
import os

current_set = None
current_state = None
current_pal = None
current_img = None
tile_index = 0

total_tile_index = 0

tile_sets = []
sprite_states = []
sprites = []
sprites_dict = {}
tiledata_lines = []

pal_data = None

def write_header(s):
    headerfile.write(s)
    #sys.stdout.write(s)

def write_out(s):
    myfile.write(s)
    #sys.stdout.write(s)

def write_tile(s):
    tilefile.write(s)
    #sys.stdout.write(s)

def process_tile2(img_data):
    val = 0
    #print(img_data, len(img_data))
    for pixel_idx, pixel in enumerate(img_data):
        
        try:
            idx = pal_data.index(pixel)
        except ValueError:
            print("Warning: Color {} not found in palette".format(pixel))
            idx = 0

        val = (val << 4) | idx

    #sys.stdout.write("{}, ".format(hex(idx)))

        if (pixel_idx+1) % 8 == 0:

            s = "{0:#0{1}x},".format(val, 10)
            tiledata_lines.append(s)
            #if pixel_idx != len(img_data)-1:
            # write_out(s)
            val = 0

def process_tile(sprite_src_x, sprite_src_y, sprite_tile_w, sprite_tile_h):
    # current_img and pal_data is already loaded
    
    for x in range(0, sprite_tile_w):
        for y in range(0, sprite_tile_h):
            # print(x, y, sprite_tile_w, sprite_tile_h)
            left = sprite_src_x + x * 8
            top = sprite_src_y + y * 8
            r = (left, top, left + 8, top + 8)
            region = current_img.crop(r)
            process_tile2(region.getdata())
                
def process_tilemap():
    # img_data = img.getdata()
    num_tiles = current_img.width/8 * current_img.height/8
    print("Process tilemap:", current_img.width, current_img.height)

    for y in range(0, current_img.height, 8):
        for x in range(0, current_img.width, 8):
            region = current_img.crop((x, y, x + 8, y + 8))
            process_tile2(region.getdata())

    return num_tiles


def get_file(file_name):
    return args.base_dir + "/" + file_name

def parse_script_file(abs_path):
    print("Parse script file: {}".format(abs_path))
    
    global total_tile_index
    global pal_data
    global current_img

    with open(abs_path, "r") as script_file:
        
        lines = [x.strip() for x in script_file.readlines()]
        lines = [x for x in lines if not x.startswith("#")]
        lines = [x for x in lines if len(x) > 0]
        #print lines

        for line in lines:
            p = line.split()
            cmd = p[0]
            #print(p)

            if cmd == 'SET':
                current_set = {"name": p[1], "num_tiles":0, "tile_no":total_tile_index}
                tile_sets.append(current_set)
                tile_index = 0

                # print("Start set ", current_set)

            if cmd == 'STATE':
                current_state = {"name": p[1], "sprites":["", "", "", ""], "set":current_set["name"] }
                sprite_states.append(current_state)

                # print("Start state ", current_state)

            if cmd == 'PAL':
                current_pal = Image.open(get_file(p[1]))
                pal_data = [x for x in current_pal.getdata()]
                print("Using palette ", get_file(p[1]))
                print("Using palette img", current_pal)

            if cmd == 'IMG':
                current_img = Image.open(get_file(p[1]))
                print("Using image ", get_file(p[1]))
                print("Using img img", current_img)

            if cmd == 'SPRITE':
                sprite_dir = int(p[1])
                sprite_name = "{}_{}".format(current_state["name"], sprite_dir)

                # current_state["sprites"].append(sprite_name)
                current_state["sprites"][sprite_dir] = sprite_name

                if p[2] == 'USE':
                    other_index = int(p[3])
                    

                    sprite = dict( sprites_dict["{}_{}".format(current_state["name"], other_index)] )

                    if len(p) >= 5:
                        flip_type = p[4]
                        if flip_type:
                            if flip_type == 'HFLIP':
                                sprite["h_flip"] = 1

                            if flip_type == 'VFLIP':
                                sprite["v_flip"] = 1
                else:
                    sprite_tile_w = int(p[2])
                    sprite_tile_h = int(p[3])
                    sprite_src_x = int(p[4])
                    sprite_src_y = int(p[5])
                    sprite_origin_x = int(p[6])
                    sprite_origin_y = int(p[7])

                    sprite = {
                        "ox":sprite_origin_x,
                        "oy":sprite_origin_y,
                        "size":(sprite_tile_w, sprite_tile_h),
                        "h_flip":0,
                        "v_flip":0,
                        # "info": "SPRITE_SIZE({},{})".format(sprite_tile_w, sprite_tile_h),
                        "tile_index":tile_index
                        }

                    # print("Generate:", sprites)
                    tiledata_lines.append("// Tile data for sprite {}".format(sprite_name))
                    process_tile(sprite_src_x, sprite_src_y, sprite_tile_w, sprite_tile_h)

                    num_tiles = (sprite_tile_w * sprite_tile_h)
                    tile_index += num_tiles
                    total_tile_index += num_tiles

                current_set["num_tiles"] = tile_index

                sprite["name"] = sprite_name
                sprites.append(sprite)
                sprites_dict[sprite_name] = sprite

                # print("Generate {{ {}, {}, {}, {} }} // {} > {}".format(sprite_origin_x, sprite_origin_y, 0, tile_index, current_set, sprite_name))

            if cmd == 'LOADTILES':
                tiledata_lines.append("// Tile data for tileset {}".format(current_set["name"]))
                num_tiles = process_tilemap()
                current_set["num_tiles"] = num_tiles
                total_tile_index += num_tiles


parser = argparse.ArgumentParser()
parser.add_argument("script", help="script file")
parser.add_argument("base_dir", help="base dir")

args = parser.parse_args()

# print(args)
parse_script_file(args.script)

tilefile = open("src/res/res_tiles.c", "w")
headerfile = open("src/res/res.h", "w")
myfile = open("src/res/res.c", "w")

# print("\nTile sets:")
# print(tile_sets)

# print("\nSprite states:")
# print(sprite_states)

# print("\nPhysical sprites:")
# print(sprites)

# res.c
write_out("#include \"../common.h\"\n")

write_tile("#include \"../common.h\"\n")

#write_header("#include <genesis.h>\n")

for idx, val in enumerate(tile_sets):
    write_header("#define {} {}\n".format(val["name"], idx))

for idx, val in enumerate(sprite_states):
    write_header("#define {} {}\n".format(val["name"], idx))

for idx, val in enumerate(sprites):
    write_header("#define {} {}\n".format(val["name"], idx))

write_header("extern const u32 tiles[{}*8];\n".format(int(total_tile_index)))

write_out("struct tile_set_t tile_sets[{}] = {{\n".format(len(tile_sets)))
write_header("extern struct tile_set_t tile_sets[{}];\n".format(len(tile_sets)))
write_header("extern struct sprite_state_t sprite_states[{}];\n".format(len(sprite_states)))
write_header("extern struct sprite_info_t sprite_infos[{}];\n".format(len(sprites)))

for ts in tile_sets:
    write_out("\t{{ {}, {} }}, // {}\n".format(ts["num_tiles"], ts["tile_no"], ts["name"]))
write_out("};\n\n")

write_out("struct sprite_state_t sprite_states[{}] = {{\n".format(len(sprite_states)))
for ss in sprite_states:
    write_out("\t{{\t// {}\n".format(ss["name"]))

    write_out("\t\t{{ {}, {}, {}, {} }},\n".format(
        ss["sprites"][0], ss["sprites"][1], ss["sprites"][2], ss["sprites"][3]))

    write_out("\t\t{},\n".format(ss["set"]))

    write_out("\t},\n")

write_out("};\n\n")

write_out("struct sprite_info_t sprite_infos[{}] = {{\n".format(len(sprites)))
for s in sprites:
    sprite_size = s["size"]
    info = "SPRITE_SIZE({},{})".format(sprite_size[0], sprite_size[1])
    if s["h_flip"] == 1:
        info = info + "|0x10"
    if s["v_flip"] == 1:
        info = info + "|0x20"

    write_out("\t{{ {}, {}, {}, {} }}, // {}\n".format(s["ox"], s["oy"], info, s["tile_index"], s["name"]))
write_out("};\n\n")

write_tile("const u32 tiles[{}*8] = {{\n".format(int(total_tile_index)))
for line in tiledata_lines:
    write_tile("\t{}\n".format(line))
write_tile("};\n\n")

# img = Image.open(args.img)

# bn = os.path.basename(args.img)
# fn = os.path.splitext(bn)
# # print(fn[0])

# process_tilemap(img, pal_data, name=fn[0])
myfile.close()
headerfile.close()
tilefile.close()

def process_main():
    print("Test!")
