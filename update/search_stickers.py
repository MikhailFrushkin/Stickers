import asyncio
import datetime
import os
from urllib.parse import quote

import aiofiles
import aiohttp
from loguru import logger


async def traverse_yandex_disk(session, folder_path, offset=0):
    limit = 1000
    url = (f"https://cloud-api.yandex.net/v1/disk/resources?path={quote(folder_path)}"
           f"&limit={limit}&offset={offset}"
           f"&fields=_embedded.items.name,_embedded.items.type,_embedded.items.size,"
           f"_embedded.items.file,_embedded.items.path,_embedded.offset,_embedded.total")
    try:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            tasks = []
            for item in data["_embedded"]["items"]:
                if item["type"] == "file" and item["name"].endswith(".pdf") and item['size'] < 30000:
                    result_dict[item["name"].lower().strip()] = item["file"]
                elif item["type"] == "dir":
                    task = traverse_yandex_disk(session, item["path"])  # Рекурсивный вызов
                    tasks.append(task)
            if tasks:
                await asyncio.gather(*tasks)  # Дождемся завершения всех рекурсивных вызовов

            total = data["_embedded"]["total"]
            offset += limit
            if offset < total:
                await traverse_yandex_disk(session, folder_path, offset=offset)

    except Exception as ex:
        pass
        # logger.error(f'Ошибка при поиске папки {folder_path} {ex}')


async def main_search(folder_path):
    async with aiohttp.ClientSession() as session:
        await traverse_yandex_disk(session, folder_path)


async def download_file(session, url, filename, semaphore, retry_count=3, retry_delay=10):
    for _ in range(retry_count):
        try:
            async with semaphore:
                async with session.get(url) as response:
                    async with aiofiles.open(filename, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await f.write(chunk)
                logger.info(f'Файл {filename} загружен')
                return  # Если загрузка успешна, выходим из цикла
        except Exception as ex:
            # logger.error(f'Ошибка при скачивании файла {filename}: {ex}')
            # logger.warning(f'Повторная попытка через {retry_delay} сек...')
            await asyncio.sleep(retry_delay)

    # logger.error(f'Не удалось скачать файл {filename} после нескольких попыток')


async def download_files(result_dict, directory_path):
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for filename, url in result_dict.items():
            filepath = os.path.join(directory_path, filename)
            if not os.path.exists(filepath):
                task = download_file(session, url, filepath, semaphore)
                tasks.append(task)
        await asyncio.gather(*tasks)


async def main_download():
    await download_files(result_dict, directory_path)


def main_search_sticker(config_prog, folder_path='/Значки ANIKOYA  02 23'):
    global headers
    global result_dict
    global directory_path
    start = datetime.datetime.now()
    directory_path = config_prog.params.get("Путь к шк")
    headers = {'Authorization': f'OAuth {config_prog.params.get("token")}'}
    result_dict = {}

    asyncio.run(main_search(folder_path))
    logger.warning(f'Найденно шк: {len(result_dict)} {datetime.datetime.now() - start}')

    asyncio.run(main_download())
