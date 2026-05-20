from machine import Pin, I2C, ADC
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

buttons = [
    Pin(BUTTON1_PIN, Pin.IN, Pin.PULL_UP),
    Pin(BUTTON2_PIN, Pin.IN, Pin.PULL_UP),
    Pin(BUTTON3_PIN, Pin.IN, Pin.PULL_UP),
    Pin(BUTTON4_PIN, Pin.IN, Pin.PULL_UP),
]

last_states = [1, 1, 1, 1]

# --------------------
# LED Setup
# --------------------

led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)
led3 = Pin(LED3_PIN, Pin.OUT)
led4 = Pin(LED4_PIN, Pin.OUT)

# --------------------
# Battery Setup
# --------------------

battery_adc = ADC(BATTERY_PIN)

LOW_BATTERY_THRESHOLD = 30

# --------------------
# Pages
# --------------------

page = 0

# --------------------
# Battery Functions
# --------------------

def get_battery_voltage():
    """
    Read battery voltage.
    Assumes 100k/100k voltage divider.
    """

    raw = battery_adc.read_u16()

    # Convert ADC reading to voltage
    voltage = (raw / 65535) * 3.3

    # Undo divider (x2)
    battery_voltage = voltage * 2

    return battery_voltage


def get_battery_percent():
    """
    Approximate percentage for 3x AAA alkaline batteries.

    4.5V = full
    3.3V = empty
    """

    voltage = get_battery_voltage()

    percent = int(((voltage - 3.3) / (4.5 - 3.3)) * 100)

    # Clamp range
    percent = max(0, min(100, percent))

    return percent

# --------------------
# Display Functions
# --------------------

def draw_page():
    oled.fill(0)

    battery = get_battery_percent()

    if page == 0:
        oled.text("Zach", 0, 0)
        oled.text("Indie Dev", 0, 12)
        oled.text("RP2040 Badge", 0, 24)

    elif page == 1:
        oled.text("Primordia", 0, 0)
        oled.text("Systems", 0, 12)
        oled.text("STATUS: OK", 0, 24)

    elif page == 2:
        oled.text("Battery", 0, 0)
        oled.text(str(battery) + "%", 0, 12)

        voltage = round(get_battery_voltage(), 2)
        oled.text(str(voltage) + "V", 0, 24)

    oled.show()

# --------------------
# Button Actions
# --------------------

def handle_button_press(index):
    global page

    # Button 1
    if index == 0:
        page = (page + 1) % 3
        draw_page()

    # Button 2
    elif index == 1:
        led1.toggle()

    # Button 3
    elif index == 2:
        led3.toggle()

    # Button 4
    elif index == 3:
        led4.toggle()

# --------------------
# Initial Draw
# --------------------

draw_page()

# --------------------
# Main Loop
# --------------------

while True:

    # Check Buttons
    for i in range(4):

        current = buttons[i].value()

        # Detect press
        if last_states[i] == 1 and current == 0:
            handle_button_press(i)

        last_states[i] = current

    # Battery Warning LED
    battery_percent = get_battery_percent()

    if battery_percent < LOW_BATTERY_THRESHOLD:
        led2.on()
    else:
        led2.off()

    time.sleep(0.05)