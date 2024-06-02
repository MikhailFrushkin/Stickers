import asyncio
import io
import tempfile
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
from loguru import logger
from reportlab.lib.pagesizes import A3, A6
from reportlab.pdfgen import canvas

from utils.utils import mm_to_px, extract_number, update_progres_bar, timer


def process_image_sync(image_path, adjusted_a6_width, adjusted_a6_height):
    try:
        k = 2.5
        with open(image_path, 'rb') as file:
            img_data = file.read()
        img = Image.open(io.BytesIO(img_data))
        img = img.rotate(90, expand=True)
        img.thumbnail((adjusted_a6_height * k, adjusted_a6_width * k), Image.LANCZOS)
        in_memory_buffer = io.BytesIO()
        img = img.convert("RGB")  # Convert image to RGB to ensure compatibility with JPEG format
        img.save(in_memory_buffer, format='JPEG')
        in_memory_buffer.seek(0)
        img_data = in_memory_buffer.getvalue()
        img_from_buffer = Image.open(io.BytesIO(img_data))
        return img_from_buffer
    except Exception as e:
        logger.error(f"Ошибка обработки изображения {image_path}: {e}")
        return None


async def generate_mini_posters(articles, output_file, progress_step, progress_bar):
    a6_width, a6_height = A6
    gap_mm = 2
    gap_px = mm_to_px(gap_mm)

    adjusted_a6_width = a6_width - 1.5 * gap_px
    adjusted_a6_height = a6_height - gap_px

    pdf_file = canvas.Canvas(output_file, pagesize=A3)
    image_index = 0
    total_images = 0
    batch_size = 5  # Количество изображений в одном пакете
    image_cache = {}

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        for article in articles:
            image_list_art = article.images.split(';')
            image_list_sorted = sorted(image_list_art, key=extract_number)
            batched_image_list = [image_list_sorted[i:i + batch_size] for i in
                                  range(0, len(image_list_sorted), batch_size)]

            for batch in batched_image_list:
                futures = []
                # list_display = '\n'.join(batch)
                # logger.info(f"{list_display}")

                for image_path in batch:
                    if image_path in image_cache:
                        futures.append(image_cache[image_path])
                    else:
                        future = loop.run_in_executor(executor, process_image_sync, image_path, adjusted_a6_width,
                                                      adjusted_a6_height)
                        futures.append(future)
                        image_cache[image_path] = future

                for future in asyncio.as_completed(futures):
                    img_from_buffer = await future
                    if img_from_buffer is not None:
                        if image_index % 8 == 0 and image_index != 0:
                            pdf_file.showPage()
                            image_index = 0

                        x_pos = (image_index % 2) * (adjusted_a6_height + gap_px) + gap_px
                        y_pos = (image_index // 2) * (adjusted_a6_width + gap_px) + gap_px

                        pdf_file.drawInlineImage(img_from_buffer, x_pos, y_pos, width=adjusted_a6_height,
                                                 height=adjusted_a6_width)
                        image_index += 1
                        total_images += 1

            update_progres_bar(progress_bar, progress_step)

    pdf_file.save()
    return total_images


def process_image_sync_a3(image_path):
    try:
        with open(image_path, 'rb') as file:
            img_data = file.read()
        img = Image.open(io.BytesIO(img_data))
        width, height = img.size
        if width > height:
            img = img.rotate(90, expand=True)
        return img
    except Exception as e:
        logger.error(f"Ошибка обработки изображения {image_path}: {e}")
        return None


def generate_posters(articles, output_file, progress_step, progress_bar):
    image_cache = {}  # Кеш для изображений
    temp_file_cache = {}  # Кеш для временных файлов
    total_img = sum(len(article.images.split(';')) for article in articles)
    try:
        c = canvas.Canvas(output_file, pagesize=A3)
        for article in articles:
            image_list_art = article.images.split(';')
            image_list_sorted = sorted(image_list_art, key=extract_number)
            for i, poster_file in enumerate(image_list_sorted):
                # logger.debug(poster_file)
                if poster_file in image_cache:
                    image = image_cache[poster_file]
                else:
                    image = process_image_sync_a3(poster_file)
                    if image is not None:
                        image_cache[poster_file] = image

                if image is not None:
                    if poster_file in temp_file_cache:
                        temp_file_name = temp_file_cache[poster_file]
                    else:
                        in_memory_buffer = io.BytesIO()
                        image = image.convert("RGB")  # Convert image to RGB to ensure compatibility with JPEG format
                        image.save(in_memory_buffer, format='JPEG', quality=100)  # Save with minimal compression
                        in_memory_buffer.seek(0)
                        img_data = in_memory_buffer.getvalue()
                        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                            temp_file.write(img_data)
                            temp_file_name = temp_file.name
                        temp_file_cache[poster_file] = temp_file_name

                    c.drawImage(temp_file_name, 0, 0, width=A3[0], height=A3[1])

                # Ensure a new page for each image
                c.showPage()
            update_progres_bar(progress_bar, progress_step)
        c.save()
    except Exception as ex:
        logger.error(ex)
    return total_img
#
# def generate_posters(articles, output_file, progress_step, progress_bar):
#     image_list = []
#     for article in articles:
#         image_list_art = article.images.split(';')
#         image_list_sorted = sorted(image_list_art, key=extract_number)
#         image_list.extend(image_list_sorted)
#
#     total_img = len(image_list)
#     try:
#         c = canvas.Canvas(output_file, pagesize=A3)
#         for article in articles:
#             image_list_art = article.images.split(';')
#             image_list_sorted = sorted(image_list_art, key=extract_number)
#             for i, poster_file in enumerate(image_list_sorted):
#                 logger.debug(poster_file)
#                 image = Image.open(poster_file)
#                 width, height = image.size
#                 if width > height:
#                     rotated_image = image.rotate(90, expand=True)
#                     try:
#                         with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
#                             rotated_image.save(temp_file.name, format='JPEG')
#                             c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
#                     except Exception as ex:
#                         logger.error(ex)
#                         with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
#                             rotated_image.save(temp_file.name, format='PNG')
#                             c.drawImage(temp_file.name, 0, 0, width=A3[0], height=A3[1])
#                 else:
#                     c.drawImage(poster_file, 0, 0, width=A3[0], height=A3[1])
#                 if i != total_img - 1:
#                     c.showPage()
#             update_progres_bar(progress_bar, progress_step)
#         c.save()
#     except Exception as ex:
#         logger.error(ex)
#     return total_img

#
# def process_image_sync(image_path, adjusted_a6_width, adjusted_a6_height):
#     try:
#         k = 2.5
#         with open(image_path, 'rb') as file:
#             img_data = file.read()
#         img = Image.open(io.BytesIO(img_data))
#         img = img.rotate(90, expand=True)
#         img.thumbnail((adjusted_a6_height * k, adjusted_a6_width * k), Image.LANCZOS)
#         in_memory_buffer = io.BytesIO()
#         img = img.convert("RGB")  # Convert image to RGB to ensure compatibility with JPEG format
#         img.save(in_memory_buffer, format='JPEG')
#         in_memory_buffer.seek(0)
#         img_data = in_memory_buffer.getvalue()
#         img_from_buffer = Image.open(io.BytesIO(img_data))
#         return img_from_buffer
#     except Exception as e:
#         logger.error(f"Ошибка обработки изображения {image_path}: {e}")
#         return None
#
#
# async def generate_mini_posters(articles, output_file, progress_step, progress_bar):
#     a6_width, a6_height = A6
#     gap_mm = 2
#     gap_px = mm_to_px(gap_mm)
#
#     adjusted_a6_width = a6_width - 1.5 * gap_px
#     adjusted_a6_height = a6_height - gap_px
#
#     pdf_file = canvas.Canvas(output_file, pagesize=A3)
#     image_index = 0
#     total_images = 0
#     image_cache = {}
#     article_cache = {}
#
#     loop = asyncio.get_event_loop()
#     with ThreadPoolExecutor() as executor:
#         for article in articles:
#             if article in article_cache:
#                 image_list_sorted = article_cache[article]
#             else:
#                 image_list_art = article.images.split(';')
#                 image_list_sorted = sorted(image_list_art, key=extract_number)
#                 article_cache[article] = image_list_sorted
#
#             futures = []
#
#             for image_path in image_list_sorted:
#                 if image_path in image_cache:
#                     futures.append(image_cache[image_path])
#                 else:
#                     future = loop.run_in_executor(executor, process_image_sync, image_path, adjusted_a6_width,
#                                                   adjusted_a6_height)
#                     futures.append(future)
#                     image_cache[image_path] = future
#
#             for future in asyncio.as_completed(futures):
#                 img_from_buffer = await future
#                 if img_from_buffer is not None:
#                     if image_index % 8 == 0 and image_index != 0:
#                         pdf_file.showPage()
#                         image_index = 0
#
#                     x_pos = (image_index % 2) * (adjusted_a6_height + gap_px) + gap_px
#                     y_pos = (image_index // 2) * (adjusted_a6_width + gap_px) + gap_px
#
#                     pdf_file.drawInlineImage(img_from_buffer, x_pos, y_pos, width=adjusted_a6_height,
#                                              height=adjusted_a6_width)
#                     image_index += 1
#                     total_images += 1
#
#             update_progres_bar(progress_bar, progress_step)
#
#     pdf_file.save()
#     return total_images


# def generate_mini_posters(articles, output_file, progress_step, progress_bar):
#     a6_width, a6_height = A6
#     gap_mm = 2
#     gap_px = mm_to_px(gap_mm)
#
#     adjusted_a6_width = a6_width - 1.5 * gap_px
#     adjusted_a6_height = a6_height - gap_px
#
#     pdf_file = canvas.Canvas(output_file, pagesize=A3)
#     image_index = 0
#     total_images = 0
#
#     in_memory_buffer = io.BytesIO()  # Create an in-memory buffer to store images
#
#     try:
#         # Цикл для обработки изображений и сохранения их в буфере
#         for article in articles:
#             image_list_art = article.images.split(';')
#             image_list_sorted = sorted(image_list_art, key=extract_number)
#
#             for image_path in image_list_sorted:
#                 logger.info(f'Добавление {image_path}')
#
#                 try:
#                     img = Image.open(image_path)
#                     img = img.rotate(90, expand=True)
#
#                     # Save image to in-memory buffer
#                     img.thumbnail((adjusted_a6_height * 2.5, adjusted_a6_width * 2.5), Image.LANCZOS)
#                     img.save(in_memory_buffer, format='PNG')  # Save the image to the in-memory buffer
#                     in_memory_buffer.seek(0)  # Move the cursor to the beginning of the buffer
#
#                     img_data = in_memory_buffer.getvalue()  # Получаем данные из буфера как строку
#
#                     # Создаем объект Image из строки
#                     img_from_buffer = Image.open(io.BytesIO(img_data))
#
#                     total_images += 1  # Увеличиваем счетчик изображений
#
#
#                 except Exception as e:
#                     logger.error(f"Ошибка обработки изображения {image_path}: {e}")
#
#                     in_memory_buffer.seek(0)  # Move the cursor to the beginning of the buffer для следующего изображения
#
#                     continue
#
#                 # Цикл для добавления изображений из буфера в документ PDF
#                 if image_index % 8 == 0 and image_index != 0:
#                     image_index = 0
#                     pdf_file.showPage()
#
#                 x_pos = (image_index % 2) * (adjusted_a6_height + gap_px) + gap_px
#                 y_pos = (image_index // 2) * (adjusted_a6_width + gap_px) + gap_px
#
#                 pdf_file.drawInlineImage(img_from_buffer, x_pos, y_pos, width=adjusted_a6_height,
#                                          height=adjusted_a6_width)
#                 image_index += 1
#             update_progres_bar(progress_bar, progress_step)
#     finally:
#         in_memory_buffer.close()  # Close the in-memory buffer
#
#     pdf_file.save()
#     return total_images


# def generate_mini_posters(articles, output_file, progress_step, progress_bar):
#     a6_width, a6_height = A6
#     gap_mm = 2
#     gap_px = mm_to_px(gap_mm)
#
#     adjusted_a6_width = a6_width - 1.5 * gap_px
#     adjusted_a6_height = a6_height - gap_px
#
#     pdf_file = canvas.Canvas(output_file, pagesize=A3)
#     image_index = 0
#     total_images = 0
#
#     for article in articles:
#         image_list_art = article.images.split(';')
#         image_list_sorted = sorted(image_list_art, key=extract_number)
#
#         for image_path in image_list_sorted:
#             logger.info(f'Добавление {image_path}')
#
#             try:
#                 img = Image.open(image_path)
#                 img = img.rotate(90, expand=True)
#
#                 if image_index % 8 == 0 and image_index != 0:
#                     image_index = 0
#                     pdf_file.showPage()
#
#                 x_pos = (image_index % 2) * (adjusted_a6_height + gap_px) + gap_px
#                 y_pos = (image_index // 2) * (adjusted_a6_width + gap_px) + gap_px
#
#                 pdf_file.drawInlineImage(img, x_pos, y_pos, width=adjusted_a6_height, height=adjusted_a6_width)
#                 image_index += 1
#                 total_images += 1
#
#             except Exception as e:
#                 logger.error(f"Ошибка обработки изображения {image_path}: {e}")
#
#         update_progres_bar(progress_bar, progress_step)
#
#     pdf_file.save()
#     return total_images
