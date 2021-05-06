import json
from os import listdir
import requests
import vk
import random
import os
import time
from PIL import Image
from dotenv import load_dotenv


def add_watermark(name_photo):
    watermark = Image.open('logo.png')
    im = Image.open(name_photo)
    im.paste(watermark, (int(im.width / 4), int(im.height * 0.9)), watermark)
    im.save(name_photo)


def send_post_wall():
    owner = '-' + os.getenv('group_id')
    photo_files = listdir('photos')
    try:
        photo_files.remove('.DS_Store')
    except:
        pass
    timestamp = int(time.mktime(time.strptime(os.getenv("date"), '%Y-%m-%d %H:%M:%S')))
    os.chdir('photos')
    for image in photo_files:
        if image != 'logo.png':
            print(image)
            if os.getenv('logo') == 1:
                add_watermark(image)
            timestamp = timestamp + random.randint(3600, 11000)
            img_server = vk_api.photos.getWallUploadServer(group_id=os.getenv('group_id'))['upload_url']
            print(img_server)
            print(os.getcwd())
            files = {
                'photo': open(image, 'rb')
            }
            photo = open(image, 'rb')
            img_send = requests.post(img_server, files=files)
            img_json = json.loads(img_send.text)
            print(img_json)
            img_save = vk_api.photos.saveWallPhoto(group_id=os.getenv('group_id'), photo=img_json['photo'],
                                                   server=img_json['server'], hash=img_json['hash'])
            img = ''
            for im in img_save:
                img = 'photo{}_{}'.format(im['owner_id'], im['id'])
            message = vk_api.wall.post(owner_id=owner, from_group=1,
                                       message=os.getenv('message'),
                                       attachments=img, publish_date=timestamp)
            os.system('rm ' + image)
            time.sleep(5)


if __name__ == '__main__':
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
    session = vk.AuthSession(os.getenv('app_id'), os.getenv("phone"), os.getenv("password"),
                             scope='wall,groups,offline,photos')
    vk_api = vk.API(session, v='5.95', lang='ru', timeout=10)

    send_post_wall()
