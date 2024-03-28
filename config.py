import json
from pathlib import Path

from loguru import logger

headers = {'Content-Type': 'application/json'}
# domain = 'http://127.0.0.1:8000/api_rest'
domain = 'https://mycego.online/api_rest'


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
                    "3D наклейки": True,
                    "Наклейки на карту": False,
                    "Брелки": False,
                    "Квадратные наклейки": False,
                    "Кружки-сердечко": False
                },
                "Частота обновления": 120,
                "Путь к базе": "C:\\База",
                "Путь к шк": "C:\\База\\ШК",
                "token": ""
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


if __name__ == '__main__':
    # Создаем объект класса Config
    config = Config()

    # Выводим текущие параметры
    print("Текущие параметры конфигурации:")
    print(config.params)

    # Пример изменения параметра и сохранение его в файл
    config.set_param("Автоматическое обновление", True)
    config.set_param("Частота обновления", 60)

    # Выводим обновленные параметры
    print("\nОбновленные параметры конфигурации:")
    print(config.params)
