from PIL import Image
import argparse
import blessed
import asciilib


term = blessed.Terminal()
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of image")
parser.add_argument("--size", "-S", type=int, help="Integer of X pixels", default=term.height - 2)
args = parser.parse_args()

invert = False
im_pil = Image.open(args.filename)
print(asciilib.create_ascii_image(im_pil, args.size, invert))