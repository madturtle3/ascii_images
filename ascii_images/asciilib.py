from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import blessed

def echo(text):
    print(text, end="", flush=True)

def get_saturaiton(image_list):
    return round(sum(image_list) / len(image_list))

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


def create_ascii_color_image(image, size=150, invert=False):
    if type(image) == str:
        image = Image.open(image)
    image = image.convert("RGB")
    term = blessed.Terminal()
    ascii_photo = ""
    photo_size = size
    xpixels = photo_size

    xpix, ypix = image.size
    ypixels = round(xpix/ypix * photo_size * 2) # gotta round for that precision!
    new_img = image.resize((ypixels, xpixels))
    #new_img = new_img.convert("L")
    grey_img = ImageOps.grayscale(new_img).getdata()

    imglist = new_img.getdata()
    #imglist = reduce_background(imglist)
    saturation = round(get_saturaiton(grey_img) ** 1.25)

    density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{\}[]?-_+~<>i!lI;:,\"^`'."
    
    iter_pixels = 0
    density = density[::-1]
    if invert:
        density = density[::-1]
    for pixel, cpixel in zip(grey_img, imglist):
        #ascii_val = round(((len(density) / 255) * pixel) - 1)
        ascii_val = round(((len(density) / 255) * pixel)- 1)
        if invert:
            ascii_photo += term.on_color_rgb(cpixel[0], cpixel[1], cpixel[2]) + " " + term.normal
        else:
            ascii_photo += term.color_rgb(cpixel[0], cpixel[1], cpixel[2]) + density[ascii_val] + term.normal
        #ascii_photo += term.red + density[ascii_val] + term.normal
        #ascii_photo += density[ascii_val]
        if (iter_pixels + 1) % ypixels== 0:
            ascii_photo += "\n"
        iter_pixels += 1
    return ascii_photo

def create_ascii_image(image, size=150, contrast=10, invert=False):
    if type(image) == str:
        image = Image.open(image)
    term = blessed.Terminal()
    ascii_photo = ""
    photo_size = size
    xpixels = photo_size

    xpix, ypix = image.size
    ypixels = round(xpix/ypix * photo_size * 2) # gotta round for that precision!
    new_img = image.resize((ypixels, xpixels))
    #new_img = new_img.convert("L")
    grey_img = ImageOps.grayscale(new_img).getdata()
    #imglist = reduce_background(imglist)
    saturation = round(get_saturaiton(grey_img) ** 1.25)

    density = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{\}[]?-_+~<>i!lI;:,\"^`'."
    
    iter_pixels = 0
    density = density[::-1]
    for pixel in zip(grey_img):
        #ascii_val = round(((len(density) / 255) * pixel) - 1)
        ascii_val = round(((len(density) / 255) * pixel[0])- 1)
        if invert:
            ascii_photo += term.on_color_rgb(pixel[0], pixel[0], pixel[0]) + " " + term.normal
        else:
            ascii_photo += term.color_rgb(pixel[0], pixel[0], pixel[0]) + density[ascii_val] + term.normal
        #ascii_photo += term.red + density[ascii_val] + term.normal
        #ascii_photo += density[ascii_val]
        if (iter_pixels + 1) % ypixels == 0:
            ascii_photo += "\n"
        iter_pixels += 1
    return ascii_photo

def create_ascii_mono_image(image, size=150, contrast=10, invert=False):
    if type(image) == str:
        image = Image.open(image)
    term = blessed.Terminal()
    ascii_photo = ""
    photo_size = size
    xpixels = photo_size

    xpix, ypix = image.size
    ypixels = round(xpix/ypix * photo_size * 2) # gotta round for that precision!
    new_img = image.resize((ypixels, xpixels))
    #new_img = new_img.convert("L")
    if invert:
        new_img = new_img.filter(ImageFilter.FIND_EDGES)
    grey_img = ImageOps.grayscale(new_img).getdata()
    #imglist = reduce_background(imglist)
    saturation = round(get_saturaiton(grey_img) ** 1.25)

    density = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{\}[]?-_+~<>i!lI;:,\"^`'."
    density = density + " " * contrast
    iter_pixels = 0
    density = density[::-1]
    for pixel in zip(grey_img):
        #ascii_val = round(((len(density) / 255) * pixel) - 1)
        ascii_val = round(((len(density) / 255) * pixel[0])- 1)
        ascii_photo += density[ascii_val]
        #ascii_photo += term.red + density[ascii_val] + term.normal
        #ascii_photo += density[ascii_val]
        if (iter_pixels + 1) % ypixels == 0:
            ascii_photo += "\n"
        iter_pixels += 1
    return ascii_photo
