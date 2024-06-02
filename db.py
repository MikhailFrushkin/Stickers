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
    size = CharField(verbose_name='Размер', null=True)

    skin = CharField(verbose_name='Путь к подложке', null=True)
    images = TextField(verbose_name='Пути в файлам')
    sticker = CharField(verbose_name='Путь к Шк', null=True)
    barcode = CharField(verbose_name='Баркод', null=True)

    union_file = CharField(verbose_name='Путь к объединенному файлу', null=True)
    blur_images = TextField(verbose_name='Пути в файлам c блюром', null=True)

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
    def create_art(cls, folder, art, quantity, size, category, brand, updated_at_in_site):
        from main import config_prog
        union_file = None
        blur_images = None
        sticker = None
        skin = None

        art = art.upper()
        # art = remove_russian_letters(art).upper()
        existing_article = cls.get_or_none(art=art, category=category, brand=brand)
        if existing_article:
            return existing_article

        folder_name = os.path.abspath(folder)
        image_filenames = []
        image_blur_filenames = []
        union_files = []

        for index, filename in enumerate(os.listdir(folder_name), start=1):
            file_path = os.path.join(folder_name, filename)
            if os.path.isfile(file_path):
                filename = filename.strip().lower()
                if filename.endswith('.pdf'):
                    sticker = file_path
                    if not os.path.exists(os.path.join(config_prog.params.get('Путь к шк'), filename)):
                        shutil.copy2(file_path, config_prog.params.get('Путь к шк'))
                elif 'blur' in filename:
                    image_blur_filenames.append(file_path)
                elif os.path.splitext(filename)[0].isdigit():
                    image_filenames.append(file_path)
                elif 'подложка' in filename:
                    skin = file_path
                elif 'все' in filename or 'макет' in filename:
                    union_files.append(file_path)
        images = ';'.join(image_filenames)
        if image_blur_filenames:
            blur_images = ';'.join(image_blur_filenames)
        if union_files:
            union_file = ';'.join(union_files)

        images_in_folder = len(image_filenames)
        if len(image_filenames) != quantity:
            logger.error(f'Не совпадает кол-во: {art}')
            return
        if not skin:
            logger.error(f'Нет подложки: {art}')
            return
        if not sticker:
            logger.warning(f'Нет шк: {art}')
        article = cls.create(art=art, folder=os.path.abspath(folder), category=category,
                             brand=brand, quantity=quantity, size=size, sticker=sticker, skin=skin,
                             updated_at_in_site=updated_at_in_site, union_file=union_file,
                             images=images, images_in_folder=images_in_folder, blur_images=blur_images)
        print(f'В базу добавлен артикул: {art}')

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


class NotFoundArt(Model):
    art = CharField(verbose_name='Артикул')
    doc_name = CharField(verbose_name='Имя файла')
    type = CharField(verbose_name='Тип', null=True)
    shop = CharField(verbose_name='Магазин', null=True)
    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.art


class Orders(Model):
    name = CharField(verbose_name='Имя заказа', index=True)
    category = CharField(verbose_name='Категория')
    found_arts_count = IntegerField(verbose_name='Найденно артикулов')
    found_arts = ManyToManyField(Article, backref='found_arts')
    not_found_arts_count = IntegerField(verbose_name='Не найденные артикула')
    not_found_arts = ManyToManyField(NotFoundArt, backref='not_found_arts')
    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.name
