import os
import re
import shutil
from datetime import datetime

from loguru import logger
from peewee import *

from utils.utils import remove_russian_letters

db = SqliteDatabase('base/base.db')


class Article(Model):
    art = CharField(verbose_name='Артикул', index=True)
    folder = CharField(verbose_name='Папка')
    quantity = IntegerField(verbose_name='Кол-во')
    images_in_folder = IntegerField(verbose_name='Кол-во файлов в папке')

    brand = CharField(verbose_name='Бренд', default='AniKoya')
    category = CharField(verbose_name='Категория')

    skin = CharField(verbose_name='Путь к подложке', null=True)
    images = TextField(verbose_name='Пути в файлам')
    sticker = CharField(verbose_name='Путь к Шк', null=True)

    one_pdf = CharField(verbose_name='Путь к объединенному пдф', null=True)

    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)
    updated_at_in_site = DateTimeField(verbose_name='Время обновления на сайте', null=True)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.art = self.art.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.art

    @classmethod
    def create_art(cls, folder, art, quantity, category, brand, updated_at_in_site, one_pdf=None):
        from main import config_prog

        sticker = None
        skin = None

        art = remove_russian_letters(art).upper()
        existing_article = cls.get_or_none(art=art, category=category, brand=brand,
                                           updated_at_in_site=None, one_pdf=one_pdf)
        if existing_article:
            return existing_article
        else:
            existing_article = cls.get_or_none(art=art, category=category, brand=brand,
                                               updated_at_in_site=updated_at_in_site, one_pdf=one_pdf)
        if existing_article:
            return existing_article
        folder_name = os.path.abspath(folder)
        image_filenames = []

        for index, filename in enumerate(os.listdir(folder_name), start=1):
            file_path = os.path.join(folder_name, filename)
            if os.path.isfile(file_path):
                if filename.endswith('.pdf'):
                    sticker = file_path
                    if not os.path.exists(os.path.join(config_prog.params.get('Путь к шк'), filename)):
                        shutil.copy2(file_path, config_prog.params.get('Путь к шк'))
                elif filename.strip()[0].isdigit():
                    image_filenames.append(file_path)
                elif 'подложка' in filename.lower():
                    skin = file_path
        images = ';'.join(image_filenames)
        images_in_folder = len(image_filenames)
        if len(image_filenames) != quantity:
            logger.error(f'не совпадает кол-во: {art}')
            return
        article = cls.create(art=art, folder=os.path.abspath(folder), category=category,
                             brand=brand, quantity=quantity, sticker=sticker, skin=skin,
                             updated_at_in_site=updated_at_in_site, one_pdf=one_pdf,
                             images=images, images_in_folder=images_in_folder)
        logger.success(f'В базу добавлен артикул: {art}')

        return article

    @classmethod
    def delete_by_art(cls, art, category, brand):
        """
        Удаляет запись из базы данных по артикулу и соответствующую папку на диске.
        :param art: Артикул записи, которую нужно удалить.
        :return: True, если запись была найдена и удалена, иначе False.
        """
        # Найти запись с заданным артикулом
        try:
            article = cls.get(cls.art == art, cls.category == category, cls.brand == brand)
        except cls.DoesNotExist:
            return False

        folder_path = article.folder
        query = cls.delete().where(cls.art == art, cls.category == category, cls.brand == brand)
        deleted = query.execute()

        # Если запись была успешно удалена, удалить и папку
        if deleted and folder_path:
            try:
                shutil.rmtree(folder_path)
                return True
            except Exception as e:
                logger.error(f"Ошибка при удалении папки: {e}")
                return False
        return False


class Orders(Model):
    name = CharField(verbose_name='Имя заказа', index=True)
    found_arts = IntegerField(verbose_name='Найденно артикулов')
    not_found_arts = IntegerField(verbose_name='Не найденные артикула')
    type = CharField(verbose_name='Тип')
    shop = CharField(verbose_name='Магазин', default='AniKoya')
    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.name


class NotFoundArt(Model):
    art = CharField(verbose_name='Артикул', index=True)
    type = CharField(verbose_name='Тип')
    shop = CharField(verbose_name='Магазин', default='AniKoya')
    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.art
