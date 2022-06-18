#!/usr/bin/env python
from PIL import Image, ImageOps
import argparse
import blessed
import cv2
import sys
import os
sys.path.append(os.path.abspath(__file__))
from asciilib import create_ascii_color_image, create_ascii_image, echo

term = blessed.Terminal()
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="filename to use. If webcam, use 0.")
parser.add_argument("--mode", "-M", type=str, choices=["v", "p"], default="p", help="Mode of terminal. Either <v>ideo or <p>icture")
parser.add_argument("--color", "-C", type=str, choices=["c", "g"], default="g", help="color type. <g>reyscalse or <c>olor")
parser.add_argument("--size", "-S", type=int, help="height of image displayed. Default is terminal height.", default=term.height)
args = parser.parse_args()

if args.mode == "p":
    im_pil = Image.open(args.filename)
    if args.color == "g":
        print(create_ascii_image(im_pil, args.size))
    elif args.color == "c":
        print(create_ascii_color_image(im_pil, args.size))


elif args.mode == "v":
    if not args.filename.isdigit():
        feed = cv2.VideoCapture(args.filename)
    else:
        feed = cv2.VideoCapture(int(args.filename))
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():

        while True:
            echo(
            term.move_yx(0,0))
            code, frame = feed.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            im_pil = ImageOps.mirror(im_pil)
            if args.color == "g":
                print(create_ascii_image(im_pil, args.size))
            elif args.color == "c":
                print(create_ascii_color_image(im_pil, args.size))