from PIL import Image
import argparse


def get_saturaiton(image_list):
    return round(sum(image_list) / len(image_list))
"""
Here's the deal:
1. load image and convert to greyscale
2. Convert to low res photo WITH same Aspect Ratio
3. Convert to ascii based on intensity of pixel"""


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Name of image to convert")
parser.add_argument("--size", "-S", type=int, help="Integer of X pixels", default=150)
parser.add_argument("--contrast", "-C", type=int, help="How darkened the image should be.", default=10)
args = parser.parse_args()

def create_ascii_image(filename, size=150, contrast=10):
    with Image.open(filename) as image:
        ascii_photo = ""
        photo_size = size
        ypixels = photo_size

        xpix, ypix = image.size
        xpixels = round(ypix/xpix * photo_size / 2) # gotta round for that precision!
        new_img = image.resize((ypixels, xpixels), Image.Resampling.LANCZOS)
        new_img = new_img.convert("L")
        imglist = new_img.getdata()
        saturation = round(get_saturaiton(imglist) ** 1.25)
        print(saturation, xpix, ypix, xpixels, ypixels)

        density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{\}[]?-_+~<>i!lI;:,\"^`'.  "
        #density =   ".:-=+*#%@"
        #density = density[::-1]
        density += " " * contrast
        if saturation > 200:
            density = density[::-1]
        
        for pixel in imglist:
            ascii_val = round(((len(density) / 255) * pixel) - 1)
            ascii_photo += density[ascii_val]
            if len(ascii_photo) % (ypixels + 1)== 0:
                ascii_photo += "\n"
        return ascii_photo

print(create_ascii_image(args.filename, args.size, args.contrast))