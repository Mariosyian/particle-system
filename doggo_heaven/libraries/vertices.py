"""
Author: Marios Yiannakou

Helper library to keep track of any vertice objects.
This file assumes a screen size of 1280 x 720.
"""
from . import colors

"""
Vertice format:
vertice = [
    (X, Y), # Coordinates of origin point in pixels
    (width, height), # Size of vertice in pixels
    <color>,
]
"""
cloud_1 = [
    (300, 100),
    (175, 100),
    None,
]
cloud_2 = [
    (700, 250),
    (300, 100),
    None,
]
cloud_2_1 = [
    (750, 200),
    (200, 50),
    None,
]
mountain_1 = [
    (0, 350),
    (150, 170),
    colors.BROWN,
]
mountain_1_1 = [
    (150, 420),
    (250, 100),
    colors.DARK_BROWN,
]
ground = [
    (0, 520),
    (1280, 200),
    colors.GREEN,
]


def get_origin_x(vertice) -> int:
    """
    Get the vertice's origin point x-coordinate.

    :param vertice: The vertice whose origin point x-coordinate to return.
    :returns: The x-coordinate of the vertice's origin point in pixels.
    """
    return vertice[0][0]


def get_origin_y(vertice) -> int:
    """
    Get the vertice's origin point y-coordinate.

    :param vertice: The vertice whose origin point y-coordinate to return.
    :returns: The y-coordinate of the vertice's origin point in pixels.
    """
    return vertice[0][1]


def get_width(vertice) -> int:
    """
    Get the vertice's width in pixels.

    :param vertice: The vertice whose width to return.
    :returns: The vertice's width measured in pixels.
    """
    return vertice[1][0]


def get_height(vertice) -> int:
    """
    Get the vertice's height in pixels.

    :param vertice: The vertice whose height to return.
    :returns: The vertice's height measured in pixels.
    """
    return vertice[1][1]


def get_color(vertice):
    """
    Get the color part of the vertice.

    :param vertice: The vertice whose color to return.
    :returns: The color of the vertice if set, `colors.WHITE` otherwise.
    """
    return vertice[2] if vertice[2] else colors.WHITE
