import os
from PIL import Image, ImageDraw, ImageFilter
from datetime import datetime
import datetime
import shutil


# background_color = 'white'
background_color = 0x363835
width_canvas = 1920
horiz_gap = 50
vert_gap = 30
# folder = 'in'
folder = '//VARDATA\Content_and_Design\Products & Projects\Karta RU\Video\shorts\screens'


def get_screenshots():
    screenshots = []
    for i in os.walk(folder):
        screenshots = i[2]

    count_screens = 0
    img_extension = ['png', 'jpg', 'jpeg', 'webp']
    for i in screenshots:
        if i.split('.')[1] in img_extension and i.split('_')[0] != 'collage':
            count_screens += 1

    return screenshots, count_screens


def size_calculation(scr_item, count_screens):
    width_img = (width_canvas - horiz_gap * (count_screens + 1)) // count_screens
    size = Image.open(f"{folder}/{scr_item[0]}")
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
    image = image.convert('RGBA')
    shadow.paste(image, (img_left, img_top), image)

    return shadow


def create_img(scr_item, width_img, height_img):
    x = horiz_gap
    for i in scr_item:
        try:
            img2 = Image.open(f"{folder}/{i}")
            im_resized = img2.resize((width_img, height_img))
            shadow = drop_shadow(im_resized)
            img.paste(shadow, (x, vert_gap))
            x += width_img + horiz_gap
        except BaseException:
            pass


screenshots, count_screens = get_screenshots()
print(screenshots, count_screens)
if count_screens:
    index_img = ['1', '2', '3', '4', '5']
    for index in index_img:
        scr_item = []
        for i in screenshots:
            if i.split('_')[0] == index:
                scr_item.append(i)
        # print(index)
        print(scr_item)

        if len(scr_item) != 0:
            width_img, height_img, height_canvas = size_calculation(scr_item, len(scr_item))

            img = Image.new('RGB', (width_canvas, height_canvas), background_color)
            create_img(scr_item, width_img, height_img)

            img.save(f'{folder}/0{index}_collage_{len(scr_item)}.jpg', quality=50)
            img.show()
else:
    print('Нет картинок в папке', folder)





# date = datetime.datetime.today()
# if background_color != 'white':
#     background_color = ''
# {date.strftime("%H-%M")}


# print(f"Width: {img.width}")
# print(f"Height: {img.height}")
# print(f"Filename: {img.filename}")
# print(f"Format: {img.format}")
# print(f"Mode: {img.mode}")


