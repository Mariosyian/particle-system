"""
Author: Marios Yiannakou

Overrides the `pygame` modules `Sprite` class, to customise functionality for the
'Doggo Heaven' game. Also adds the `Tennis_Ball` and `Player` sprites.
"""
import pygame

from libraries import colors
from libraries.globals import *
from math import cos, sin
from time import time_ns


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
    :param angle: The initial angle (in radians) of the surface. 0 being up,
        math.pi down.
    :param speed: The initial speed (index as a float) of the surface. Accepts
        values between 0 and 1.
    :param color: The color of the surface. This setting does nothing if an image has
        been provided.
    """

    image = None
    rect = None
    color = None
    width = 0
    height = 0

    angle = None
    speed = None

    # Hitbox format: top_left_x, top_left_y, width, height
    hitbox = None

    def __init__(
        self,
        image=None,
        width=0,
        height=0,
        x_coord=0,
        y_coord=0,
        angle=0,
        speed=0,
        color=colors.WHITE,
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
        self.angle = angle
        self.speed = speed

        self.hitbox = [x_coord - 5, y_coord - 5, width + 5, height + 5]

    def apply_gravity(self, gravity):
        """
        Applies a gravity vector to the object. Need to pass the gravity magnitude as
        this file does not read the updated value.
        CREDITS: https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/gravity/

        :param gravity: The magnitude of the gravity vector.
        :returns: The updated rectangle of the sprite after gravity has been applied.
        """
        (self.angle, self.speed) = add_vectors(
            self.angle, self.speed, GRAVITY_ANGLE, gravity
        )
        self.rect.x += sin(self.angle) * self.speed
        self.rect.y -= cos(self.angle) * self.speed
        self.speed *= DRAG

        return self.rect


class Tennis_Ball(Sprite):
    """
    Represents a tennis ball sprite.

    A tennis ball has additional characteristics from the base sprite model:
        - Gravity properties
            - Elasticity
        - Collision capabilities with other particles (excluding background)
        - Lifetime

    :param image: An image loaded using `pygame.image.load`, or `None` if drawing a
        simple, filled rectangle. This is effectively the sprites surface.
    :param width: The width of the surface (hitbox).
    :param height: The height of the surface (hitbox).
    :param x_coord: The x-coordinate of the images top-left corner.
    :param y_coord: The y-coordinate of the images top-left corner.
    :param angle: The initial angle (in radians) of the tennis ball. 0 being up,
        math.pi down.
    :param speed: The initial speed (index as a float) of the tennis ball. Accepts
        values between 0 and 1.
    :param elasticity: The elasticity (index as a float) of the tennis ball. This is a
        multiplier index that is applied to the ball's speed each time it reaches a
        boundary position.
    :param opacity: The opacity (alpha value) of the image. This is an integer in the
        range 0 - 255 (inclusive), where 0 is fully transparent and 255 is fully
        opaque.
    :param lifetime: The amount of time (in seconds) the ball remains in the game.
        An integer greater than zero. If zero, the ball does not disappear
        (i.e. infinite liftime).
    """

    elasticity = None
    born = None
    lifetime = 0

    def __init__(
        self,
        image=None,
        width=0,
        height=0,
        x_coord=0,
        y_coord=0,
        angle=0,
        speed=GRAVITY_MAGN,
        elasticity=0.8,
        lifetime=0,
    ):
        super().__init__(image, width, height, x_coord, y_coord, angle, speed)
        self.elasticity = float(elasticity)
        self.lifetime = lifetime
        self.born = time_ns()

    def bounce(self):
        """
        Handle the bouncing logic in case a tennis ball collides with any screen edges.

        :returns: The updated rectangle of the tennis ball.
        """
        if self.rect.x >= WINDOW_WIDTH:
            self.rect.x = 2 * WINDOW_WIDTH - self.rect.x
            self.angle = -self.angle
            self.speed *= self.elasticity
        elif self.rect.x <= 0:
            self.rect.x -= 2 * self.rect.x
            self.angle = -self.angle
            self.speed *= self.elasticity

        if self.rect.y >= (WINDOW_HEIGHT - self.height):
            self.rect.y = 2 * WINDOW_HEIGHT - (self.rect.y + self.height)
            self.angle = pi - self.angle
            self.speed *= self.elasticity
        elif self.rect.y <= 0:
            self.rect.y -= 2 * self.rect.y
            self.angle = pi - self.angle
            self.speed *= self.elasticity

        return self.rect

    def alive(self):
        """
        Calculates if a tennis ball sprite should be rendered or not.

        :returns: True if `lifetime` is set to 0, or if `lifetime` is less than the
            difference between the creation of the sprite and the current time in ns.
            False otherwise.
        """
        if self.lifetime == 0:
            return True

        while time_ns() - self.born < (self.lifetime * 1000 * 1000 * 1000):
            return True
        return False

    def set_lifetime(self, lifetime):
        """
        Update the lifetime of the tennis ball, and sets the "born" time, to the time
        the lifetime was updated.

        :param lifetime: The new lifetime of the tennis ball in seconds.
        """
        self.lifetime = lifetime
        self.born = time_ns()

    def set_elasticity(self, elasticity):
        """
        Update the elasticity of the tennis ball.

        :param elasticity: The new elasticity of the tennis ball.
        """
        self.elasticity = elasticity


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
    :param angle: The initial angle (in radians) of the player. 0 being up,
        math.pi down.
    :param speed: The initial speed (index as a float) of the player. Accepts
        values between 0 and 1.
    :param direction: The initial direction the sprite is facing towards.
    """

    is_jumping = False
    is_dropping = False
    direction = None

    def __init__(
        self,
        image=None,
        width=0,
        height=0,
        x_coord=0,
        y_coord=0,
        angle=-(pi / 2),
        speed=0,
        direction=LEFT,
    ):
        super().__init__(image, width, height, x_coord, y_coord, angle, speed)
        self.direction = direction

    def move_up(self, offset=5):
        """
        Translate the player by `offset` amount in the upwards direction.

        :param offset: The amount to translate the player by.
        """
        self.angle = 0
        self.speed = offset
        if self.rect.y > MAX_UP:
            self.rect.top -= offset
            self.hitbox[1] -= offset

    def move_down(self, offset=5):
        """
        Translate the player by `offset` amount in the downwards direction.

        :param offset: The amount to translate the player by.
        """
        self.angle = pi
        self.speed = offset
        if self.rect.y < (MAX_DOWN - self.rect.height):
            self.rect.bottom += offset
            self.hitbox[1] += offset

    def move_right(self, offset=5):
        """
        Translate the player by `offset` amount in the right direction.

        :param offset: The amount to translate the player by.
        """
        self.angle = pi / 2
        self.speed = offset
        self.direction = RIGHT
        if self.rect.x < (MAX_RIGHT - self.rect.width):
            self.rect.right += offset
            self.hitbox[0] += offset

    def move_left(self, offset=5):
        """
        Translate the player by `offset` amount in the left direction.

        :param offset: The amount to translate the player by.
        """
        self.angle = -(pi / 2)
        self.speed = offset
        self.direction = LEFT
        if self.rect.x > MAX_LEFT:
            self.rect.left -= offset
            self.hitbox[0] -= offset

    def update_width_height(self):
        """
        Updates the players hitbox dimensions.

        Use this right after updating the players sprite to ensure accurate collisions.
        """
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox[2] = self.width + 5
        self.hitbox[3] = self.height + 5
