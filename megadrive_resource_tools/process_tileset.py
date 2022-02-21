from PIL import Image
import argparse
import sys
import os

def write_header(s):
    headerfile.write(s)
    #sys.stdout.write(s)

def write_out(s):
    myfile.write(s)
    #sys.stdout.write(s)

def process_tile(img_data, pal_data):
    val = 0

    for pixel_idx, pixel in enumerate(img_data):
        
        try:
            idx = pal_data.index(pixel)
        except ValueError:
            print("process_tileset: Warning: Color {} not found in palette".format(pixel))
            idx = 0

        val = (val << 4) | idx

    #sys.stdout.write("{}, ".format(hex(idx)))

        if (pixel_idx+1) % 8 == 0:
            s = "\t{0:#0{1}x},\n".format(val, 10)
            #if pixel_idx != len(img_data)-1:
            write_out(s)
            val = 0

def process_tilemap(img, pal_data, name='tileset'):
    img_data = img.getdata()
    num_tiles = img.width/8 * img.height/8
    print("Process tilemap:", img.width, img.height)
    write_header("extern const u32 {}[{}*8];\n".format(name, num_tiles))
    write_out("const u32 {}[{}*8] = \n".format(name,num_tiles))
    write_out("{\n")
    for y in range(0, img.height, 8):
        for x in range(0, img.width, 8):
            write_out("\t // Tile at {}, {}\n".format(x, y))
            region = img.crop((x, y, x + 8, y + 8))
            process_tile(region.getdata(), pal_data)

    write_out("};\n")

parser = argparse.ArgumentParser()
parser.add_argument("pal", help="16x1 24-bit BMP file")
parser.add_argument("img", help="24-bit BMP file (tiles)")

args = parser.parse_args()

im = Image.open(args.pal)
pal_data = [x for x in im.getdata()]


img = Image.open(args.img)

bn = os.path.basename(args.img)
fn = os.path.splitext(bn)
# print(fn[0])

headerfile = open("src/res/res.h", "a")
myfile = open("src/res/res.c", "a")
process_tilemap(img, pal_data, name=fn[0])
myfile.close()
headerfile.close()

