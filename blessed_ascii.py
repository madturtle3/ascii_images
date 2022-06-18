from PIL import Image, ImageOps
import argparse
import blessed
import cv2
import asciilib




term = blessed.Terminal()
feed = cv2.VideoCapture(0)
log = open("log.txt", "a")
parser = argparse.ArgumentParser()
parser.add_argument("--size", "-S", type=int, help="Integer of X pixels", default=term.height)
args = parser.parse_args()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():

    while True:
        asciilib.echo(
        term.move_yx(0,0))
        code, frame = feed.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        im_pil = ImageOps.mirror(im_pil)

        print(asciilib.create_ascii_image(im_pil, args.size))