#!/usr/bin/python
import pygame
from PIL import Image, ImageOps
import cv2
import argparse

size = 500


def create_rects(og_image):

    image = og_image

    if significant_axis == 0:
        image: Image.Image = image.resize(
            (args.size, round((args.size / image.size[0]) * image.size[1]))
            )
    else:
        image: Image.Image = image.resize(
            (
                round((args.size / image.size[1]) * image.size[0]), args.size))

    data = image.convert("RGB").getdata()
    pixel_width = round(size / image.size[1], 2) - 1
    global window
    window = pygame.display.set_mode((round(pixel_width * image.size[0]), round(pixel_width * image.size[1])))
    x = 0
    y = 0
    pixel_width += 1
    frames_through = 0
    for frame in data:
        r = pygame.Rect(x, y, pixel_width, pixel_width)
        pygame.draw.rect(window, frame, r)
        x += pixel_width - 1
        frames_through += 1
        if frames_through == image.width:
            y += pixel_width - 1
            x = 0
            frames_through = 0
    pygame.display.flip()

parser = argparse.ArgumentParser()

parser.add_argument("--filename", "-F", type=str, help="filename of file to use", default="none")
parser.add_argument("--size", "-S", type=int,
                    help="size of image in pixrels", default=25)
parser.add_argument("--greyscale", "-G", action="store_true", help="greyscale image?")
parser.add_argument("--video", "-V", action="store_true", help="set to use webcam video")

args = parser.parse_args()

if args.video:
    if args.filename != "none":
        stream = cv2.VideoCapture(args.filename)
    else:
        stream = cv2.VideoCapture(0)

if not args.video:
    og_image = Image.open(args.filename)

    if args.greyscale:
        og_image = og_image.convert("L")


significant_axis = 1



window = pygame.display.set_mode((size, size))
SIZE_INCREASER = 5
CLOCK_SPEED = 30
if not args.video:
    pygame.display.set_caption(args.filename)
    create_rects(og_image)
clock = pygame.time.Clock()
increase_size = 0
increase_quality = 0
while True:
    if args.video:
        code, frame = stream.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        og_image = ImageOps.mirror(im_pil)
        if args.greyscale:
            og_image = og_image.convert("L")
        create_rects(og_image)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                increase_size = SIZE_INCREASER
            elif event.key == pygame.K_LEFT:
                increase_size = -SIZE_INCREASER
            if event.key == pygame.K_UP:
                increase_quality = SIZE_INCREASER
                increase_size = SIZE_INCREASER
            elif event.key == pygame.K_DOWN:
                increase_quality = -SIZE_INCREASER
                increase_size = -SIZE_INCREASER
            elif event.key == pygame.K_g:
                print(args.size)
            elif event.key == pygame.K_s:
                incsize = input("size? ")
                args.size = int(incsize)
                create_rects(og_image)
            elif event.key == pygame.K_SPACE:
                args.greyscale = not args.greyscale
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                increase_size = 0
            if event.key == pygame.K_LEFT:
                increase_size = 0
            if event.key == pygame.K_UP:
                increase_quality = 0
                increase_size = 0
            if event.key == pygame.K_DOWN:
                increase_size = 0
                increase_quality = 0

    if increase_size != 0 or increase_quality != 0:
        if args.size < 10 and increase_quality < 0:
            increase_size = 0
            increase_quality = 0
        size += increase_size
        
        args.size += increase_quality
        create_rects(og_image)
    
    clock.tick(CLOCK_SPEED)

    #if clock.get_fps() <CLOCK_SPEED:
    #    print("AAAAA! TOO MUCH!")
