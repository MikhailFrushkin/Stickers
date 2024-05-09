import json
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader, PdfWriter
from loguru import logger
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from config import ready_path

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
Image.MAX_IMAGE_PIXELS = None


def add_header_and_footer_to_pdf(pdf_file, footer_text, A3_flag):
    """Надписи сверху пдф файла и снизу"""
    # Open the original PDF and extract its content
    with open(pdf_file, "rb") as pdf:
        pdf_content = BytesIO(pdf.read())
    if A3_flag:
        with open('Настройки\\Параметры значков_A3.json', 'r') as file:
            config = json.load(file)
        pagesize = A3
        size = 8
    else:
        with open('Настройки\\Параметры значков.json', 'r') as file:
            config = json.load(file)
        pagesize = A4
        size = 10

    x2, y2 = config['pdf down']['x'], config['pdf down']['y']
    # Load pages from the original PDF and add header and footer to each page
    reader = PdfReader(pdf_content)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        try:
            page = reader.pages[page_num]

            # Create a canvas for the page
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=pagesize)

            # Add the header text (centered) to the canvas
            can.setFont("Arial", size=size)
            if A3_flag:
                can.drawCentredString(x2, y2, f"{footer_text} - Стр.{page_num + 1}")
            else:
                can.drawCentredString(x2, y2, f"{footer_text} - Стр.{page_num + 1}")
            can.save()
            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])

            writer.add_page(page)
        except Exception as ex:
            logger.error(ex)
    with open(pdf_file, "wb") as output_pdf:
        writer.write(output_pdf)


def combine_images_to_pdf(input_files, output_pdf, size=None, progress=None, name_doc=None, A3_flag=False):
    """Создание файла с наклейками"""
    bad_skin_list = []
    x_offset = 20
    y_offset = 20
    big_list_skin = []
    for i in input_files:
        if i.blur_images >= 40:
            big_list_skin.append(i)
    input_files = [i for i in input_files if i not in big_list_skin]
    if A3_flag:
        c = canvas.Canvas(output_pdf, pagesize=landscape(A3), pageCompression=1)
        img_width = (A4[0] - 2 * x_offset) / 3
        img_height = (A4[1] - 2 * y_offset) / 3 - 10

        x_positions = [
            x_offset, x_offset + img_width + 10, x_offset + 2 * (img_width + 10),
                      x_offset + 3 * (img_width + 10), x_offset + 4 * (img_width + 10), x_offset + 5 * (img_width + 10)
        ]
        y_positions = [
            A3[0] - y_offset, A3[0] - y_offset - img_height - 15, A3[0] - y_offset - 2 * (img_height + 15)
        ]

        total_images = len(input_files)
        images_per_page = 18  # Размещаем 18 изображений на одной странице
        num_pages = (total_images + images_per_page - 1) // images_per_page

        for page in range(num_pages):
            start_idx = page * images_per_page
            end_idx = min(start_idx + images_per_page, total_images)
            for i, img in enumerate(input_files[start_idx:end_idx]):
                x = x_positions[i % 6]
                y = y_positions[i // 6]
                c.setFont("Helvetica-Bold", 6)
                c.drawString(x, y + 1, f"#{img.num_on_list}  {img.art}")
                try:
                    logger.success(f"Добавился подложка {img.num_on_list}   {img.art}")
                    progress.update_progress()
                    c.drawImage(img.skin, x - 10, y - img_height - 5, width=img_width, height=img_height)
                except Exception as ex:
                    logger.error(f"Не удалось добавить подложку для {img.art} {ex}")
            c.showPage()

        c.save()
    else:
        c = canvas.Canvas(output_pdf, pagesize=A4)
        img_width = (A4[0] - 2 * x_offset) / 3
        img_height = (A4[1] - 2 * y_offset) / 3 - 5

        x_positions = [x_offset, x_offset + img_width + 5, x_offset + 2 * (img_width + 5)]
        y_positions = [A4[1] - y_offset, A4[1] - y_offset - img_height - 10, A4[1] - y_offset - 2 * (img_height + 10)]

        total_images = len(input_files)
        images_per_page = 9
        num_pages = (total_images + images_per_page - 1) // images_per_page

        for page in range(num_pages):
            start_idx = page * images_per_page
            end_idx = min(start_idx + images_per_page, total_images)
            for i, img in enumerate(input_files[start_idx:end_idx]):
                if not os.path.exists(img.skin):
                    logger.debug(f'{img.skin} не существует')
                else:
                    x = x_positions[i % 3]
                    y = y_positions[i // 3]
                    c.setFont("Helvetica-Bold", 8)
                    c.drawString(x, y + 2, f"#{img.num_on_list}     {img.art}")
                    try:
                        logger.success(f"Добавился скин {img.num_on_list}     {img.art}")
                        progress.update_progress()
                        c.drawImage(img.skin, x - 10, y - img_height, width=img_width, height=img_height)
                    except Exception as ex:
                        logger.error(f"Не удалось добавить подложку для {img.art} {ex}")
                        try:
                            c.drawImage(img.skin, x - 10, y - img_height, width=img_width, height=img_height)
                        except Exception as ex:
                            logger.error(f"Не удалось добавить подложку для {img.art} {ex} 2й раз")
                            bad_skin_list.append(img.art)

            c.showPage()
        c.save()

    if big_list_skin:
        c = canvas.Canvas(f"Файлы на печать/Большие подложки {size}.pdf", pagesize=A4)
        img_width = 505
        img_height = 674
        for i, img in enumerate(big_list_skin):
            c.setFont("Helvetica-Bold", 8)
            c.drawString(30, 30, f"#{img.num_on_list}     {img.art}")
            try:
                logger.success(f"Добавился скин {img.num_on_list}     {img.art}")
                progress.update_progress()

                c.drawImage(img.skin, 40, 100, width=img_width, height=img_height)
            except Exception as ex:
                logger.error(f"Не удалось добавить подложку для {img.art} {ex}")
            c.showPage()
        c.save()
    add_header_and_footer_to_pdf(output_pdf, name_doc, A3_flag=A3_flag)
    return bad_skin_list


def write_images_art(image, text):
    """Нанесения номера на значке"""
    width, height = image.size
    draw = ImageDraw.Draw(image)

    # Calculate the font size based on the image width
    font_size = int(width / 18)
    font = ImageFont.truetype("arial.ttf", size=font_size)

    # Добавляем надпись в правый верхний угол
    bbox1 = draw.textbbox((0, 0), text, font=font)
    x1 = width - bbox1[2] - 125
    y1 = 5
    draw.text((x1, y1), text, font=font, fill="black")

    return image


def write_page_name(image, text, x, y):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 40)

    draw.text((x, y), text, font=font, fill="black")

    return image


def distribute_images(queryset, size, category, a3_flag, count) -> tuple:
    if a3_flag:
        with open('Настройки\\Параметры значков_A3.json', 'r') as file:
            config = json.load(file)
    else:
        with open('Настройки\\Параметры значков.json', 'r') as file:
            config = json.load(file)
    nums = config[f'{str(size)}']['nums']
    list_arts = [[None, i.images_in_folder, i.blur_images, i.id] for i in queryset]
    list_arts = sorted(list_arts, key=lambda x: x[1], reverse=True)
    # Список для хранения наборов
    sets_of_orders = []

    current_set = []  # Текущий набор
    current_count = 0  # Текущее количество элементов в наборе
    while len(list_arts) > 0:
        for order in list_arts[:]:
            if order[1] > nums:
                image_list = [(i.strip(), count) for i in order[2].split(';')]
                if (current_count + (len(image_list) % nums)) <= nums and ((len(image_list) % nums) != 0):
                    current_set.extend(image_list[-(order[1] % nums):])
                    current_count += len(image_list) % nums
                    full_lists = order[1] // nums
                    for i in range(full_lists):
                        sets_of_orders.append(image_list[nums * i:nums * i + nums])
                    list_arts.remove(order)
                    count += 1
                elif (order[1] > nums) and current_count == 0:
                    full_lists = order[1] // nums
                    for i in range(full_lists):
                        sets_of_orders.append(image_list[nums * i:nums * i + nums])
                    if order[1] % nums != 0:
                        current_set.extend(image_list[-(order[1] % nums):])
                    list_arts.remove(order)
                    count += 1
                else:
                    sets_of_orders.append(current_set)
                    current_set = []
                    current_count = 0
                    full_lists = order[1] // nums
                    for i in range(full_lists):
                        sets_of_orders.append(image_list[nums * i:nums * i + nums])

                    if order[1] % nums != 0:
                        current_set.extend(image_list[-(order[1] % nums):])
                        current_count += len(image_list[-(order[1] % nums):])
                    list_arts.remove(order)
                    count += 1

            if (current_count + order[1]) <= nums:
                current_set.extend([[i, count] for i in order[2].split(';')])
                current_count += order[1]
                list_arts.remove(order)
                count += 1
                if current_count == nums:
                    sets_of_orders.append(current_set)
                    current_set = []
                    current_count = 0
                    break
            continue
        if current_count != 0:
            sets_of_orders.append(current_set)
        if len(list_arts) == 1:
            sets_of_orders.append([[i, count] for i in list_arts[0][2].split(';')])
            list_arts.remove(list_arts[0])
            count += 1

        if list_arts:
            current_set = []
            current_set.extend([[i, count] for i in list_arts[0][2].split(';')])
            current_count = list_arts[0][1]
            list_arts.remove(list_arts[0])
            count += 1

    sum_image = sum([len(i) for i in sets_of_orders])
    sum_lists = len(sets_of_orders)
    logger.info(f'Сумма изображений {category} {size}: {sum_image}')
    # logger.info(f'Сумма значков на листах: {set([len(i) for i in sets_of_orders])}')
    logger.info(f'Количество листов: {sum_lists}')
    return sets_of_orders, count, sum_image, sum_lists


def create_contact_sheet(images, size, name_doc, category, A3_flag=False):
    border_color = (0, 0, 0, 255)  # Черный цвет рамки
    border_width = 1  # Ширина рамки в пикселях
    folder = f'{ready_path}/{category}/{size}'
    os.makedirs(folder, exist_ok=True)
    if A3_flag:
        a4_width = 3508
        a4_height = 4961
        with open('Настройки\\Параметры значков_A3.json', 'r') as file:
            config = json.load(file)
    else:
        a4_width = 2480
        a4_height = 3508
        with open('Настройки\\Параметры значков.json', 'r') as file:
            config = json.load(file)
    image_width_mm = config[f'{str(size)}']['diameter']
    image_height_mm = config[f'{str(size)}']['diameter']

    # Convert mm to inches (1 inch = 25.4 mm)
    mm_to_inch = 25.4
    image_width = int(image_width_mm * 300 / mm_to_inch)
    image_height = int(image_height_mm * 300 / mm_to_inch)

    for index, img in enumerate(images, start=1):
        try:
            contact_sheet = Image.new('RGBA', (a4_width, a4_height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(contact_sheet)

            for i in range(config[f'{str(size)}']['ICONS_PER_COL']):
                for j in range(config[f'{str(size)}']['ICONS_PER_ROW']):
                    try:
                        image = Image.open(img[i * config[f'{str(size)}']['ICONS_PER_ROW'] + j][0].strip())
                        image = write_images_art(image,
                                                 f'{img[i * config[f"{str(size)}"]["ICONS_PER_ROW"] + j][1]}')
                        image = image.resize((image_width, image_height), Image.LANCZOS)
                    except Exception as ex:
                        break
                    try:
                        if size == '56':
                            contact_sheet.paste(image, (j * image_width - 10, i * image_height + 10 * (i + 1)))
                            border_rect = [j * image_width - 10, i * image_height + 10 * (i + 1),
                                           (j + 1) * image_width - 10, (i + 1) * image_height + 10 * (i + 1)]
                        elif size == '25' or size == '44':
                            contact_sheet.paste(image, (j * image_width + 100, i * image_height + 10 * (i + 1)))
                            border_rect = [j * image_width + 100, i * image_height + 10 * (i + 1),
                                           (j + 1) * image_width + 100, (i + 1) * image_height + 10 * (i + 1)]
                        else:
                            contact_sheet.paste(image, (j * image_width + 10, i * image_height + 10 * (i + 1)))
                            border_rect = [j * image_width + 10, i * image_height + 10 * (i + 1),
                                           (j + 1) * image_width + 10, (i + 1) * image_height + 10 * (i + 1)]
                    except Exception as ex:
                        break
                    try:
                        circle_center = ((border_rect[0] + border_rect[2]) // 2, (border_rect[1] + border_rect[3]) // 2)
                        circle_radius = min((border_rect[2] - border_rect[0]) // 2,
                                            (border_rect[3] - border_rect[1]) // 2)
                        draw.ellipse((circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                                      circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                                     outline=border_color, width=border_width)
                    except Exception as ex:
                        break
            path_ready = f'{folder}/{index}.png'

            x = config['number on badge']['x'] - 80
            y = config['number on badge']['y']
            image = write_page_name(contact_sheet, f"{name_doc} Стр.{index}", x, y)
            image.save(path_ready)

        except Exception as ex:
            logger.error(ex)
            logger.error(img)


def created_good_images(records, category, size, name_doc, A3_flag=False):
    sum_image = 0
    try:
        count = 1
        sets_of_orders, count, sum_image, sum_lists = distribute_images(records, size, category, A3_flag, count)
        # try:
        #     logger.debug(f'Создание наклеек {size}')
        #     combine_images_to_pdf(queryset.order_by(Orders.num_on_list),
        #                                           f"{ready_path}/Наклейки {size}.pdf", size, progress, name_doc,
        #                                           A3_flag)
        # except Exception as ex:
        #     logger.error(ex)
        #     logger.error(f'Не удалось создать файл с наклейками {size}')
        #
        try:
            create_contact_sheet(sets_of_orders, size, name_doc, category, A3_flag)
        except Exception as ex:
            logger.error(ex)
    except Exception as ex:
        logger.error(ex)
    return sum_image

