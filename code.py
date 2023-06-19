import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode


MACRO_FOLDER = '/macros'


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
position = 0
last_position = 0

app_index = 0
apps[app_index].switch()

# MAIN LOOP ----------------------------

while True:
    # Handle encoder changes
    position = macropad.encoder
    if position != last_position:
        if position < last_position:
            macropad.consumer_control.press(ConsumerControlCode.VOLUME_DECREMENT)
        else:
            macropad.consumer_control.press(ConsumerControlCode.VOLUME_INCREMENT)
        macropad.consumer_control.release()
        last_position = position

    # Handle encoder press changes
    macropad.encoder_switch_debounced.update()
    if encoder_switch_debounced_event == 'pressed':
        if (time.time() - encoder_switch_debounced_millis) > 1:
            encoder_switch_press_released = 1
            apps[app_index].turnOffLeds()

    if macropad.encoder_switch_debounced.pressed:
        encoder_switch_debounced_event = 'pressed'
        encoder_switch_debounced_millis = time.time()
    if macropad.encoder_switch_debounced.released:
        encoder_switch_debounced_event = 'released'
        if encoder_switch_press_released == 1:
            encoder_switch_press_released = 0
            app_index = 0
        else:
            app_index += 1
        app_index = app_index % len(apps)
        apps[app_index].switch()
