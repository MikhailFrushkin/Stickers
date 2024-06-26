import os
import re
import time

import pandas as pd
from loguru import logger
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.success(f"Время выполнения функции {func.__name__}: {round(execution_time, 2)} сек.")
        return result

    return wrapper


def chunk_list(lst, chunk_size=4):
    """Divide a list into chunks of a specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_russian_letters(input_string):
    """Удаление русских букв из строки"""
    # Используем регулярное выражение для поиска всех русских букв
    russian_letters_pattern = re.compile('[а-яА-Я]')

    # Заменяем найденные русские буквы на пустую строку
    result_string = re.sub(russian_letters_pattern, '', input_string)

    return result_string.strip()


def replace_bad_simbols(row: str) -> str:
    """Удаляет символы из строки которые нельзя указывать в названии файлов"""
    bad = r'[\?\/\\\:\*\"><\|]'
    new_row = re.sub(bad, '', row)
    return new_row


def update_progres_bar(progress_bar, progress_step):
    current_value = progress_bar.value()
    new_value = current_value + progress_step
    progress_bar.setValue(int(new_value))


def split_row(row: str) -> list:
    """Разделяет строку по делителям"""
    delimiters = r'[\\/|, ]'
    substrings = re.split(delimiters, row)
    substrings = [i for i in substrings if i]
    return substrings


def df_in_xlsx(df: pd.DataFrame, filename: str, directory: str = 'Файлы связанные с заказом', max_width: int = 50):
    """Запись датафрейма в файл"""
    workbook = Workbook()
    sheet = workbook.active
    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)
    for column in sheet.columns:
        column_letter = column[0].column_letter
        max_length = max(len(str(cell.value)) for cell in column)
        adjusted_width = min(max_length + 2, max_width)
        sheet.column_dimensions[column_letter].width = adjusted_width

    os.makedirs(directory, exist_ok=True)
    workbook.save(f"{directory}\\{filename}.xlsx")


def rename_files(file_path: str, new_name: str):
    """Преименовывание файлов"""
    try:
        base_path = os.path.dirname(file_path)
        file_extension = os.path.splitext(file_path)[1]
        new_path = os.path.join(base_path, new_name + file_extension)
        os.rename(file_path, new_path)
        # logger.debug(f'Переименован файл {file_path} в {new_path}')
        return new_path
    except Exception as ex:
        logger.error(f'не удалось переименовать файл {file_path}\n{ex}')


def mm_to_points(mm):
    inches = mm / 254
    points = inches * 72
    return points


def mm_to_px(mm):
    return mm * 2.83465


def mm_to_mm(px):
    return px / 2.83465


# Функция для извлечения числовой части из имени файла
def extract_number(filename):
    match = re.search(r'(\d+)(?=\.\w+$)', filename)
    return int(match.group(1)) if match else 0