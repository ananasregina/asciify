import colorsys
import fcntl
import os
import struct
import termios

import cv2
import numpy as np

DEFAULT_CHARSET = [" ", ".", "-", "=", "+", "*", "x", "#", "$", "&", "X", "@"]


def hsv_to_ansi(h, s, v):
    """Convert HSV (OpenCV: h: 0-360, s: 0-100, v: 0-100) to ANSI escape code"""
    # s = min(255, int(s * 1.5))
    # v = min(255, int(v * 1.5))

    r, g, b = colorsys.hsv_to_rgb(h / 179, s / 255, v / 255)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def get_font_aspect_ratio():
    """Get terminal font aspect ratio dynamically.

    Returns the height/width ratio of terminal characters by querying the terminal for both character dimensions and pixel dimensions.

    :return: Font aspect ratio (typically 1.8-2.2)
    :rtype: float
    """
    try:
        char_size = os.get_terminal_size()
        rows, cols = char_size.lines, char_size.columns

        with open('/dev/tty', 'rb') as tty:
            # TIOCGWINSZ ioctl: returns (rows, cols, xpixel, ypixel)
            result = fcntl.ioctl(tty, termios.TIOCGWINSZ, b'\x00' * 8)
            _, _, width_px, height_px = struct.unpack('HHHH', result)

        if height_px > 0 and width_px > 0 and rows > 0 and cols > 0:
            char_height = height_px / rows
            char_width = width_px / cols

            aspect_ratio = char_height / char_width
            return aspect_ratio

    except (OSError, IOError, ZeroDivisionError):
        return 2.0

def create_test():
    img = np.zeros((500, 500, 3), dtype=np.uint8)

    img[50:450, 50:450] = [255, 255, 255]
    img[100:400, 100:400] = [0, 0, 0]

    cv2.circle(img, (250, 250), 150, (255, 0, 0), 5)

    cv2.line(img, (0, 250), (500, 250), (0, 255, 0), 2)
    cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 2)

    cv2.imwrite("test_square.png", img)
    print("Created test_square.png")

