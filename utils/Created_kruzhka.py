from PIL import Image, ImageOps
from loguru import logger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from config import ready_path
from utils.utils import extract_number, chunk_list, update_progres_bar


def created_lists_orders_kruzhka(arts, max_folder, category, progress_step, progress_bar):
    image_paths = []
    for article in arts:
        image_list_art = article.images.split(';')
        image_list_sorted = sorted(image_list_art, key=extract_number)
        image_paths.extend(image_list_sorted)
    progress_step = progress_step / (len(image_paths)/len(arts))
    chunks = list(chunk_list(image_paths, 3))
    output_path = f'{ready_path}/Кружки.pdf'

    desired_width_mm = 203
    desired_height_mm = 91
    spacing_mm = 5
    points_per_inch = 72  # 1 дюйм = 72 пункта

    add_width = 0
    add_height = 0

    desired_width_pt = int(desired_width_mm * points_per_inch / 25.4) + add_width
    desired_height_pt = int(desired_height_mm * points_per_inch / 25.4) + add_height

    spacing_pt = int(spacing_mm * points_per_inch / 25.4)
    a4_width, a4_height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    page_count = 1
    all_count_image = 0
    for chunk in chunks:
        current_x = 10
        current_y = a4_height - spacing_pt - desired_height_pt
        for index,  img_path in enumerate(chunk, start=1):
            try:
                image = Image.open(img_path)
                mirrored_image = ImageOps.mirror(image)
                c.drawInlineImage(mirrored_image, current_x, current_y, width=desired_width_pt,
                                  height=desired_height_pt)

                current_y += - spacing_pt - desired_height_pt

            except Exception as ex:
                logger.error(f"Error processing image {img_path}: {ex}")
            else:
                all_count_image += 1
            update_progres_bar(progress_bar, progress_step)

        c.showPage()
        page_count += 1
    c.save()

    return all_count_image
