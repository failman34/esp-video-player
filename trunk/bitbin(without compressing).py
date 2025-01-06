import os
from PIL import Image

def process_images_to_bin(folder_path, output_file):
    WIDTH = 128
    HEIGHT = 64

    # Размер одного битмапа (в байтах)
    bitmap_size = WIDTH * HEIGHT // 8

    # Открываем бинарный файл для записи
    with open(output_file, "wb") as bin_file:

        # Сканируем папку
        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                file_path = os.path.join(folder_path, filename)
                print(f"Обрабатываем: {filename}")

                # Открываем и обрабатываем изображение
                with Image.open(file_path) as img:
                    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                    grayscale = img.convert("L")

                    # Определяем среднюю яркость
                    pixels = list(grayscale.getdata())
                    avg_brightness = sum(pixels) // len(pixels)

                    # Преобразуем в монохромное изображение
                    binary_img = grayscale.point(lambda x: 255 if x > avg_brightness else 0, mode="1")

                    # Формируем байты битмапа
                    bitmap_data = bytearray()
                    for y in range(HEIGHT):
                        byte = 0
                        for x in range(WIDTH):
                            pixel = binary_img.getpixel((x, y))
                            bit = 0 if pixel == 0 else 1
                            byte = (byte << 1) | bit
                            if (x + 1) % 8 == 0 or x == WIDTH - 1:
                                bitmap_data.append(byte)
                                byte = 0

                    # Проверяем размер битмапа
                    if len(bitmap_data) != bitmap_size:
                        raise ValueError(f"Ошибка: Размер битмапа {filename} не соответствует {bitmap_size} байтам")

                    # Записываем битмап в общий бинарный файл
                    bin_file.write(bitmap_data)

    print(f"Готово! Все битмапы объединены в {output_file}")

# Укажите путь к папке с изображениями и имя выходного файла
folder_path = "frames"  # Папка с изображениями
output_file = "all_bitmaps.bin"  # Выходной бинарный файл

process_images_to_bin(folder_path, output_file)
