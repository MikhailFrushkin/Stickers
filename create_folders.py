import os
import shutil

from loguru import logger


def create_folder_order(articles, name_doc):
    from main import config_prog
    shutil.rmtree(os.path.join(config_prog.current_dir, 'Заказ'), ignore_errors=True)
    count = 1
    dir_count = 1
    count_images = 0
    directory = os.path.join(config_prog.current_dir, 'Заказ', f'{os.path.splitext(name_doc)[0]}_{dir_count}')
    os.makedirs(directory, exist_ok=True)

    for index, article in enumerate(articles, start=1):
        image_paths = article.images.split(';')
        article_images_count = sum(1 for _ in image_paths)
        if count_images + article_images_count > 240:
            dir_count += 1
            directory = os.path.join(config_prog.current_dir, 'Заказ', f'{os.path.splitext(name_doc)[0]}_{dir_count}')
            os.makedirs(directory, exist_ok=True)
            count_images = 0

        for image_path in image_paths:
            try:
                exp = os.path.splitext(os.path.basename(image_path))[1]
                new_filename = f"{index}_{count}{exp}"
                destination_path = os.path.join(directory, new_filename)
                shutil.copy2(image_path, destination_path)
                count += 1
                count_images += 1
            except Exception as ex:
                logger.error(ex)
    print('Готово')


def find_files_in_directory(directory, file_list):
    file_dict = {}
    found_files = []
    not_found_files = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_name = (file.replace('_1.pdf', '').
                         replace('_2.pdf', '').
                         replace('_3.pdf', '').
                         replace('.pdf', '').
                         lower().strip())
            file_dict[file_name] = os.path.join(directory, file)

    for poster in file_list:
        file_name = poster.lower().strip()
        if file_name in file_dict:
            found_files.append(file_dict[file_name])
        else:
            not_found_files.append(poster)
    return found_files, not_found_files


def create_order_shk(arts):
    from main import config_prog

    print(arts)

    # found_files_stickers, not_found_stickers = find_files_in_directory(config_prog.params.get('Путь к шк'), arts)
    # print(len(found_files_stickers))
    # print(len(not_found_stickers))