# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Consumer Control codes (media keys)

# The syntax for Consumer Control macros is a little peculiar, in order to
# maintain backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes are distinguished by enclosing them in a list within
# the list, which is why you'll see double brackets [[ ]] below.
# Like Keycodes, Consumer Control codes can be positive (press) or negative
# (release), and float values can be inserted for pauses.

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {
    'name' : 'Win',
    'color': 0x040404,
    'macros' : [
        # --
        (0x080008, '>||', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x080008, '<<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x080008, '>>', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # --
        (0x080600, '^C', [Keycode.CONTROL, Keycode.C]),
        (0x080600, '^V', [Keycode.CONTROL, Keycode.V]),
        (0x080008, 'Mute', [[ConsumerControlCode.MUTE]]),
        # --
        (0x000408, '//\\\\', [Keycode.PAGE_UP]),
        (0x000008, '/\\', [Keycode.UP_ARROW]),
        (0x000408, '\\\\//', [Keycode.PAGE_DOWN]),
        # --
        (0x000008, '<', [Keycode.LEFT_ARROW]),
        (0x000008, '\\/', [Keycode.DOWN_ARROW]),
        (0x000008, '>', [Keycode.RIGHT_ARROW]),
    ],
    'encoder': [
        ConsumerControlCode.VOLUME_DECREMENT,
        ConsumerControlCode.VOLUME_INCREMENT,
    ]
}
