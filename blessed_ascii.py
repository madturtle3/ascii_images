from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import argparse
import blessed
import cv2
import math

def echo(text):
    print(text, end="", flush=True)

def get_saturaiton(image_list):
    return round(sum(image_list) / len(image_list))

def reduce_background(image_list):
    new_image_list = []
    print(get_saturaiton(image_list))
    for pixel in image_list:
        new_pixel = pixel
        if pixel < (255 * (3/4)) and pixel > (255 * (1/4)):
            new_pixel *= 1.25
        new_image_list.append(new_pixel)
    return new_image_list

def to_grayscale(array):
    grey_pixel = 0
    gray_array = []
    for item in array:
        grey_pixel = round(item[0] * .21) + round(item[1] * .072) + round(item[2] * .07)
        gray_array.append(grey_pixel)
    return gray_array


"""
Here's the deal:
1. load image and convert to greyscale
2. Convert to low res photo WITH same Aspect Ratio
3. Convert to ascii based on intensity of pixel"""


parser = argparse.ArgumentParser()
parser.add_argument("--size", "-S", type=int, help="Integer of X pixels", default=125)
parser.add_argument("--contrast", "-C", type=int, help="How darkened the image should be.", default=10)
args = parser.parse_args()

def create_ascii_image(image, size=150, contrast=10, invert=False):
    ascii_photo = ""
    photo_size = size
    xpixels = photo_size

    xpix, ypix = image.size
    ypixels = round(xpix/ypix * photo_size * 2) # gotta round for that precision!
    new_img = image.resize((ypixels, xpixels), Image.Resampling.LANCZOS)
    #new_img = new_img.convert("L")
    new_img = ImageOps.grayscale(new_img)
    new_img = ImageEnhance.Color(new_img).enhance(2)
    comp_img = new_img.filter(ImageFilter.FIND_EDGES).getdata()
    imglist = new_img.getdata()
    new_imglist = []
    for pixel, edge_pixel in zip(imglist, comp_img):
        new_imglist.append(abs(pixel - edge_pixel))
    imglist = new_imglist
        
    #imglist = reduce_background(imglist)
    saturation = round(get_saturaiton(imglist) ** 1.25)

    density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{\}[]?-_+~<>>i!lI;:,\"^`'.  "
    
    density += " " * contrast
    density = density[::-1]
    if invert:
        density = density[::-1]
    for pixel in imglist:
        ascii_val = round(math.sqrt((len(density) ** 2 / 255) * pixel) - 1)
        #ascii_val = round(((len(density) / 255)) * pixel) - 1)
        ascii_photo += density[ascii_val]
        if len(ascii_photo) % (ypixels + 1)== 0:
            ascii_photo += "\n"
    return ascii_photo

term = blessed.Terminal()
feed = cv2.VideoCapture(0)
contrast = args.contrast
invert = False
log = open("log.txt", "a")
with term.fullscreen(), term.cbreak(), term.hidden_cursor():

    while True:
        if term.kbhit(0):
            key = term.inkey()
            if key.name == "KEY_UP":
                contrast += 1
            if key.name == "KEY_DOWN":
                if contrast > 1:
                    contrast -= 1
            if key == "i":
                invert = not invert
        echo(
        term.move_yx(0,0))
        code, frame = feed.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        im_pil = ImageOps.mirror(im_pil)

        print(create_ascii_image(im_pil, term.height, contrast, invert))