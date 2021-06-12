import json
from os import listdir
import requests
import vk_api
import random
import os
import time
from PIL import Image
from dotenv import load_dotenv


def add_watermark(name_photo):  # Функция которая накладывает водяной знак
    watermark = Image.open('logo.png')
    im = Image.open(name_photo)
    im.paste(watermark, (int(im.width / 2) - int(watermark.width / 2), int(im.height * 0.9)), watermark)
    im.save(name_photo)


def send_post_wall():
    owner = '-' + os.getenv('group_id')  # Преобразовываем айди для сообществ
    photo_files = listdir('photos')
    try:
        photo_files.remove('.DS_Store')  # Чистим мусор если имеется
    except:
        pass
    # Преобразовываем дату в unix time
    timestamp = int(time.mktime(time.strptime(os.getenv("date"), '%Y-%m-%d %H:%M:%S')))
    os.chdir('photos')
    for image in photo_files:  # Парсим директорию с фото
        if image != 'logo.png':
            print(image)
            if os.getenv('logo') == 1:
                add_watermark(image)
            # Устанавливаем время публикации
            timestamp = timestamp + random.randint(int(os.getenv('time1')) * 60, int(os.getenv('time2')) * 60)
            # Получаем адрес заливки
            img_server = vk_api.photos.getWallUploadServer(group_id=os.getenv('group_id'))['upload_url']
            files = {
                'photo': open(image, 'rb')
            }
            photo = open(image, 'rb')
            # Заливаем фото и получаем адрес
            img_send = requests.post(img_server, files=files)
            img_json = json.loads(img_send.text)
            img_save = vk_api.photos.saveWallPhoto(group_id=os.getenv('group_id'), photo=img_json['photo'],
                                                   server=img_json['server'], hash=img_json['hash'])
            img = ''
            for im in img_save:
                img = 'photo{}_{}'.format(im['owner_id'], im['id'])
            message = vk_api.wall.post(owner_id=owner, from_group=1,
                                       message=os.getenv('message'),
                                       attachments=img, publish_date=timestamp)
            os.system('rm ' + image)  # Удаляем фото из папки
            time.sleep(5)


if __name__ == '__main__':
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
    # Подключаем env и авторизуемся
    vk.logger.setLevel('DEBUG')
    session = vk.AuthSession(os.getenv('app_id'), os.getenv("phone"), os.getenv("password"),
                             scope='groups,manage,wall,photos')

    vk_api = vk.API(session, v='5.95', lang='ru', timeout=10)
    send_post_wall()
