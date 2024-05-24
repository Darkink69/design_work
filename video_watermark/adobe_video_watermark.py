import time
import datetime as dt
import subprocess
import os
import shutil
import psutil
import yt_dlp
from ffprobe import FFProbe
from PIL import Image, ImageDraw, ImageFilter, ImageFont

folder_adobe = 'adobe'
folder_two = 'shutterstock'
result = 'result'
videos = 5

# folder = [folder_adobe, folder_two]


def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")


print(time_now(), 'Начало работы')


def get_name_files(folder):
    files_dir = os.listdir(folder)
    files_video = []
    for file in files_dir:
        if os.path.isfile(f'{folder}/{file}'):
            new_name = file.replace(' ', '_')
            os.rename(f'{folder}/{file}', f'{folder}/{new_name}')
            files_video.append(new_name)

    print(f'В папке {folder} - {len(files_video)} файла(ов)')
    return files_video


def make_screens(folder, file):
    item_folder = file[:-4]
    if not os.path.isdir(f'{folder}/{item_folder}'):
        path = f'{os.getcwd()}\\{folder}/' + item_folder
        os.mkdir(path)

        try:
            pro = f'ffmpeg -i {folder}/{file} {folder}/{item_folder}/frame_%03d.png'
            pr = subprocess.check_call(pro, shell=True)
        except BaseException:
            print(time_now(), 'Ошибка создания кадра')

        return item_folder


def merge_screens_mask(item_folder_adobe, item_folder_two):
    all_frames = []
    all_frames += os.listdir(f'{folder_adobe}/{item_folder_adobe}')
    print(len(all_frames), 'файла(ов) в папке', item_folder_adobe)
    print(time_now(), 'Начинаем склеивание кадров по маске')

    for frame in all_frames:
        try:
            im1 = Image.open(f'{folder_adobe}/{item_folder_adobe}/{frame}')
            im2 = Image.open(f'{folder_two}/{item_folder_two}/{frame}').resize(im1.size)
            mask = Image.open('mask.png').resize(im2.size).convert('L')
            im1.paste(im2, (0, 0), mask)
            im1.save(f'{result}/{frame}')
        except BaseException:
            print('Ошибка при сложении кадра', frame)


def merge_png_to_mp4(item_folder_adobe):
    print(time_now(), 'Создание видео из кадров')
    try:
        pro = f'ffmpeg -r 29.97 -y -i "{result}/frame_%03d.png" {item_folder_adobe}_4k.mp4'
        pr = subprocess.check_call(pro, shell=True)
    except BaseException:
        print('Ошибка при объединении кадров')


def delete_everything_in_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def create_thumbnail_in_video(video):
    try:
        pro = f'ffmpeg -i {video} -vf "thumbnail" -frames:v 1 thumbnail.png'
        pr = subprocess.check_call(pro, shell=True)

        pro = f'ffmpeg -i {video} -i thumbnail.png -map 1 -map 0 -c copy -disposition:0 attached_pic out.mp4'
        pr = subprocess.check_call(pro, shell=True)
        os.remove(video)
        os.remove('thumbnail.png')
        os.rename(f'out.mp4', video)
    except BaseException:
        print('Ошибка создания thumbnail')


for i in range(videos):
    files_video = get_name_files(folder_adobe)
    item_folder_adobe = make_screens(folder_adobe, files_video[i])

    files_video = get_name_files(folder_two)
    item_folder_two = make_screens(folder_two, files_video[i])
    # item_folder_adobe = '03'
    # item_folder_two = '03'
    merge_screens_mask(item_folder_adobe, item_folder_two)

    merge_png_to_mp4(item_folder_adobe)
    delete_everything_in_folder(result)

    create_thumbnail_in_video(f'{item_folder_adobe}_4k.mp4')





# all_frames = []
# all_frames += os.listdir(f'{folder_two}/03_gp')
# print(all_frames)
# for frame in all_frames:
#     # os.rename(f'{frame}', {frame})
#     os.rename(f'{folder_two}/03_gp/{frame}', f'{folder_two}/03_gp/{frame[:9]+".png"}')
# f = 'frame_001-very_compressed-scale-2_00x.png'


print(time_now(), 'Обработка завершена')

