import os
from PIL import Image, ImageDraw, ImageFilter
from datetime import datetime
import datetime


# background_color = 'white'
background_color = 0x363835
width_canvas = 1920
horiz_gap = 50
vert_gap = 30


def get_screenshots():
    screenshots = []
    for i in os.walk('in'):
        screenshots = i[2]
    count_screens = len(screenshots)
    return screenshots, count_screens


def size_calculation(count_screens):
    width_img = (width_canvas - horiz_gap * (count_screens + 1)) // count_screens
    size = Image.open(f"in/{screenshots[0]}")
    height_img = size.height * width_img // size.width
    height_canvas = height_img + vert_gap * 2
    return width_img, height_img, height_canvas


def drop_shadow(image, iterations=5, border=8, offset=(3, 3), background_colour=background_color, shadow_colour=0x444444):
    shadow_width = image.size[0] + abs(offset[0]) + 2 * border
    shadow_height = image.size[1] + abs(offset[1]) + 2 * border

    shadow = Image.new(image.mode, (shadow_width, shadow_height), background_colour)
    shadow_left = border + max(offset[0], 0)
    shadow_top = border + max(offset[1], 0)
    shadow.paste(shadow_colour, [shadow_left, shadow_top, shadow_left + image.size[0], shadow_top + image.size[1]])

    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    img_left = border - min(offset[0], 0)
    img_top = border - min(offset[1], 0)
    shadow.paste(image, (img_left, img_top), image)

    return shadow


def create_img(width_img, height_img):
    x = horiz_gap
    for i in screenshots:
        img2 = Image.open(f"in/{i}")
        im_resized = img2.resize((width_img, height_img))
        shadow = drop_shadow(im_resized)
        img.paste(shadow, (x, vert_gap))
        x += width_img + horiz_gap


screenshots, count_screens = get_screenshots()
if count_screens:
    width_img, height_img, height_canvas = size_calculation(count_screens)

    img = Image.new('RGB', (width_canvas, height_canvas), background_color)
    create_img(width_img, height_img)

    date = datetime.datetime.today()
    img.save(f'{count_screens}_{date.strftime("%H-%M")}.jpg', quality=50)
    img.show()
else:
    print('Нет картинок в папке in')






# img = Image.open("C://Users/varkatov\Downloads/trash//nu.png")
# print(f"Width: {img.width}")
# print(f"Height: {img.height}")
# print(f"Filename: {img.filename}")
# print(f"Format: {img.format}")
# print(f"Mode: {img.mode}")


