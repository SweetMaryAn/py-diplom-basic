import requests
from tqdm import tqdm
import time

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

    def upload_file_to_disk(self, disk_file_path, name_directory='Photos'):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for disk_file in tqdm(disk_file_path):
            params = {"path": f'{name_directory}/{disk_file[0]}.jpg', "url": disk_file[1]}
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 201:
                print("Success")
            time.sleep(1)
