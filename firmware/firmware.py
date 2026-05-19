from machine import Pin, I2C
import ssd1306
import time

# --------------------
# Pin Configuration
# --------------------

SDA_PIN = 0
SCL_PIN = 1

BUTTON1_PIN = 2
BUTTON2_PIN = 3
BUTTON3_PIN = 4
BUTTON4_PIN = 5

BUZZER_PIN = 6

LED1_PIN = 7
LED2_PIN = 8
LED3_PIN = 9
LED4_PIN = 25

BATTERY_PIN = 26
# --------------------
# OLED Setup
# --------------------

i2c = I2C(
    0,
    scl=Pin(SCL_PIN),
    sda=Pin(SDA_PIN),
    freq=400000
)

oled = ssd1306.SSD1306_I2C(
    128,
    32,
    i2c
)

# --------------------
# Button Setup
# --------------------

button = Pin(
    BUTTON1_PIN,
    Pin.IN,
    Pin.PULL_UP
)

# --------------------
# Pages
# --------------------

page = 0

def draw_page():
    oled.fill(0)

    if page == 0:
        oled.text("Zach", 0, 0)
        oled.text("Indie Dev", 0, 12)
        oled.text("RP2040 Badge", 0, 24)

    elif page == 1:
        oled.text("Primordia", 0, 0)
        oled.text("Systems", 0, 12)
        oled.text("STATUS: OK", 0, 24)

    oled.show()

# Initial Draw
draw_page()

# --------------------
# Main Loop
# --------------------

last_button = 1

while True:

    current = button.value()

    # Button Press Detection
    if last_button == 1 and current == 0:
        page = (page + 1) % 2
        draw_page()

    last_button = current

    time.sleep(0.05)