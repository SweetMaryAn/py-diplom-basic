from Vk import VkPhoto
from Yandex import YandexDisk

if __name__ == '__main__':
    vk_client = VkPhoto(input('Введите токен Вконтакте: '), '5.131')
    ya = YandexDisk(input('Введите токен Яндекс Диска: '))
    ya.new_directory()
    ya.upload_file_to_disk(vk_client.get_photos(
        input('Укажите количество фото, которое необходимо выгрузить: ')
    ))