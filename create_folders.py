import asyncio
import os
import re
import shutil
import time

import PyPDF2
import aiohttp
import pandas as pd
import requests
from loguru import logger
from peewee import fn

from utils.utils import df_in_xlsx


def create_folder_order(articles, name_doc):
    from main import config_prog

    def fill_list(lst, target_size):
        if len(lst) >= target_size:
            return lst[:target_size]
        else:
            repetitions = target_size // len(lst)
            remainder = target_size % len(lst)
            filled_lst = lst * repetitions + lst[:remainder]
            return filled_lst

    def copy_files_folder(arts, brand, category, max_folder=240, target_size=1):
        count = 1
        dir_count = 1
        count_images = 0
        all_count_images = 0
        directory = os.path.join(config_prog.current_dir, 'Заказ', f'{os.path.splitext(name_doc)[0]}'
                                                                   f'_{brand}_{category}_{dir_count}')
        os.makedirs(directory, exist_ok=True)
        for index, article in enumerate(arts, start=1):
            image_paths = article.images.split(';')
            len_images = len(image_paths)
            if brand == 'AniKoya' and category == 'Наклейки 3-D':
                len_blocks = len_images // 15 + 1
                target_size = 15 * len_blocks
            filled_list = fill_list(image_paths, target_size)
            article_images_count = len(filled_list)

            if count_images + article_images_count > max_folder:
                dir_count += 1
                directory = os.path.join(config_prog.current_dir, 'Заказ', f'{os.path.splitext(name_doc)[0]}'
                                                                           f'_{brand}_{category}_{dir_count}')
                os.makedirs(directory, exist_ok=True)
                count_images = 0

            for image_path in filled_list:
                try:
                    exp = os.path.splitext(os.path.basename(image_path))[1]
                    new_filename = f"{count}{exp}"
                    destination_path = os.path.join(directory, new_filename)
                    shutil.copy2(image_path, destination_path)
                    count += 1
                    count_images += 1
                    all_count_images += 1
                except Exception as ex:
                    logger.error(ex)

        return all_count_images

    shutil.rmtree(os.path.join(config_prog.current_dir, 'Заказ'), ignore_errors=True)

    anikoya_3d_stickers = []
    dochke_popsockets = []
    other_articles = []

    for article in articles:
        if article.brand == 'AniKoya' and article.category == 'Наклейки 3-D':
            anikoya_3d_stickers.append(article)
        elif article.brand == 'Дочке понравилось' and article.category == 'Попсокеты':
            dochke_popsockets.append(article)
        else:
            other_articles.append(article)

    all_images_count = 0
    if anikoya_3d_stickers:
        all_images_count += copy_files_folder(anikoya_3d_stickers, 'AniKoya', 'Наклейки 3-D')
    if dochke_popsockets:
        all_images_count += copy_files_folder(dochke_popsockets, 'Дочке понравилось', 'Попсокеты')

    logger.success('Завершено копирование файлов')
    return len(articles), all_images_count, len(anikoya_3d_stickers), len(dochke_popsockets)


def find_files_in_directory(directory, file_list):
    file_dict = {}
    found_files = []
    not_found_files = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_name = re.sub(r'(_[1-5]|\.pdf)', '', file, flags=re.IGNORECASE).lower().strip()
            file_dict[file_name] = os.path.join(directory, file)

    for poster in file_list:
        file_name = poster.lower().strip()
        if file_name in file_dict:
            found_files.append(file_dict[file_name])
        else:
            not_found_files.append(poster)
    return found_files, not_found_files


def merge_pdfs_stickers(arts_paths, output_path):
    pdf_writer = PyPDF2.PdfWriter()
    arts_paths.reverse()
    for index, input_path in enumerate(arts_paths, start=1):
        try:
            with open(input_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
        except Exception:
            pass
    current_output_path = f"{output_path}.pdf"
    with open(current_output_path, 'wb') as output_file:
        pdf_writer.write(output_file)
    PyPDF2.PdfWriter()


def create_order_shk(arts, name_doc):
    from main import config_prog
    found_files_stickers, not_found_stickers = find_files_in_directory(config_prog.params.get('Путь к шк'), arts)
    if found_files_stickers:
        merge_pdfs_stickers(found_files_stickers, f'Заказ\\!ШК {name_doc}')
        logger.debug(f'{name_doc} ШК сохранены!')
    else:
        logger.error(f'{name_doc} ШК не найдены!')
    return not_found_stickers


def create_bad_arts(arts, name_doc, version):
    df_not_found = pd.DataFrame(arts, columns=['Артикул'])
    try:
        if len(df_not_found) > 0:
            df_in_xlsx(df_not_found, f'Не найденные {name_doc} v.{version}', directory='Заказ')
    except Exception as ex:
        logger.error(ex)


def upload_file(loadfile, replace=False):
    from main import config_prog
    savefile = f'/Отчеты/{os.path.basename(loadfile)}'
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {
        "Authorization": f"OAuth {config_prog.params.get('token')}"
    }
    params = {
        "path": savefile,
        "overwrite": replace
    }
    resp = requests.get(upload_url, headers=headers, params=params)
    logger.debug(resp.status_code)

    res = resp.json()
    if resp.status_code == 409:
        return True
    else:
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except KeyError as e:
                logger.error(f"KeyError: {e}. Response: {res}")
            except requests.exceptions.Timeout as e:
                logger.error("Timeout error:", e)
            except requests.exceptions.RequestException as e:
                logger.error("An error occurred:", e)
                logger.error("An error occurred:", resp.status_code)
                logger.error("An error occurred:", resp.json())
            except Exception as e:
                logger.error(f"An error Exception: {e}")
            else:
                return True
