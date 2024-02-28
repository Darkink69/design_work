from PIL import Image, ImageDraw
import os
import shutil

template_folders = ['0.5x', '1x', '2x', '4x', 'PNG', 'SVG']
sub_folders = ['16', '32', '64', 'SVG']
name_folder_new_files = '__NEW'


def make_catalog_config():
    print('Создаем новый каталог иконок...')
    path = os.getcwd()
    f = open("icons_catalog.txt", "w")
    for root, dirs, files in os.walk(path):
        for file in files:
            img_path = f'{root}/{file}\n'
            f.write(img_path)
            print(img_path)
    f.close()


# make_catalog_config()


def open_catalog_config():
    f = open("icons_catalog.txt", "r")
    paths = []
    for i in f:
        paths.append(i.replace('\\', '/')[0:-1])
    f.close()
    return paths


def get_new_files():
    new_files = []
    for new_folder in template_folders:
        for i in os.walk(new_folder):
            if i[2]:
                print(f'{len(i[2])} новых(й) файл(ов) в папке {new_folder}:')
                print(i[2])
                new_files.append(i[2])
            else:
                print(f'Нет новых файлов в папке {new_folder}')
    if not new_files:
        print('Нет новых файлов')
    return new_files


def make_new_folders(folder, sub_folders):
    if not os.path.isdir(folder):
        for i in sub_folders:
            os.makedirs(f'{folder}/{i}/')


def copy_file(path_out, filename):
    shutil.copy(filename, path_out)


def delete_file():
    pass


def get_file_extension(path, filename):
    file_name, file_extension = os.path.splitext(f'{path}/{filename}')
    return file_extension


def get_size_PNG(img_path):
    img = Image.open(img_path)
    return img.size[0]


def sort_and_copy_new_files():
    new_folders = []
    for new_folder in template_folders:
        if os.path.isdir(new_folder):
            if os.listdir(new_folder):
                new_folders.append(new_folder)

    for new_folder in range(len(new_folders)):
        for i in new_files[new_folder]:
            file_extension = get_file_extension(new_folders[new_folder], i)
            if file_extension == '.png':
                width_icon = get_size_PNG(f'{new_folders[new_folder]}/{i}')
                if not width_icon == 8:
                    copy_file(f'{name_folder_new_files}/{str(width_icon)}', f'{new_folders[new_folder]}/{i}')
            if file_extension == '.svg':
                copy_file(f'{name_folder_new_files}/{sub_folders[-1]}', f'{new_folders[new_folder]}/{i}')


new_files = get_new_files()
if new_files:
    make_new_folders(name_folder_new_files, sub_folders)
    sort_and_copy_new_files()





img_paths = open_catalog_config()
print(new_files)


if new_files:
    for i in new_files[0]:
        for path in img_paths:
            if path.split('/')[-1] == i:
                path_out = path.split('/')[-3] + '/' + path.split('/')[-2] + '/'
                print(path_out, i)
                copy_file(path_out, f'0.5x/{i}')





# img_path = paths[10]
# print(img_path)


# img.show()





