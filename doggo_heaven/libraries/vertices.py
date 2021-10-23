from . import colors

cloud_1 = [
    [-0.7, 0.6, 0.0],
    [-0.4, 0.6, 0.0],
    [-0.4, 0.2, 0.0],
    [-0.7, 0.2, 0.0],
    None,
]
cloud_2 = [
    [0.3, 0.4, 0.0],
    [0.7, 0.4, 0.0],
    [0.7, 0.1, 0.0],
    [0.3, 0.1, 0.0],
    None,
]
cloud_2_1 = [
    [0.4, 0.5, 0.0],
    [0.6, 0.5, 0.0],
    [0.6, 0.4, 0.0],
    [0.4, 0.4, 0.0],
    None,
]
mountain_1 = [
    [-1.0, 0.1, 0.0],
    [-0.8, 0.1, 0.0],
    [-0.8, -0.5, 0.0],
    [-1.0, -0.5, 0.0],
    colors.BROWN,
]
mountain_1_1 = [
    [-0.9, 0.0, 0.0],
    [-0.7, 0.0, 0.0],
    [-0.7, -0.5, 0.0],
    [-0.9, -0.5, 0.0],
    colors.DARK_BROWN,
]
ground = [
    [-1.0, -0.5, 0.0],
    [1.0, -0.5, 0.0],
    [1.0, -1.0, 0.0],
    [-1.0, -1.0, 0.0],
    colors.GREEN,
]
dog = [
    [0.7, -0.4, 1.0],
    [0.9, -0.4, 1.0],
    [0.9, -0.6, 1.0],
    [0.7, -0.6, 1.0],
    colors.BROWN,
]

def get_color(vertice):
    """
    Get the color part of the vertice.

    :param vertice: The vertice whose color to return.
    :returns: The color part of the vertice, `colors.WHITE` if `None`
    """
    return vertice[4] if vertice[4] else colors.WHITE