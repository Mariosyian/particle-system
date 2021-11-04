import pygame

from libraries import colors, globals


class Sprite(pygame.sprite.Sprite):
    """
    Represents a generic constructor for creating a new model/sprite.

    A sprite consists of:
        - An image or image
        - The image's rectangle (hitbox)
        - A color (R, G, B)
        - A width and height (in pixels)
        - An origin point of its top-left corner (in pixels)

    :param image: An image loaded using `pygame.image.load`, or `None` if drawing a
        simple, filled rectangle. This is effectively the sprites surface.
    :param width: The width of the surface (hitbox).
    :param height: The height of the surface (hitbox).
    :param x_coord: The x-coordinate of the images top-left corner.
    :param y_coord: The y-coordinate of the images top-left corner.
    :param color: The color of the surface. This setting does nothing if an image has
        been provided.
    """

    image = None
    rect = None
    color = None
    width = 0
    height = 0

    def __init__(
        self, image=None, width=0, height=0, x_coord=0, y_coord=0, color=colors.WHITE
    ):
        super().__init__()
        if not image:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_coord, y_coord)
        self.color = color if color else colors.WHITE
        self.width = width
        self.height = height


class Tennis_Ball(Sprite):
    """
    Represents a tennis ball sprite.

    A tennis ball has additional characteristics from the base sprite model:
        - Gravity
        - Collision capabilities with other particles (excluding background)

    :param image: An image loaded using `pygame.image.load`, or `None` if drawing a
        simple, filled rectangle. This is effectively the sprites surface.
    :param width: The width of the surface (hitbox).
    :param height: The height of the surface (hitbox).
    :param x_coord: The x-coordinate of the images top-left corner.
    :param y_coord: The y-coordinate of the images top-left corner.
    """

    def __init__(self, image=None, width=0, height=0, x_coord=0, y_coord=0):
        super().__init__(image, width, height, x_coord, y_coord)


class Player(Sprite):
    """
    Represents a player sprite.

    A player has additional characteristics from the base sprite model:
        - Movement (up, down, left, right, jump)
        - Collision capabilities with other particles (excluding background)

    :param image: An image loaded using `pygame.image.load`, or `None` if drawing a
        simple, filled rectangle. This is effectively the sprites surface.
    :param width: The width of the surface (hitbox).
    :param height: The height of the surface (hitbox).
    :param x_coord: The x-coordinate of the images top-left corner.
    :param y_coord: The y-coordinate of the images top-left corner.
    """

    is_jumping = False
    is_dropping = False

    def __init__(self, image=None, width=0, height=0, x_coord=0, y_coord=0):
        super().__init__(image, width, height, x_coord, y_coord)

    def move_up(self, offset=5):
        """
        Translate the player by `offset` amount in the upwards direction.

        :param offset: The amount to translate the player by.
        """
        if self.rect.y > globals.MAX_UP:
            self.rect.top -= offset

    def move_down(self, offset=5):
        """
        Translate the player by `offset` amount in the downwards direction.

        :param offset: The amount to translate the player by.
        """
        if self.rect.y < (globals.MAX_DOWN - self.rect.height):
            self.rect.bottom += offset

    def move_right(self, offset=5):
        """
        Translate the player by `offset` amount in the right direction.

        :param offset: The amount to translate the player by.
        """
        if self.rect.x < (globals.MAX_RIGHT - self.rect.width):
            self.rect.right += offset

    def move_left(self, offset=5):
        """
        Translate the player by `offset` amount in the left direction.

        :param offset: The amount to translate the player by.
        """
        if self.rect.x > globals.MAX_LEFT:
            self.rect.left -= offset
