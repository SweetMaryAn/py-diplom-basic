import requests
import json


class VkPhoto:

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, user_id=None, count=5):
        photos_params = {
            'owner_id': user_id,
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
        for ind in photos:  # Сохраняем в переменные все нужные данные из json vk
            like = ind['likes']['count']
            date = ind['date']
            if likes[like] > 1:  # Проверка на дублирование лайков
                name = f'{like}_{date}'
            else:
                name = like
            url_1 = ind['sizes'][-1]['url']
            type = ind['sizes'][-1]['type']
            read = requests.get(url_1)  # Скачиваем файлы по ссылке
            with open(f'{name}.jpg', 'wb') as file_1:
                file_1.write(read.content)
            open_data.append({"file_name": name, "size": type})
            photo_name.append(str(name))  # Создаем список имен, чтобы потом по нему итерироваться при загрузке на ЯДиск
        data = {'photos': open_data}
        with open('photos.json', 'w') as file_2:  # Записываем полученную информацию по фото в json
            json.dump(data, file_2)
        return photo_name  # Забираем после выполнения метода список имен для работы с ним в классе YandexDisk


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def new_directory(self, name_directory='Photos'):  # Создаем папку на Яндек Диске
        directory_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": name_directory, "overwrite": "true"}
        response = requests.put(directory_url, headers=headers, params=params)
        return response.json()

    def _get_upload_link(self, disk_file_path):  # Вспомогательный метод  - получаем ссылку для загрузки на Яндекс Диск
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, name_directory='Photos'):
        for disk_file in disk_file_path:  # Итерируемся по списку имен и загружаем поочередно файлы на Яндекс Диск
            href = self._get_upload_link(disk_file_path=(f'{name_directory}/{disk_file}.jpg')).get("href", "")
            response = requests.put(href, data=open(f'{disk_file}.jpg', 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print("Success")


if __name__ == '__main__':
    vk_client = VkPhoto(input('Введите токен Вконтакте: '), '5.131')
    ya = YandexDisk(input('Введите токен Яндекс Диска: '))
    ya.new_directory()
    ya.upload_file_to_disk(vk_client.get_photos(input('Укажите ID пользователя Вконтакте: ')))
