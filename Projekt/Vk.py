import requests
import json
from tqdm import tqdm
import time

class VkPhoto:

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def _user(self):
        ind = int(input('''
        Запрос информации по id пользователя или по username?
        Введите:
        1 - если по username
        2 - если по id
        '''))
        if ind == 1:
            user_id = input('Введите username: ')
            user_params = {
                'user_ids': user_id,
            }
            res = requests.get('https://api.vk.com/method/users.get', params={**self.params, **user_params})
            users = res.json()['response'][0]['id']
        elif ind == 2:
            user_id = input('Введите id: ')
            users = user_id
        else:
            print('Вы ввели несуществующую команду')
        return users

    def get_photos(self, count=5):
        photos_params = {
            'owner_id': self._user(),
            'album_id': 'profile',
            'photo_sizes': 1,
            'rev': 0,
            'extended': 'likes',
            'count': count
        }
        res = requests.get('https://api.vk.com/method/photos.get', params={**self.params, **photos_params})
        photos = res.json()['response']['items']
        likes = {}
        open_data = []
        photo_name = []
        for ind in photos:  # Создаем словарь, который определит есть ли фото с одинаковым количеством лайокв
            likes.setdefault(ind['likes']['count'], 0)
            likes[ind['likes']['count']] += 1
        for ind in tqdm(photos):  # Сохраняем в переменные все нужные данные из json vk
            open_name = []
            like = ind['likes']['count']
            date = ind['date']
            if likes[like] > 1:  # Проверка на дублирование лайков
                name = f'{like}_{date}'
            else:
                name = like
            url_1 = ind['sizes'][-1]['url']
            type = ind['sizes'][-1]['type']
            open_data.append({"file_name": name, "size": type})
            open_name.append(str(name))
            open_name.append(url_1)
            photo_name.append(open_name)  # Создаем список имен, чтобы потом по нему итерироваться при загрузке на ЯДиск
            time.sleep(1)
        data = {'photos': open_data}
        with open('photos.json', 'w') as file_2:  # Записываем полученную информацию по фото в json
            json.dump(data, file_2)
        return photo_name  # Забираем после выполнения метода список имен для работы с ним в классе YandexDisk