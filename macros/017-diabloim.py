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
    'name' : 'Diablo Immortal',
    'color': 0x040404,
    'macros' : [
        # --
        (0x040000, ' :: ', [Keycode.FOUR]),
        (0x080408, '  X ', [Keycode.ESCAPE]),
        (0x000600, ' >> ', [Keycode.LEFT_SHIFT]),
        # --
        (0x040000, ' .: ', [Keycode.THREE]),
        (0x000008, ' -- ', ['I']),
        (0x000600, '  ] ', ['R']),
        # --
        (0x040000, '  : ', [Keycode.TWO]),
        (0x000008, ' <> ', ['M']),
        (0x000600, ' << ', ['E']),
        # --
        (0x040000, '  . ', [Keycode.ONE]),
        (0x090700, '  + ', [Keycode.SPACEBAR]),
        (0x080008, ' ++ ', ['Q']),
    ],
    'encoder': [
        ConsumerControlCode.VOLUME_DECREMENT,
        ConsumerControlCode.VOLUME_INCREMENT,
    ]
}
