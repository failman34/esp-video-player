# ESP-Video-Player
---
An ESP32-based project for playing video animations on an SSD1306 OLED display.  
This project uses the [Adafruit SSD1306 library](https://github.com/adafruit/Adafruit_SSD1306) for rendering graphics.  

## Installation

### Step 1: Load the Sketch onto the ESP32
1. Open the `.ino` file in the Arduino IDE.  
2. Select the appropriate ESP32 board in **Tools > Board**.  
3. In **Tools > Partition Scheme**, select **Custom** to use the `partitions.csv` provided in the project.  
4. Upload the sketch to your ESP32.  

### Step 2: Prepare Video Files
The project includes two pre-converted compressed video files (bitmap arrays):  
- "Bad Apple"  
- "Kanaria - Brain"  

If you want to use another video:  
1. Extract video frames (e.g., using VLC Media Player).  
2. Use the provided `framestobin.py` script to convert the frames to a compressed bitmap array.  
   - The output will be a `.bin` file.  
3. Rename the generated `.bin` file to `bitmaps.bin`.  
4. Create a folder named `data` in the project directory and place the `bitmaps.bin` file inside.  

### Step 3: Create and Flash the SPIFFS Partition
You will need two tools:  
- **mkspiffs** (to create the SPIFFS partition)  
- **esptool** (to flash the partition to the ESP32)  

Run the following commands:

1. Create the SPIFFS partition:  
   ```sh
   mkspiffs -c data -p 256 -b 4096 -s 0x38fff4 data.bin
   ```  

2. Flash the partition to your ESP32:  
   ```sh
   esptool -b 921600 write_flash 0x70000 data.bin
   ```  

---

The readme was created through a translator using chat gpt, so there may be inaccuracies . If there are any problems there is always the Issues tab