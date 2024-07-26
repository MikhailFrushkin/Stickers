import shutil
import pandas as pd
from loguru import logger
from peewee import DoesNotExist, fn
from config import config_prog
from db import Article


def read_excel_file(file: str):
    """Чтение файла с заказом"""
    shutil.rmtree('Файлы связанные с заказом', ignore_errors=True)
    tuples_list = None
    found_articles = []
    not_found_arts = []
    arts = []
    try:
        if file.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            logger.error(f'Ошибка чтения файла {file}')
            return
        art_column = None
        tuples_list = list()
        df = df.fillna("")

        if len(df.columns) == 2:
            config_prog.union_arts = True
            rows = []
            df.columns = ['артикул', 'количество']
            art_column = 'артикул'
            df['количество'] = df['количество'].astype(int)
            # Применение upper() к столбцу с артикулами
            df[art_column] = df[art_column].apply(lambda x: x.upper() if isinstance(x, str) else x)
            # Дублирование артикулов в соответствии с их количеством
            for index, row in df.iterrows():
                for i in range(int(row['количество'])):
                    rows.append({'артикул': row['артикул'], 'количество': 1})
            new_df = pd.DataFrame(rows)
            arts_df = new_df[new_df[art_column] != ""][art_column]
            # Группировка и подсчет количества каждого артикула
            counts = arts_df.value_counts().reset_index()
            counts.columns = ['артикул', 'количество']

            # Преобразование в список кортежей
            tuples_list = counts.to_records(index=False).tolist()
        else:
            config_prog.union_arts = False
            for i in df.columns:
                if 'артикул продавца' in i.lower():
                    art_column = i
                    break
            if not art_column:
                logger.error(f'Не найден столбец с артикулом "Артикул продавца"')
                return
            # Применение upper() к столбцу с артикулами
            df[art_column] = df[art_column].apply(lambda x: x.upper() if isinstance(x, str) else x)
            # Фильтрация значений "" из столбца с артикулами
            arts_df = df[df[art_column] != ""][art_column]
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
                # Пытаемся найти артикул в базе данных, игнорируя префикс "DOP_"
                article = Article.select().where(fn.REPLACE(Article.art, "DOP_", "") == art_upper).order_by(
                    Article.updated_at_in_site).first()
                # Если артикул найден, добавляем его в список найденных объектов модели Article
                if article:
                    found_articles.append(article)
                else:
                    not_found_arts.append(art_upper)
            except Exception as ex:
                logger.error(ex)

    def sort_key(item):
        return item[2]

    for i in range(len(tuples_list)):
        art_upper = tuples_list[i][0].upper()
        try:
            _ = Article.get(fn.REPLACE(Article.art, "DOP_", "") == art_upper)
            tuples_list[i] += (True,)  # Добавление True к кортежу, если артикул найден
        except DoesNotExist:
            tuples_list[i] += (False,)
    sorted_tuples = sorted(tuples_list, key=sort_key)

    return sorted_tuples, found_articles, not_found_arts, arts


if __name__ == '__main__':
    file = r'1.xlsx'
    read_excel_file(file)
