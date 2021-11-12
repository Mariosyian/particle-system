"""
Author: Marios Yiannakou

Helper library to keep all global variables such as screen size,
enumerated keys (e.g. UP, DOWN, LEFT, RIGHT) accessible.
"""
from math import atan2, cos, hypot, pi, sin

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SCREEN = (WINDOW_WIDTH, WINDOW_HEIGHT)
NUM_OF_BALLS = 27

LOW_FPS = 30
GOLDEN_FPS = 60
MAX_FPS = 120

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Screen limits in pixels
MAX_UP = 400
MAX_DOWN = 720
MAX_LEFT = 0
MAX_RIGHT = 1280

# Gravity
GRAVITY_ANGLE = pi  # Gravity angle in radians
GRAVITY_MAGN = 1.0  # Gravity magnitude
DRAG = 0.99         # Multiplier for drag. Drag applied = 1 - `DRAG`

def add_vectors(angle_1, magn_1, angle_2, magn_2):
    """
    Adds two vectors, each with the given angle and magnitude, and returns the
    resulting vector as an angle and magnitude tuple with a (float, float) format.

    :param angle_1: The angle of the first vector in radians.
    :param magn_1: The magnitude of the first vector.
    :param angle_2: The angle of the second vector in radians.
    :param magn_2: The magnitude of the second vector.
    :returns: A tuple in the format (float, float) that represents the angle and
        magnitude respectively, of the resulting vector.
    """
    x = sin(angle_1) * magn_1 + sin(angle_2) * magn_2
    y = cos(angle_1) * magn_1 + cos(angle_2) * magn_2
    magnitude = hypot(x, y)
    angle = 0.5 * pi - atan2(y, x)

    return (angle, magnitude)
