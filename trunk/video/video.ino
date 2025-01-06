#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "bitmaps.h" // Подключаем сгенерированный заголовочный файл

#define SCREEN_WIDTH 128 // Ширина дисплея SSD1306
#define SCREEN_HEIGHT 64 // Высота дисплея SSD1306
#define OLED_RESET -1    // Сброс (не используется для I2C)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);


const unsigned long targetFPS = 24; // Желаемая частота кадров (24 FPS)
unsigned long frameDelay = 1000 / targetFPS; // Время на один кадр в миллисекундах
unsigned long lastFrameTime = 0; // Время последнего кадра
unsigned long frameTime;
unsigned long startTime;


void setup() {
  Serial.begin(921600);
  Wire.begin(25, 26, 100000);
    // Инициализация дисплея
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Адрес дисплея I2C
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ;
    }
    display.clearDisplay();
    display.display();

    // Задержка для старта
    delay(1000);
}

void loop() {
for (size_t i = 0; i < all_bitmaps_count; i++) {
        startTime = millis(); // Засекаем время начала кадра

        display.clearDisplay(); // Очищаем дисплей

        // Вывод битмапа
        display.drawBitmap(0, 0, all_bitmaps[i], SCREEN_WIDTH, SCREEN_HEIGHT, WHITE);
        display.display(); // Отображаем изменения

        // // Отображение времени обработки кадра (опционально)
        // Serial.print(F("Кадр "));
        // Serial.print(i + 1);
        // Serial.print(F(" из "));
        // Serial.print(all_bitmaps_count);
        // Serial.print(F(". Время обработки: "));
        // Serial.print(frameTime);
        // Serial.print(F(" мс. Задержка: "));
        // Serial.println(frameDelay - frameTime);

        // Засекаем время завершения кадра
        frameTime = millis() - startTime;

        // Синхронизация частоты кадров
        delay(frameDelay - frameTime); // Ждем остаток времени до следующего кадра

        
        
    }
}