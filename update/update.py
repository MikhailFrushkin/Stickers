import datetime
import json
import os
import shutil

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config import domain, headers, base_folder, config_prog
from db import Article
from utils.blur import blur_image


def get_products(category: str | list, brand_request: str | None = None):
    response = None
    try:
        if not brand_request:
            url = f'{domain}/products/'
            if isinstance(category, list):
                categories = category
            else:
                categories = [category]
            json_data = json.dumps(categories)
        else:
            url = f'{domain}/products_v2/'
            data = {
                "categories": [category],
                "brands": [brand_request],
            }
            json_data = json.dumps(data)
        response = requests.get(url, data=json_data, headers=headers)
        return response.json().get('data', [])

    except Exception as ex:
        logger.error(f'Ошибка в запросе по api {ex}')
        if response:
            logger.error(response.status_code)
            logger.error(response.text)


def get_info_publish_folder(public_url, download_union_list=False):
    result_data = []
    res = requests.get(
        f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_url}&limit=1000')
    if res.status_code == 200:
        data = res.json()
        folder_name = data.get('name')
        data = data.get('_embedded', {}).get('items', [])
        for i in data:
            file_name = i.get('name', None)
            if file_name:
                file_name = file_name.strip().lower()

                if (os.path.splitext(file_name)[0].isdigit() or 'принт' in os.path.splitext(file_name)[0] or (
                        'кружка' in file_name and '1' in file_name) or 'подл' in file_name or file_name.endswith('.pdf')
                        or file_name.endswith('.cdr')):
                    if download_union_list:
                        result_data.append({'name': i.get('name').strip(), 'file': i.get('file'),
                                            'path': i.get('path')})
                    else:
                        if "все" not in file_name or 'макет' not in file_name:
                            result_data.append(
                                {'name': i.get('name').strip(), 'file': i.get('file'), 'path': i.get('path')})

        for i in result_data:
            if i.get('name').endswith('.pdf'):
                break
        else:
            logger.error(f'Нет шк {public_url}')
            return
        return result_data, folder_name


def create_download_data(item, download_union_list):
    try:
        url_data, folder_name = get_info_publish_folder(item['directory_url'], download_union_list)
        if url_data:
            item['url_data'] = url_data
            item['folder_name'] = folder_name
            return item
    except Exception as ex:
        logger.error(ex)


def get_arts_in_base(category):
    records = Article.select().where(Article.category == category)
    art_list = list(set(i.art.upper() for i in records))
    return art_list


def get_download_url(path_file):
    headers_yandex = {'Authorization': f'OAuth {config_prog.params.get("token")}'}

    url = f'https://cloud-api.yandex.net/v1/disk/resources/download?path={path_file}'
    response = requests.get(url, headers=headers_yandex)
    logger.warning(response.status_code)
    logger.warning(response.text)
    if response.status_code == 200:
        return response.json().get('href')


def download_file(destination_path, url, path_file):
    session = requests.Session()
    retries = Retry(total=2, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
        else:
            logger.error(f"Error {response.status_code} while downloading file: {url}")
    except requests.RequestException as e:
        logger.error(f"Error during downloading file: {e}")
        try:
            url = get_download_url(path_file)
            response = session.get(url, stream=True, timeout=5)
            if response.status_code == 200:
                with open(destination_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
        except Exception as ex:
            logger.error(ex)


def copy_image(image_path, count):
    folder_art = os.path.dirname(image_path)
    exp = image_path.split('.')[-1]
    for i in range(count - 1):
        shutil.copy2(image_path, os.path.join(folder_art, f'{i + 2}.{exp}'))


def main_download_site(category: str | list, config, self, download_union_list):
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    chunk_size = 20
    art_list = []
    download_arts = []
    data = get_products(category)

    if isinstance(category, list):
        for cat in category:
            art_list.extend(get_arts_in_base(cat))
        if category[0] == 'Кружки':
            category = 'Кружки'
    else:
        art_list = get_arts_in_base(category)
    logger.info(f'Артикулов в базе: {len(art_list)}')
    logger.info(f'Артикулов в ответе с сервера: {len(data)}')
    for item in data:
        art = item['art'].upper()
        if art not in art_list:
            download_arts.append(item)
        else:
            product = Article.get(Article.art == art)
            str_date_item = item['updated_at']

            date_site = datetime.datetime.strptime(str_date_item, "%Y-%m-%dT%H:%M:%S.%fZ")
            try:
                if date_site > product.updated_at_in_site:
                    product.delete_instance()
                    download_arts.append(item)
            except Exception as ex:
                logger.error(ex)
                logger.error(product)

    # data = [item for item in data if item['art'].upper() not in art_list]
    # data = data[:500]
    logger.success(f'Артикулов для загрузки: {len(download_arts)}')

    all_arts = len(download_arts)
    count = 1
    count_download = 1
    if not len(download_arts):
        self.progress_updated.emit(100, 100)
        self.update_progress_message.emit('Обновление', 100, 100)
        return
    for chunk in chunk_list(download_arts, chunk_size):
        result_download_arts = []

        for index, item in enumerate(chunk, start=1):
            download_data = create_download_data(item, download_union_list)
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
                folder_name = item['folder_name']
                size = item['size']

                updated_at_in_site = datetime.datetime.strptime(item['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

                folder = os.path.join(config.params.get('Путь к базе'), brand, category, art)

                try:
                    if os.path.exists(folder):
                        logger.warning(f'Файлы артикула существуют {art}, но будут обновлены!')
                        shutil.rmtree(folder, ignore_errors=True)
                    os.makedirs(folder, exist_ok=True)
                except Exception as ex:
                    logger.error(ex)

                for i in item['url_data']:
                    try:
                        destination_path = os.path.join(folder, i['name'])
                        download_file(destination_path, i['file'],
                                      f'{base_folder}/{category_prod}/{folder_name}{i["path"]}')
                    except Exception as ex:
                        logger.error(ex)

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
                    if (category == 'Брелки' or category == 'Зеркальца' or category == 'Значки'
                            or (category == 'Попсокеты' and size == '44')):
                        size_blur = size
                        flag_blur = False
                        for file in os.listdir(folder):
                            file_name, exp = os.path.splitext(file)
                            if file_name.isdigit():
                                image_path = os.path.join(folder, file)
                                output_path = os.path.join(folder, f'blur_{file}')
                                flag_blur = blur_image(image_path, output_path, size_blur)
                except Exception as ex:
                    logger.error(ex)

                try:
                    if (category == 'Брелки' or category == 'Зеркальца' or category == 'Значки'
                            or (category == 'Попсокеты' and size == '44')) and not flag_blur:
                        pass
                    else:
                        Article.create_art(folder, art, quantity, size, category_prod, brand, updated_at_in_site)
                except Exception as ex:
                    logger.error(ex)
            except Exception as ex:
                logger.error(ex)
            count_download += 1
            self.progress_updated.emit(count_download, all_arts)
            self.update_progress_message.emit('Обновление', count_download, all_arts)


if __name__ == '__main__':
    get_download_url(f'{base_folder}/Брелки/10954_2_25_1/1.png')
