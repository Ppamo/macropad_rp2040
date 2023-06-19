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

from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {
    'name' : 'Win',
    'color': 0x400000,
    'macros' : [
        # 1st row ----------
        (-1, '', []),
        (0x202000, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (-1, 'Bright+', [[ConsumerControlCode.BRIGHTNESS_INCREMENT]]),
        # 2nd row ----------
        (-1, '', []),
        (0x202000, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (-1, 'Bright-', [[ConsumerControlCode.BRIGHTNESS_DECREMENT]]),
        # 3rd row ----------
        (-1, '', []),
        (-1, 'Mute', [[ConsumerControlCode.MUTE]]),
        (-1, '', []),
        # 4th row ----------
        (-1, '<<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (-1, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (-1, '>>', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
    ],
    'encoder': [
        ([[ConsumerControlCode.VOLUME_INCREMENT]]),
        ([[ConsumerControlCode.VOLUME_DECREMENT]]),
    ]
}
