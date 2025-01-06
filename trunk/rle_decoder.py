def rle_decode(encoded_data):
    decoded_data = bytearray()
    count = 0
    for i in range(0, len(encoded_data), 2):
        count = encoded_data[i]
        byte = encoded_data[i + 1]
        decoded_data.extend([byte] * count)
    return decoded_data

# Открываем файл all.bin для чтения закодированных данных
with open('all_bitmaps_rle.bin', 'rb') as infile:
    encoded_data = infile.read()

# Декодируем данные
decoded_data = rle_decode(encoded_data)

# Сохраняем декодированные данные в новый файл
with open('decoded_all.bin', 'wb') as outfile:
    outfile.write(decoded_data)

print("Декодирование завершено и сохранено в файл 'decoded_all.bin'.")
