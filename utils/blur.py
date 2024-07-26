import cv2
import numpy as np
from loguru import logger
from pathlib import Path
from config import data_blur


def blur_image(image_path, output_path, size_blur):
    # Открываем изображение
    image_path = str(Path(image_path))
    original_image = cv2.imread(image_path)
    if not original_image:
        logger.error(f'Ошибка открытия файла: {image_path}')
        return False
    # Получите размеры изображения
    height, width, _ = original_image.shape

    # Создайте чистый холст для результата
    result_image = np.full_like(original_image, (255, 255, 255), dtype=np.uint8)

    # Вычислите координаты центра и радиус круга
    center_x = width // 2
    center_y = height // 2
    radius = min(center_x, center_y) - 5

    # Создайте маску круга
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, (255, 255, 255), -1)

    # Примените маску к исходному изображению
    result_image[mask > 0] = original_image[mask > 0]

    # Примените размытие к круговой области
    blurred_circle = cv2.GaussianBlur(result_image, (71, 71), 30)  # Измените параметры размытия по вашему усмотрению

    # Создайте круговую маску для result_image
    circle_mask = np.zeros((result_image.shape[0], result_image.shape[1]), dtype=np.uint8)
    cv2.circle(circle_mask,
               [result_image.shape[1] // 2, result_image.shape[0] // 2],
               radius,
               (255),
               -1)

    # Вычислите новые размеры увеличенного изображения
    new_height = int(result_image.shape[0] * data_blur[size_blur])
    new_width = int(result_image.shape[1] * data_blur[size_blur])

    # Увеличьте изображение с размытым кругом
    enlarged_result = cv2.resize(blurred_circle, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Вычислите смещение для вставки увеличенного изображения с размытым кругом
    offset_y = (enlarged_result.shape[0] - result_image.shape[0]) // 2
    offset_x = (enlarged_result.shape[1] - result_image.shape[1]) // 2

    # Вставьте увеличенное изображение с размытым кругом в общий результат
    enlarged_result[offset_y:offset_y + result_image.shape[0], offset_x:offset_x + result_image.shape[1]] = \
        np.where(circle_mask[:, :, None] > 0, result_image,
                 enlarged_result[offset_y:offset_y + result_image.shape[0], offset_x:offset_x + result_image.shape[1]])

    # Сохраните увеличенное изображение с размытым кругом

    cv2.imwrite(output_path, enlarged_result)

    logger.debug(f"Изображение сохранено в: {output_path}")
    return True


if __name__ == '__main__':
    image_path = r'C:\test\1.png'
    size_blur = '56'
    output_path = fr'C:\test\blur_1_{size_blur}.png'
    blur_image(image_path, output_path, size_blur)
