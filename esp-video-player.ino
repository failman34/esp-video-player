#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SPIFFS.h>

#define BUFFER_SIZE 1024  // Размер буфера
#define WIDTH 128
#define HEIGHT 64

byte buffer[BUFFER_SIZE];  // Буфер для хранения декодированных данных
int buffer_index = 0;      // Индекс для текущей позиции в буфере
unsigned long frameDelay = 1000 / 24; // 24 FPS
unsigned long startTime;
unsigned long frameTime;

Adafruit_SSD1306 display(WIDTH, HEIGHT, &Wire);

// Ваша функция для обработки данных
void process_buffer() {
    
    display.clearDisplay();
    display.drawBitmap(0, 0, buffer, WIDTH, HEIGHT, WHITE);
    display.display();


    buffer_index = 0;
}

// Функция декодирования RLE
void rle_decode(File &infile) {
    byte count = 0;
    byte byte_val = 0;

    while (infile.available()) {
        
        // Читаем два байта
        count = infile.read();         // Первый байт - количество
        byte_val = infile.read();      // Второй байт - значение

        // Записываем данные в буфер
        for (int i = 0; i < count; i++) {
            if (buffer_index < BUFFER_SIZE) {
                buffer[buffer_index++] = byte_val;
            }
        }

        if (buffer_index >= BUFFER_SIZE) {
        	process_buffer();
          	frameTime = millis() - startTime;
          	if (frameTime < frameDelay) {
            	delay(frameDelay - frameTime);
            	Serial.println(frameDelay - frameTime);
          	}
          	startTime = millis();
        }
    }
}

void setup() {
    Serial.begin(115200);
    Wire.begin(25, 26, 100000);

    if (!SPIFFS.begin()) {
    	Serial.println("Ошибка монтирования SPIFFS!");
    	while (true);
    }

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    	Serial.println(F("SSD1306 allocation failed"));
    	while (true);
    }

    // Открываем входной файл для чтения
    File infile = SPIFFS.open("/bitmaps.bin", "r");
    if (!infile) {
        Serial.println("Не удалось открыть файл для чтения");
        return;
    }

    display.clearDisplay();
    display.display();
    delay(1000);

    // Декодируем данные
    rle_decode(infile);

    // Закрываем файл
    infile.close();

    Serial.println("Декодирование завершено.");
}

void loop() {
    // Ничего не делаем в цикле
}