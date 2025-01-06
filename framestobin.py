import os
from PIL import Image

def compress_rle(data):
    """Сжимает данные методом RLE."""
    compressed = []
    prev_byte = data[0]
    count = 1

    for byte in data[1:]:
        if byte == prev_byte and count < 255:
            count += 1
        else:
            compressed.append(count)
            compressed.append(prev_byte)
            prev_byte = byte
            count = 1

    # Добавляем оставшиеся данные
    compressed.append(count)
    compressed.append(prev_byte)

    return compressed

def process_images_with_rle(folder_path, output_file):
    WIDTH = 128
    HEIGHT = 64

    all_bitmaps = []

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
                
                # Сохраняем битмап
                bitmap_data = []
                for y in range(HEIGHT):
                    byte = 0
                    for x in range(WIDTH):
                        pixel = binary_img.getpixel((x, y))
                        bit = 0 if pixel == 0 else 1
                        byte = (byte << 1) | bit
                        if (x + 1) % 8 == 0 or x == WIDTH - 1:
                            bitmap_data.append(byte)
                            byte = 0
                
                # Сжимаем данные методом RLE
                compressed_data = compress_rle(bitmap_data)
                all_bitmaps.append(compressed_data)

    # Записываем сжатые битмапы в бинарный файл
    with open(output_file, "wb") as f:
        for bitmap in all_bitmaps:
            # Сохраняем длину битмапа перед сжатыми данными
            f.write(bytearray(bitmap))

    print(f"Готово! Сжатые битмапы сохранены в {output_file}")

# Укажите путь к папке с изображениями и имя выходного файла
folder_path = input("folder_path: ")  # Папка с изображениями
output_file = "all_bitmaps_rle.bin"  # Выходной файл

process_images_with_rle(folder_path, output_file)
