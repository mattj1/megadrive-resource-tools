from PIL import Image
import argparse
import sys
import os


def write_header(s):
    headerfile.write(s)
    # sys.stdout.write(s)


def write_out(s):
    myfile.write(s)
    # sys.stdout.write(s)


def process_palette(pal_data, name='palette'):
    # RGB
    
    write_header("extern const u32 {}_RGB[16];\n".format(name))
    
    write_out("const u32 {}_RGB[16] = \n".format(name));
    
    write_out("{\n");
    for c in pal_data:
        write_out("\t{},\n".format(hex(c[0]<<16 | c[1] << 8 | c[2])))
    
    write_out("};\n")

    # VDP

    write_header("extern const u16 {}[16];\n".format(name))

    write_out("const u16 {}[16] = \n".format(name));

    write_out("{\n");
    for c in pal_data:
        write_out("\tRGB24_TO_VDPCOLOR({}),\n".format(hex(c[0]<<16 | c[1] << 8 | c[2])))

    write_out("};\n")

parser = argparse.ArgumentParser()
parser.add_argument("pal", help="16x1 24-bit BMP file")

args = parser.parse_args()

print("Process palette", args.pal)

im = Image.open(args.pal)
pal_data = [x for x in im.getdata()]

# for pixel in pal_data:
#      print(pixel)

bn = os.path.basename(args.pal)
fn = os.path.splitext(bn)
#print(fn[0])

headerfile = open("src/res/res.h", "a")
myfile = open("src/res/res.c", "a")

process_palette(pal_data, name=fn[0])
myfile.close()
headerfile.close()

