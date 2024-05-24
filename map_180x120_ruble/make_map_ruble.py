import os
from PIL import Image, ImageDraw, ImageFilter

imgs_folder = 'in'


def get_images():
    images = []
    for i in os.walk(imgs_folder):
        images = i[2]
        # count_images = len(images)
    return images


images = get_images()
print(len(images), f'картинок(и) в папке {imgs_folder}')

for i in images:
    print(i)

    img = Image.open(f'{imgs_folder}/{i}')
    print(img.size)
    cropped_img = img.crop((310, 107, 1610, 972))
    img_resize = cropped_img.resize((180, 120))

    img_ruble = Image.open('map_BUY_RUB.png')

    mask = Image.open('mask.png').resize(img_ruble.size).convert('L')

    img_resize.paste(img_ruble, (0, 0), mask)
    img_resize.save(f'out/{i}')

    print('------------------------------')



