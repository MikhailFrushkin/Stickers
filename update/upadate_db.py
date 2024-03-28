import os

from db import Article


def update_db_in_folder(config_prog):
    directory = config_prog.params.get('Путь к базе')
    count = 1
    for root, dirs, files in os.walk(directory):
        quantity = 0
        for file in files:
            if file[0].isdigit() and not file.endswith('.pdf'):
                quantity += 1
        if quantity:
            art = os.path.basename(root)
            category = os.path.basename(os.path.dirname(root))
            brand = os.path.basename(os.path.dirname(os.path.dirname(root)))
            Article.create_art(folder=root, art=art, quantity=quantity, category=category, brand=brand,
                               updated_at_in_site=None, one_pdf=None)
            count += 1
