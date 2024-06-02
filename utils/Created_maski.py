import os
import shutil

from PIL import Image, ImageOps
from loguru import logger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from config import ready_path
from utils.utils import extract_number, chunk_list, update_progres_bar


def created_maski(arts, max_folder, category, progress_step, progress_bar):
    image_paths = []
    output_path = f'{ready_path}\\{category}'
    os.makedirs(output_path, exist_ok=True)
    for index, article in enumerate(arts, start=1):
        image_list_art = article.union_file.split(';')
        for index2, file in enumerate(image_list_art, start=1):
            if len(image_list_art) == 1:
                new_name = f"{index}. {article.art}.cdr"
            else:
                new_name = f"{index}. {article.art}-{index2}.cdr"
            shutil.copy2(file, os.path.join(output_path, new_name))
        update_progres_bar(progress_bar, progress_step)

    return len(image_paths)
