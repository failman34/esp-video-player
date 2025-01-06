import os
from PIL import Image

def process_images_in_folder(folder_path, output_file):
    WIDTH = 128
    HEIGHT = 64

    # Начало заголовочного файла
    header = """
#include <stdint.h>

"""
    # Для хранения всех битмапов
    bitmaps = []

    # Сканируем папку
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            file_path = os.path.join(folder_path, filename)
            bitmap_name = os.path.splitext(filename)[0].replace(" ", "_")
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
                
                # Сохраняем битмап
                bitmap_data = []
                for y in range(HEIGHT):
                    byte = 0
                    for x in range(WIDTH):
                        pixel = binary_img.getpixel((x, y))
                        bit = 0 if pixel == 0 else 1
                        byte = (byte << 1) | bit
                        if (x + 1) % 8 == 0 or x == WIDTH - 1:
                            bitmap_data.append(f"0x{byte:02X}")
                            byte = 0
                
                # Добавляем битмап в общий массив
                bitmaps.append({
                    "name": bitmap_name,
                    "data": bitmap_data
                })
    
    # Формируем содержимое файла
    with open(output_file, "w") as f:
        f.write(header)

        # Записываем каждый битмап
        for bitmap in bitmaps:
            f.write(f"const uint8_t {bitmap['name']}[] = {{\n")
            f.write(", ".join(f"  {line}" for line in bitmap['data']))
            f.write("\n};\n\n")
        
        # Записываем массив указателей на битмапы и их количество
        f.write("const uint8_t* all_bitmaps[] = {\n")
        for bitmap in bitmaps:
            f.write(f"  {bitmap['name']},\n")
        f.write("};\n\n")
        f.write(f"const size_t all_bitmaps_count = {len(bitmaps)};\n")

    print(f"Готово! Битмапы сохранены в {output_file}")

# Укажите путь к папке с изображениями и имя выходного файла
folder_path = "vlc"  # Папка с изображениями
output_file = "all_bitmaps.h"  # Выходной файл

process_images_in_folder(folder_path, output_file)
