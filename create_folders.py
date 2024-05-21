import os
import random
import re
import shutil

import PyPDF2
import pandas as pd
import requests
from loguru import logger

from config import ready_path
from utils.Created_images_list import created_good_images, combine_images_to_pdf
from utils.utils import df_in_xlsx, chunk_list


def fill_list(lst, target_size):
    """
    Заполняет список до нужного размера, повторяя его элементы.
    """
    if len(lst) >= target_size:
        return lst[:target_size]
    else:
        repetitions = target_size // len(lst)
        remainder = target_size % len(lst)
        return lst * repetitions + lst[:remainder]


def copy_image_files(filled_list, directory, count, count_images, all_count_images):
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
            logger.error(f"Error copying file {image_path}: {ex}")
    return count, count_images, all_count_images


def add_random_images(images_list):
    unique_elements = list(set(images_list))

    # Если уникальных элементов меньше трех, берем все
    if len(unique_elements) < 3:
        unique_random_elements = list(unique_elements)
        # Дополнение до трех элементов из повторяющихся
        while len(unique_random_elements) < 3:
            random_element = random.choice(images_list)
            if random_element not in unique_random_elements:
                unique_random_elements.append(random_element)
    else:
        unique_random_elements = random.sample(unique_elements, 3)
    return unique_random_elements


def copy_images_number(arts_number, number, max_folder, category, all_count_images, config_prog):
    """
    Копирует изображения из списка статей в папки, ограничивая количество файлов в папке.
    """
    dir_count = 1
    count = 1
    count_images = 0
    directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{number}шт._{dir_count}')
    os.makedirs(directory, exist_ok=True)

    if number == 12:
        for article in arts_number:
            image_paths = article.images.split(';')
            filled_list = fill_list(image_paths, 15 * (len(image_paths) // 15 + 1)) if number == 12 else image_paths

            if count_images + len(filled_list) > max_folder:
                dir_count += 1
                directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{number}шт._{dir_count}')
                os.makedirs(directory, exist_ok=True)
                count_images = 0

            count, count_images, all_count_images = copy_image_files(filled_list, directory, count, count_images,
                                                                     all_count_images)

    elif number == 6:
        for article in arts_number:
            filled_list = []
            image_paths = article.images.split(';')
            filled_list.extend(image_paths * 2)
            random_elements = add_random_images(filled_list)
            filled_list.extend(random_elements)

            if count_images + len(filled_list) > max_folder:
                dir_count += 1
                directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{number}шт._{dir_count}')
                os.makedirs(directory, exist_ok=True)
                count_images = 0

            count, count_images, all_count_images = copy_image_files(filled_list, directory, count, count_images,
                                                                     all_count_images)

    elif number == 2:
        chunk_list_number_6 = chunk_list(arts_number, 3)
        for chunk in chunk_list_number_6:
            filled_list = []
            for item in chunk:
                image_paths = item.images.split(';')
                filled_list.extend(image_paths * (6 // len(chunk)))

            random_elements = add_random_images(filled_list)
            filled_list.extend(random_elements)

            if count_images + len(filled_list) > max_folder:
                dir_count += 1
                directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{number}шт._{dir_count}')
                os.makedirs(directory, exist_ok=True)
                count_images = 0

            count, count_images, all_count_images = copy_image_files(filled_list, directory, count, count_images,
                                                                     all_count_images)

    return all_count_images


def created_stickers(arts, max_folder, category):
    """
    Создает наклейки из списка статей, разделяя их по количеству и копируя изображения в соответствующие папки.
    """
    from main import config_prog
    all_count_images = 0

    quantity_2 = [article for article in arts if article.quantity == 2]
    quantity_6 = [article for article in arts if article.quantity == 6]
    quantity_12_or_more = [article for article in arts if article.quantity >= 12]

    if quantity_12_or_more:
        all_count_images = copy_images_number(quantity_12_or_more, 12, max_folder, category, all_count_images,
                                              config_prog)

    # Пример вызова для quantity_6 и quantity_2 (если нужно)
    if quantity_6:
        all_count_images = copy_images_number(quantity_6, 6, max_folder, category, all_count_images, config_prog)
    if quantity_2:
        all_count_images = copy_images_number(quantity_2, 2, max_folder, category, all_count_images, config_prog)

    return all_count_images


def create_folder_order(articles, name_doc, list_model):
    from main import config_prog
    def copy_files_folder(arts, max_folder, target_size, category, list_model):
        A3_flag = False
        brand = arts[0].brand

        count = 1
        dir_count = 1
        count_images = 0
        all_count_images = 0
        sizes = {i.size for i in arts}
        directory = os.path.join(config_prog.current_dir, 'Заказ')
        os.makedirs(directory, exist_ok=True)
        if category == 'Брелки' or category == 'Зеркальца' or category == 'Значки' or category == 'Попсокеты':
            for size in sizes:

                filtered_arts = list(filter(lambda x: x.size == size, arts))

                if category == 'Зеркальца':
                    size_prod = '58'
                else:
                    size_prod = size

                all_count_images += created_good_images(filtered_arts, category, size_prod, name_doc, A3_flag,
                                                        list_model)
                combine_images_to_pdf(filtered_arts, f'{ready_path}/{category}_{size}.pdf', size=size_prod,
                                      A3_flag=A3_flag, category=category)

            return all_count_images

        sorted_arts = sorted(arts, key=lambda x: x.quantity, reverse=True)
        directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{dir_count}')
        os.makedirs(directory, exist_ok=True)
        if category == 'Наклейки 3-D':
            return created_stickers(sorted_arts, max_folder, category)
        else:
            if category == 'Наклейки квадратные':
                arts = sorted_arts
            if category == 'Попсокеты ДП':
                combine_images_to_pdf(arts, f'{ready_path}/{category}_{brand}.pdf', size=category,
                                      A3_flag=A3_flag, category=category)
            for index, article in enumerate(arts):
                image_paths = article.images.split(';')
                if target_size == 1:
                    filled_list = image_paths
                elif target_size == 2:
                    if article.quantity == 1:
                        filled_list = image_paths * 2
                    else:
                        filled_list = image_paths
                else:
                    target_size_block = article.quantity
                    filled_list = fill_list(image_paths, target_size_block)

                article_images_count = len(filled_list)
                if count_images + article_images_count > max_folder:
                    dir_count += 1
                    directory = os.path.join(config_prog.current_dir, 'Заказ', f'{category}_{dir_count}')
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
                        logger.error(image_path)
                        logger.error(ex)

        return all_count_images

    shutil.rmtree(os.path.join(config_prog.current_dir, 'Заказ'), ignore_errors=True)

    categories_dict = {
        'Наклейки 3-D': {
            'arts': [],
            'max_folder': 240,
            'target_size': None
        },
        'Попсокеты ДП': {
            'arts': [],
            'max_folder': 525,
            'target_size': 1

        },
        'Попсокеты': {
            'arts': [],
            'max_folder': None,
            'target_size': None

        },
        'Наклейки квадратные': {
            'arts': [],
            'max_folder': 64,
            'target_size': 1

        },
        'Наклейки на карту': {
            'arts': [],
            'max_folder': 38,
            'target_size': 1

        },
        'Брелки': {
            'arts': [],
            'max_folder': None,
            'target_size': None
        },
        'Зеркальца': {
            'arts': [],
            'max_folder': None,
            'target_size': None
        },
        'other_articles': {
            'arts': [],
            'max_folder': 1000,
            'target_size': 1

        },
    }

    for article in articles:
        if article.category == 'Наклейки 3-D':
            categories_dict['Наклейки 3-D']['arts'].append(article)
        elif article.brand == 'Дочке понравилось' and article.category == 'Попсокеты':
            categories_dict['Попсокеты ДП']['arts'].append(article)
        elif article.category == 'Наклейки квадратные':
            categories_dict['Наклейки квадратные']['arts'].append(article)
        elif article.category == 'Наклейки на карту':
            categories_dict['Наклейки на карту']['arts'].append(article)
        elif article.category == 'Брелки':
            categories_dict['Брелки']['arts'].append(article)
        elif article.category == 'Попсокеты':
            categories_dict['Попсокеты']['arts'].append(article)
        elif article.category == 'Зеркальца':
            categories_dict['Зеркальца']['arts'].append(article)
        else:
            categories_dict['other_articles']['arts'].append(article)
    all_images_count = 0

    for cat, value in categories_dict.items():
        if value['arts']:
            all_images_count += copy_files_folder(arts=value['arts'],
                                                  max_folder=value['max_folder'],
                                                  target_size=value['target_size'],
                                                  category=cat, list_model=list_model)

    return all_images_count, categories_dict


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
