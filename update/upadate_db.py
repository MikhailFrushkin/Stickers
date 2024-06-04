import datetime
import os

from db import Article


def update_db_in_folder(config_prog):
    directory = config_prog.params.get('Путь к базе')
    for root, dirs, files in os.walk(directory):
        quantity = 0
        for file in files:
            filename, exp = os.path.splitext(file)
            if (filename.isdigit() or 'принт' in filename.lower()) and not file.endswith('.pdf'):
                quantity += 1
        if quantity:
            art = os.path.basename(root)
            category = os.path.basename(os.path.dirname(root))
            brand = os.path.basename(os.path.dirname(os.path.dirname(root)))
            if category == 'Значки' or category == 'Брелки':
                if '25' in art:
                    size = '25'
                elif '37' in art:
                    size = '37'
                elif '44' in art:
                    size = '44'
                elif '56' in art:
                    size = '56'
                else:
                    size = '37'
            elif category == 'Попсокеты' and brand == 'Дочке понравилось':
                size = '25'
            elif category == 'Попсокеты' and brand == 'AniKoya':
                size = '44'
            elif category == 'Зеркальца':
                size = '58'
            elif category == 'Мини постеры':
                size = 'А6'
            elif category == 'Постеры':
                size = 'А3'
            else:
                size = category
            Article.create_art(folder=root, art=art, quantity=quantity, size=size, category=category, brand=brand,
                               updated_at_in_site=datetime.datetime.now())
