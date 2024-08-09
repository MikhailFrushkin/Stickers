import datetime
import json
from pprint import pprint

import pandas as pd
import requests
from loguru import logger

headers = {'Content-Type': 'application/json'}
# domain = 'http://127.0.0.1:8000/api_rest'
domain = 'https://mycego.online/api_rest'


def get_products(save_file=False):
    """получение списка товаров с сайта"""
    response = None
    try:
        url = f'{domain}/all_product_list/'
        response = requests.get(url, headers=headers)
        data = response.json().get('data', [])
        if save_file:
            with open('site_all_prod.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    except Exception as ex:
        logger.error(f'Ошибка в запросе по api {ex}')
        if response:
            logger.error(response.status_code)
            logger.error(response.text)


if __name__ == '__main__':
    data_site = get_products(save_file=False)

    new_data_site = {}
    with open('result_wb.json', 'r', encoding='utf-8') as f2:
        data_wb = json.load(f2)
    diff = {}
    for key, value in data_wb.items():
        if key.strip().upper() not in data_site:
            diff[key] = value

    # print(f'В базе сайта: {len(data_site)}')
    # print(f'На вб: {len(data_wb)}')
    # print(f'Разница: {len(diff)}')
    #
    # with open('diff.json', 'w', encoding='utf-8') as f:
    #     json.dump(diff, f, ensure_ascii=False, indent=4)

    priority_arts_df = pd.read_excel('result.xlsx.xlsx')
    priority_arts = priority_arts_df['Артикул'].tolist()
    for i in priority_arts:
        if i.upper() not in data_site and 'SUMKA' not in i:
            print(i)
    bad_arts_df = pd.read_excel('bad_arts.xlsx')
    bad_arts = bad_arts_df['Артикул'].tolist()
    result = {}
    good_groups = ['Зеркальца', 'Значки', 'Постеры', 'Плакаты', 'Кольца-держатели для телефона', 'Кружки', 'Стикеры']
    for key, value in diff.items():
        if value['subjectName'] in good_groups and key in bad_arts and 'box' not in key.lower() and 'sumka' not in key.lower():
            result[key] = {
                "арт вб": value['art_wb'],
                "Категория": value['subjectName'],
                "брэнд": value['brand'],
                "ЛК": value['wb_lk_name'],
                'Ссылка ВБ': f"https://www.wildberries.ru/catalog/{value['art_wb']}/detail.aspx"
            }
    with open('diff_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    # df = pd.DataFrame.from_dict(result, orient='index')
    # df.reset_index(inplace=True)
    # df.rename(columns={'index': 'art'}, inplace=True)
    #
    # # Write the DataFrame to an Excel file
    # df.to_excel(f'Разница артикулов на {datetime.datetime.now().date()}.xlsx', index=False)
