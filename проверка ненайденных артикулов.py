import glob
import json
import os
import shutil

import pandas as pd
import requests
from loguru import logger

from utils.utils import df_in_xlsx

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
token = data.get('token')


def get_file_excel():
    headers = {
        "Authorization": f"OAuth {token}"
    }

    params = {
        "path": 'Отчеты',
        "fields": "_embedded.items",
        "limit": 1000
    }

    response = requests.get("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)

    if response.status_code == 200:
        files = response.json().get('_embedded', {}).get('items', None)
        result = [(i['name'], i['file']) for i in files]
        return result
    else:
        logger.error("Error:", response.status_code)


def download_file(destination_path, url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
            logger.info(f"File downloaded successfully: {destination_path}")
        else:
            logger.error(f"Error {response.status_code} while downloading file: {url}")
    except requests.RequestException as e:
        logger.error(f"Error during downloading file: {e}")


def read_all_files():
    combined_df = pd.DataFrame(columns=['Артикул'])
    for file in glob.glob(os.path.join(directory, '*.xlsx')):
        df = pd.read_excel(file)

        # Выбираем только столбец "Артикул"
        if 'Артикул' in df.columns:
            df = df[['Артикул']]

            # Добавляем к общему DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    combined_df.drop_duplicates(inplace=True)
    df_in_xlsx(df=combined_df, filename='Ненайденные артикула с отчетов')


if __name__ == '__main__':
    directory = 'temp_excel'
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)
    files = get_file_excel()

    for name, url in files:
        destination_path = os.path.join(directory, name)
        download_file(destination_path, url)

    read_all_files()
