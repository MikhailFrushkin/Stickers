import json
import os
import shutil

import requests
from loguru import logger

from config import domain, headers
from db import Article


def get_products(category: str):
    url = f'{domain}/products/'
    try:
        categories = [category]
        json_data = json.dumps(categories)
        response = requests.get(url, data=json_data, headers=headers)
        return response.json().get('data', [])
    except Exception as ex:
        logger.error(f'Ошибка в запросе по api {ex}')
        logger.error(response.status_code)


def get_info_publish_folder(public_url):
    result_data = []
    res = requests.get(
        f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_url}&fields=_embedded&limit=1000')
    if res.status_code == 200:
        data = res.json().get('_embedded', {}).get('items', [])
        for i in data:
            file_name = i.get('name', None)
            if file_name:
                file_name = file_name.strip().lower()

            if (os.path.splitext(file_name)[0].isdigit()
                    or 'подл' in file_name
                    or file_name.endswith('.pdf')
            ):
                try:
                    result_data.append({
                        'name': i.get('name').strip(),
                        'file': i.get('file')
                    })
                except:
                    pass

        return result_data


def create_download_data(item):
    try:
        url_data = get_info_publish_folder(item['directory_url'])
        if url_data:
            item['url_data'] = url_data
            return item
    except Exception as ex:
        logger.error(ex)


def get_arts_in_base(category):
    records = Article.select().where(Article.category == category)
    art_list = list(set(i.art.upper() for i in records))
    return art_list


def download_file(destination_path, url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
            # logger.info(f"File downloaded successfully: {destination_path}")
        else:
            logger.error(f"Error {response.status_code} while downloading file: {url}")
    except requests.RequestException as e:
        logger.error(f"Error during downloading file: {e}")


def copy_image(image_path, count):
    folder_art = os.path.dirname(image_path)
    exp = image_path.split('.')[-1]
    for i in range(count - 1):
        shutil.copy2(image_path, os.path.join(folder_art, f'{i + 2}.{exp}'))


def main_download_site(category, config, self):
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    chunk_size = 20

    directory = os.path.join(config.params.get('Путь к базе'), category)
    art_list = get_arts_in_base(category)
    data = get_products(category)

    logger.debug(f'Артикулов в базе:{len(art_list)}')
    logger.debug(f'Артикулов в ответе с сервера:{len(data)}')
    data = [item for item in data if item['art'].upper() not in art_list]
    logger.success(f'Артикулов для загрузки:{len(data)}')

    all_arts = len(data)
    count = 1
    count_download = 1
    if not len(data):
        self.progress_updated.emit(100, 100)
        self.update_progress_message.emit('Обновление', 100, 100)
        return
    for chunk in chunk_list(data, chunk_size):
        result_download_arts = []

        for index, item in enumerate(chunk, start=1):
            # print(f'Получение мета папки {count}/{all_arts}')
            download_data = create_download_data(item)
            if download_data:
                result_download_arts.append(download_data)
            else:
                logger.error(f'не удалось получить ссылки на файлы с яндекс диска: {item.get("art", None)}')
            count += 1

        for index, item in enumerate(result_download_arts, start=1):
            try:
                art = item['art']
                brand = item['brand']
                category_prod = item['category']
                quantity = item['quantity']
                folder = os.path.join(directory, art)
                if os.path.exists(folder):
                    logger.warning(f'Папка существует {art}, удалена!')
                    shutil.rmtree(folder, ignore_errors=True)

                os.makedirs(folder, exist_ok=True)

                for i in item['url_data']:
                    destination_path = os.path.join(folder, i['name'])
                    download_file(destination_path, i['file'])

                if item['the_same']:
                    try:
                        image_path = os.path.join(folder, '1.png')
                        if os.path.exists(image_path):
                            copy_image(image_path, quantity)
                        else:
                            image_path = os.path.join(folder, '1.jpg')
                            if os.path.exists(image_path):
                                copy_image(image_path, quantity)
                            else:
                                raise ValueError(f'Нет файла для копирования артикул: {item}')
                    except Exception as ex:
                        logger.error(ex)

                try:
                    Article.create_art(folder, art, quantity, category_prod, brand)
                except Exception as ex:
                    logger.error(ex)
            except Exception as ex:
                logger.error(ex)
            count_download += 1
            self.progress_updated.emit(count_download, all_arts)
            self.update_progress_message.emit('Обновление', count_download, all_arts)
