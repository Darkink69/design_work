import os
from PIL import Image, ImageDraw, ImageFilter

max_width = 1920
max_size = 248000  # Kb
optimal_width = 1200
imgs_folder = '//VARDATA\Content_and_Design\Products & Projects\Karta RU\Video\shorts\Сырье'
# imgs_folder = 'in'


def get_images():
    images = []
    for i in os.walk(imgs_folder):
        images = i[2]
        # count_images = len(images)
    return images


images = get_images()
print(len(images), f'картинок(и) в папке {imgs_folder}')

for i in images:
    file_size = os.path.getsize(f'{imgs_folder}/{i}')
    if file_size > max_size:
        print(i, '-', file_size, 'байт')
        try:
            img = Image.open(f'{imgs_folder}/{i}')
            if img.width > 1920:
                img_resized = img.resize((optimal_width, int(optimal_width * img.height / img.width)))
                img = img_resized

            try:
                img.convert('RGB').save(f'{i[0:-4]}.jpg', quality=50)
            except BaseException:
                print('Не удалось сохранить файл', i)

            else:
                print(f'{i} меньше или около 200 Кб')

        except BaseException:
            print('Не удалось открыть файл', i)
    print('------------------------------')



