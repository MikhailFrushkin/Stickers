import os
import re
import shutil
from datetime import datetime

from loguru import logger
from peewee import *

db = SqliteDatabase('base.db')


class Article(Model):
    art = CharField(verbose_name='Артикул', index=True)
    folder = CharField(verbose_name='Папка')
    nums = IntegerField(verbose_name='Кол-во')
    nums_in_folder = IntegerField(verbose_name='Кол-во файлов в папке')
    type = CharField(verbose_name='Тип')
    skin = CharField(verbose_name='Путь к подложке')
    images = TextField(verbose_name='Пути в файлам')
    sticker = CharField(verbose_name='Путь к Шк')

    shop = CharField(verbose_name='Магазин', default='AniKoya')
    created_at = DateTimeField(verbose_name='Время создания', default=datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return self.art


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


db.connect()
db.create_tables([Article, Orders, NotFoundArt])
db.close()