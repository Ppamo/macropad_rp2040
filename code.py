import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode


MACRO_FOLDER = '/macros'
def pressed_button(app, event):
    button = event.pressed
    key_number = event.key_number
    sequence = app.macros[key_number][2]
    # 'sequence' is an arbitrary-length list, each item is one of:
    # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
    # Negative integer: (absolute value) key released
    # Float (e.g. 0.25): delay in seconds
    # String (e.g. "Foo"): corresponding keys pressed & released
    # List []: one or more Consumer Control codes (can also do float delay)
    # Dict {}: mouse buttons/motion (might extend in future)
    if key_number < 12: # No pixel for encoder button
        macropad.pixels[key_number] = 0x6F6F6F
        macropad.pixels.show()
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.press(item)
            else:
                macropad.keyboard.release(-item)
        elif isinstance(item, float):
            time.sleep(item)
        elif isinstance(item, str):
            macropad.keyboard_layout.write(item)
        elif isinstance(item, list):
            for code in item:
                if isinstance(code, int):
                    macropad.consumer_control.release()
                    macropad.consumer_control.press(code)
                if isinstance(code, float):
                    time.sleep(code)
        elif isinstance(item, dict):
            if 'buttons' in item:
                if item['buttons'] >= 0:
                    macropad.mouse.press(item['buttons'])
                else:
                    macropad.mouse.release(-item['buttons'])
            macropad.mouse.move(item['x'] if 'x' in item else 0,
                                item['y'] if 'y' in item else 0,
                                item['wheel'] if 'wheel' in item else 0)
            if 'tone' in item:
                if item['tone'] > 0:
                    macropad.stop_tone()
                    macropad.start_tone(item['tone'])
                else:
                    macropad.stop_tone()
            elif 'play' in item:
                macropad.play_file(item['play'])

def released_button(app, event):
    key_number = event.key_number
    sequence = app.macros[key_number][2]
    # Release any still-pressed keys, consumer codes, mouse buttons
    # Keys and mouse buttons are individually released this way (rather
    # than release_all()) because pad supports multi-key rollover, e.g.
    # could have a meta key or right-mouse held down by one macro and
    # press/release keys/buttons with others. Navigate popups, etc.
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.release(item)
        elif isinstance(item, dict):
            if 'buttons' in item:
                if item['buttons'] >= 0:
                    macropad.mouse.release(item['buttons'])
            elif 'tone' in item:
                macropad.stop_tone()
    macropad.consumer_control.release()
    if apps[app_index].macros[key_number][0] == -1:
        macropad.pixels[key_number] = apps[app_index].color
    else:
        macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
    macropad.pixels.show()


class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.color = appdata['color']
        self.macros = appdata['macros']
        self.encoder = appdata['encoder']

    def turnOffLeds(self):
        """ Turn off all the leds in the macropad """
        for i in range(12):
            macropad.pixels[i] = 0
        macropad.pixels.show()

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[13].text = self.name
        for i in range(12):
            if i < len(self.macros):
                if self.macros[i][0] ==  -1:
                    macropad.pixels[i] = self.color
                else:
                    macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()


macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            print("Loading", filename)
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_encoder_switch_debounced_event = None
encoder_switch_debounced_event = None
encoder_switch_press_released = 0
encoder_switch_debounced_millis = 0
last_button_pressed = None
position = 0
last_position = 0

app_index = 0
apps[app_index].switch()

# MAIN LOOP ----------------------------

while True:
    # Handle encoder changes
    position = macropad.encoder
    if position != last_position:
        print('Encoder changed')
        if position < last_position:
            macropad.consumer_control.press(apps[app_index].encoder[0])
        else:
            macropad.consumer_control.press(apps[app_index].encoder[1])
        macropad.consumer_control.release()
        last_position = position
        continue

    # Handle encoder press changes
    macropad.encoder_switch_debounced.update()
    if encoder_switch_debounced_event == 'pressed':
        print('Encoder button pressed')
        if (time.time() - encoder_switch_debounced_millis) > 1:
            print('Encoder long button pressed')
            encoder_switch_press_released = 1
            apps[app_index].turnOffLeds()

    if macropad.encoder_switch_debounced.pressed:
        print('Encoder switch pressed')
        encoder_switch_debounced_event = 'pressed'
        encoder_switch_debounced_millis = time.time()
    if macropad.encoder_switch_debounced.released:
        print('Encoder switch released')
        encoder_switch_debounced_event = 'released'
        if encoder_switch_press_released == 1:
            encoder_switch_press_released = 0
            app_index = 0
        else:
            app_index += 1
        app_index = app_index % len(apps)
        apps[app_index].switch()

    # Handle buttons
    event = macropad.keys.events.get()
    if event:
        key_number = event.key_number
        print('>> Key number: ', key_number, '/', str(len(apps[app_index].macros)))
        if key_number >= len(apps[app_index].macros):
            continue

        pressed = event.pressed
        if pressed:
            print('pressed')
            last_button_pressed = pressed
            pressed_button(apps[app_index], event)

        # if last_button_pressed:
        if event.released:
            print ('> release')
            last_button_pressed = None
            released_button(apps[app_index], event)
