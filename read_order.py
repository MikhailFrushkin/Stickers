import shutil
import pandas as pd
from loguru import logger
from peewee import DoesNotExist

from db import Article


def read_excel_file(file: str):
    """Чтение файла с заказом"""
    shutil.rmtree('Файлы связанные с заказом', ignore_errors=True)
    tuples_list = None
    found_articles = []
    not_found_arts = []

    try:
        df = pd.read_excel(file)
        art_column = None
        for i in df.columns:
            if 'артикул' in i.lower():
                art_column = i
        if not art_column:
            logger.error(f'Не найден столбец с артикулом')
            return
        # Применение upper() к столбцу с артикулами
        df[art_column] = df[art_column].apply(lambda x: x.upper() if isinstance(x, str) else x)
        arts_df = df[art_column]

        # Группировка и подсчет количества каждого артикула
        counts = arts_df.value_counts().reset_index()
        counts.columns = ['артикул', 'количество']

        # Преобразование в список кортежей
        tuples_list = counts.to_records(index=False).tolist()

    except Exception as ex:
        logger.error(ex)
    else:
        arts = arts_df.tolist()

        for art in arts:
            art_upper = art.upper()  # Приведение артикула из списка к верхнему регистру
            try:
                # Пытаемся найти артикул в базе данных
                article = Article.get(Article.art == art_upper)
                # Если артикул найден, добавляем его в список найденных объектов модели Article
                found_articles.append(article)
            except DoesNotExist:
                not_found_arts.append(art_upper)

    def sort_key(item):
        return item[2]

    for i in range(len(tuples_list)):
        art_upper = tuples_list[i][0].upper()
        try:
            _ = Article.get(Article.art == art_upper)
            tuples_list[i] += (True,)  # Добавление True к кортежу, если артикул найден
        except DoesNotExist:
            tuples_list[i] += (False,)
    sorted_tuples = sorted(tuples_list, key=sort_key)
    return sorted_tuples, found_articles, not_found_arts, arts


if __name__ == '__main__':
    file = r'1.xlsx'
    read_excel_file(file)
