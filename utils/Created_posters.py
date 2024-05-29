import re
import tempfile

from PIL import Image
from loguru import logger
from reportlab.lib.pagesizes import A3, A6
from reportlab.pdfgen import canvas


def mm_to_px(mm):
    return mm * 2.83465


def mm_to_mm(px):
    return px / 2.83465


# Функция для извлечения числовой части из имени файла
def extract_number(filename):
    match = re.search(r'(\d+)(?=\.\w+$)', filename)
    return int(match.group(1)) if match else 0


def generate_mini_posters(articles, output_file):
    image_list = []
    # for article in articles:
    #     image_list_art = article.images.split(';')
    #     image_list_sorted = sorted(image_list_art, key=extract_number)
    #     image_list.extend(image_list_sorted)
    a6_width, a6_height = A6
    gap_mm = 2
    gap_px = mm_to_px(gap_mm)

    # Уменьшаем доступное пространство на странице на размер разрыва
    adjusted_a6_width = a6_width - 1.5 * gap_px
    adjusted_a6_height = a6_height - gap_px

    # Создаем новый PDF-файл
    pdf_file = canvas.Canvas(output_file, pagesize=A3)
    image_index = 0
    total_images = 0
    for article in articles:
        image_list_art = article.images.split(';')
        image_list_sorted = sorted(image_list_art, key=extract_number)
        for image_path in image_list_sorted:
            logger.info(f'Добавление {image_path}')
            try:
                # Открываем изображение
                img = Image.open(image_path)
                img = img.rotate(90, expand=True)  # Поворачиваем изображение на 90 градусов

                # Переходим на следующую страницу, если текущая страница заполнена
                if image_index % 8 == 0 and image_index != 0:
                    image_index = 0
                    pdf_file.showPage()  # Переходим на следующую страницу

                # Рассчитываем координаты для размещения изображения на текущей странице
                x_pos = (image_index % 2) * (adjusted_a6_height + gap_px) + gap_px
                y_pos = (image_index // 2) * (adjusted_a6_width + gap_px) + gap_px

                # Вставляем изображение на страницу PDF
                pdf_file.drawInlineImage(img, x_pos, y_pos, width=adjusted_a6_height, height=adjusted_a6_width)
                image_index += 1
                total_images += 1
                # Закрываем изображение
                img.close()

            except Exception as e:
                logger.error(f"Ошибка обработки изображения {image_path}: {e}")

    pdf_file.save()
    return total_images


def generate_posters(articles, output_file):
    image_list = []
    for article in articles:
        image_list_art = article.images.split(';')
        image_list_sorted = sorted(image_list_art, key=extract_number)
        image_list.extend(image_list_sorted)

    total_img = len(image_list)
    try:
        c = canvas.Canvas(output_file, pagesize=A3)
        for i, poster_file in enumerate(image_list):
            logger.debug(poster_file)
            image = Image.open(poster_file)
            width, height = image.size
            if width > height:
                rotated_image = image.rotate(90, expand=True)
                try:
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='JPEG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
                except Exception as ex:
                    logger.error(ex)
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        rotated_image.save(temp_file.name, format='PNG')
                        c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
            else:
                c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
            if i != total_img - 1:
                c.showPage()
        c.save()
    except Exception as ex:
        logger.error(ex)
    return total_img
