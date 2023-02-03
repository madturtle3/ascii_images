#!/usr/bin/env python
from asciilib import create_ascii_color_image, create_ascii_image, create_ascii_mono_image, echo
from PIL import Image, ImageOps, ImageFilter
import argparse
import blessed
import cv2
import sys
import os
import time
import numpy
sys.path.append(os.path.abspath(__file__))


term = blessed.Terminal()
term.number_of_colors = 1 << 24
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str,
                    help="filename to use. If webcam, use 0.")
parser.add_argument("--mode", "-M", type=str, choices=[
                    "v", "p"], default="p", help="Mode of terminal. Either <v>ideo or <p>icture")
parser.add_argument("--color", "-C", type=str, choices=[
                    "c", "g", "m"], default="g", help="color type. <g>reyscalse or <c>olor")
parser.add_argument("--size", "-S", type=int,
                    help="height of image displayed. Default is terminal height.", default=term.height)
parser.add_argument(
    "--invert", "-I", help="invert image or no", action="store_true")
parser.add_argument("--contrast", "-O", type=int,
                    help="set contrast on monochromatic images", default=10)
parser.add_argument("--framerate", "-F",
                    help="framerate of camera. Default is 30.", default=30, type=int)

args = parser.parse_args()
crop = [0, 0, 100, 100]

if args.mode == "p":
    im_pil = Image.open(args.filename)
    if args.color == "g":
        print(create_ascii_image(im_pil, args.size, invert=args.invert))
    elif args.color == "c":
        if args.invert:

            print(create_ascii_color_image(im_pil, args.size, invert=True))
        else:
            print(create_ascii_color_image(im_pil, args.size, invert=False))
    elif args.color == "m":
        print(create_ascii_mono_image(im_pil, args.size, args.contrast, args.invert))


elif args.mode == "v":
    frame_period = 1 / args.framerate
    spaced = False
    last_iter = 0
    time_passed = 0
    override = False
    if not args.filename.isdigit():
        feed = cv2.VideoCapture(args.filename)
    else:
        feed = cv2.VideoCapture(int(args.filename))
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():

        while True:

            code, frame = feed.read()

            key = term.inkey(timeout=0)
            if key != "":
                override = True

            if key == " ":
                spaced = not spaced
            elif key == "w":
                args.contrast += 5
            elif key == "s":
                args.contrast -= 5
            elif key == "a":
                if args.size > 1 or args.size > term.height:
                    args.size -= 1
            elif key == "d":
                args.size += 1
            elif key == "c":
                echo(term.clear + term.normal)
            elif key == "b":
                args.color = "c"
            elif key == "n":
                args.color = "g"
            elif key == "m":
                args.color = "m"
            elif key == "i":
                args.invert = not args.invert
            elif key == "1":
                crop[0] += 10
            elif key == "2":
                crop[0] -= 10
            elif key == "y":
                crop[1] -= 10
            elif key == "h":
                crop[1] += 10
            elif key == "3":
                crop[2] -= 10
            elif key == "4":
                crop[2] += 10
            elif key == "t":
                crop[3] -= 10
            elif key == "g":
                crop[3] += 10
            elif key == "r":
                crop = [0, 0, og_size[0], og_size[1]]
            crop = numpy.abs(crop)
            if (not spaced and time.time() - last_iter > frame_period) or override:
                echo(
                    term.move_yx(0, 0))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(img)
                og_size = im_pil.size
                im_pil = ImageOps.mirror(im_pil)
                im_pil = im_pil.crop(crop)
                if override:
                    echo(term.clear)
                if args.color == "g":
                    text = create_ascii_image(
                        im_pil, args.size, invert=args.invert)
                elif args.color == "c":
                    text = create_ascii_color_image(
                        im_pil, args.size, invert=args.invert)
                elif args.color == "m":
                    text = create_ascii_mono_image(
                        im_pil, args.size, args.contrast, invert=args.invert)
                print(text)
                last_iter = time.time()
                override = False

            if key == "s":
                with open("picture.txt", "w") as picturefile:
                    picturefile.write(text)
