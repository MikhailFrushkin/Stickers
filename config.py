import json
from pathlib import Path

from loguru import logger

headers = {'Content-Type': 'application/json'}
# domain = 'http://127.0.0.1:8000/api_rest'
domain = 'https://mycego.online/api_rest'
base_folder = 'Новая база (1)'
ready_path = 'Заказ'

data_blur = {
        '25': 1.40,
        '37': 1.30,
        '44': 1.18,
        '56': 1.14,
        '58': 1.12,
    }

class Config:
    def __init__(self, filename='config.json'):
        # Устанавливаем имя файла конфигурации и текущую директорию
        self.filename = filename
        self.current_dir = Path.cwd()
        # Загружаем параметры из файла, если файл существует, иначе устанавливаем параметры по умолчанию
        self.load_from_file()

    def save_to_file(self):
        # Сохраняем текущие параметры в файл JSON
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.params, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        # Проверяем, существует ли файл конфигурации
        if not Path(self.filename).exists():
            print('Файл конфигурации не существует. Создан новый.')
            # Если файл не существует, создаем новый файл и записываем в него параметры по умолчанию
            self.params = {
                "Автоматическое обновление": True,
                "categories": {
                    "Значки": False,
                    "Попсокеты": False,
                    "Зеркальца": False,
                    "Постеры": False,
                    "Кружки": False,
                    "3D наклейки": False,
                    "Наклейки на карту": False,
                    "Брелки": False,
                    "Наклейки квадратные": False,
                    "Кружки-сердечко": False,
                    "Мини постеры": False,
                    "Маски": False
                },
                "Частота обновления": 120,
                "Путь к базе": "C:\\База",
                "Путь к шк": "C:\\База\\ШК",
                "token": "",
                "machin_name": "Комп не назван"
            }
            self.save_to_file()  # Сохраняем параметры в новый файл
        else:
            # Если файл существует, загружаем параметры из него
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.params = json.load(f)

    def set_param(self, key, value):
        # Устанавливаем новое значение для параметра

        if key in self.params:
            self.params[key] = value
            self.save_to_file()  # Сохраняем обновленные параметры в файл
        else:
            if key in self.params.get('categories'):
                self.params['categories'][key] = value
            else:
                logger.error(f'Параметр "{key}" не найден.')
        self.save_to_file()

    def reload_settings(self):
        # Перезагружаем настройки из файла
        self.load_from_file()


config_prog = Config()