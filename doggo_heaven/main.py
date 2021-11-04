"""
Author: Marios Yiannakou

The main instance of the particle system.
"""
# Remove the pygame welcome message ...
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from libraries import colors, vertices
from libraries.globals import *
from libraries.Sprites import *
from math import pi
from time import time_ns


class Doggo_Heaven:
    """A class instance of the game 'Doggo Heaven'"""

    # Sprite groups
    background_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tennis_ball_group = pygame.sprite.Group()

    def _initialise(self):
        """
        Initialise the `pygame` library and create the games window and internal clock.

        :returns: The internal clock and game window as a tuple.
        """
        pygame.init()
        clock = pygame.time.Clock()
        window = pygame.display.set_mode(SCREEN)
        pygame.display.set_caption(f"Doggo Heaven - {int(clock.get_fps())} FPS")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.ico").convert())

        return (clock, window)

    def _create_background_objects(self):
        """
        Creates all background objects as sprites and adds them to the `background_objects`
        sprite group.
        """
        # cloud_1
        cloud_1 = vertices.cloud_1
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(cloud_1),
                vertices.get_height(cloud_1),
                vertices.get_origin_x(cloud_1),
                vertices.get_origin_y(cloud_1),
                0,
                0,
                0,
                vertices.get_color(cloud_1),
            )
        )
        del cloud_1

        # cloud_2
        cloud_2 = vertices.cloud_2
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(cloud_2),
                vertices.get_height(cloud_2),
                vertices.get_origin_x(cloud_2),
                vertices.get_origin_y(cloud_2),
                0,
                0,
                0,
                vertices.get_color(cloud_2),
            )
        )
        del cloud_2

        # cloud_2_1
        cloud_2_1 = vertices.cloud_2_1
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(cloud_2_1),
                vertices.get_height(cloud_2_1),
                vertices.get_origin_x(cloud_2_1),
                vertices.get_origin_y(cloud_2_1),
                0,
                0,
                0,
                vertices.get_color(cloud_2_1),
            )
        )
        del cloud_2_1

        # mountain_1
        mountain_1 = vertices.mountain_1
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(mountain_1),
                vertices.get_height(mountain_1),
                vertices.get_origin_x(mountain_1),
                vertices.get_origin_y(mountain_1),
                0,
                0,
                0,
                vertices.get_color(mountain_1),
            )
        )
        del mountain_1

        # mountain_1_1
        mountain_1_1 = vertices.mountain_1_1
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(mountain_1_1),
                vertices.get_height(mountain_1_1),
                vertices.get_origin_x(mountain_1_1),
                vertices.get_origin_y(mountain_1_1),
                0,
                0,
                0,
                vertices.get_color(mountain_1_1),
            )
        )
        del mountain_1_1

        # ground
        ground = vertices.ground
        self.background_group.add(
            Sprite(
                None,
                vertices.get_width(ground),
                vertices.get_height(ground),
                vertices.get_origin_x(ground),
                vertices.get_origin_y(ground),
                0,
                0,
                0,
                vertices.get_color(ground),
            )
        )
        del ground

    def main(self):
        """
        Run the program.
        """
        clock, window = self._initialise()
        FPS = GOLDEN_FPS

        # Sprites
        ## Sky
        background = pygame.Surface(SCREEN).convert()
        pygame.Surface.fill(background, colors.SKY)
        window.blit(background, (0, 0))

        ## Bakcground
        self._create_background_objects()

        ## Tennis ball
        tennis_ball_img = pygame.image.load(
            "assets/images/models/tennis_ball/tennis_ball_25x25.png"
        ).convert_alpha()
        for i in range(10):
            self.tennis_ball_group.add(
                Tennis_Ball(
                    tennis_ball_img,
                    tennis_ball_img.get_width(),
                    tennis_ball_img.get_height(),
                    50 + (i * 100),
                    200,
                    pi / 2,
                    0.4
                )
            )

        ## Player
        player_left = pygame.image.load(
            "assets/images/models/dog/dog_left.png"
        ).convert_alpha()
        player_right = pygame.image.load(
            "assets/images/models/dog/dog_right.png"
        ).convert_alpha()
        player_jump_right = pygame.image.load(
            "assets/images/models/dog/dog_jump_right.png"
        ).convert_alpha()
        player_jump_left = pygame.image.load(
            "assets/images/models/dog/dog_jump_left.png"
        ).convert_alpha()
        player_drop_right = pygame.image.load(
            "assets/images/models/dog/dog_drop_right.png"
        ).convert_alpha()
        player_drop_left = pygame.image.load(
            "assets/images/models/dog/dog_drop_left.png"
        ).convert_alpha()
        player = Player(
            player_left, player_left.get_width(), player_left.get_height(), 850, 500
        )
        self.player_group.add(player)
        player_rect = player.rect

        # Jump variables
        """
        Jump offset in pixels per FPS setting.

        Since pygame uses internal ticks rather than a real time clock,
        the more FPS it renders, the more ticks there are in a real time
        second. This results in a larger number of iterations of the event
        loop, hence the players total jump height becomes FPS dependent.

        Create a dictionary that uses a different offset (in pixels), based
        on the current FPS being used
        """
        jump_offset = {
            30: 6,
            60: 3,
            120: 2,
        }
        jump_duration = 0.5 * (1000 * 1000 * 1000)  # 0.5 ns

        """
        This line of code is required as it sets the amount of time (in ms) that a key
        is required to be pressed down, in order for it to be considered pressed and
        held down. The second parameter is the time between each "KEYDOWN" event that
        will be executed (in ms) after it's considered to be held down.

        This is allows the movement keys (W, A, S, D) to be pressed once and executed
        multiple times, simulating much smoother movement animation.
        """
        pygame.key.set_repeat(1, 10)
        while True:
            clock.tick(FPS)
            pygame.display.set_caption(f"Doggo Heaven - {int(clock.get_fps())} FPS")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                # Key Bindings
                keys = pygame.key.get_pressed()
                # Idle speed
                if (
                    not keys[pygame.K_w]
                    and not keys[pygame.K_s]
                    and not keys[pygame.K_a]
                    and not keys[pygame.K_d]
                ):
                    player.speed = 0

                # Movement
                ## Up
                if keys[pygame.K_w]:
                    player.move_up()
                ## Down
                if keys[pygame.K_s]:
                    player.move_down()
                ## Left
                if keys[pygame.K_a]:
                    player.image = player_left
                    player.move_left()
                ## Right
                if keys[pygame.K_d]:
                    player.image = player_right
                    player.move_right()
                ## Jump
                if (
                    keys[pygame.K_SPACE]
                    and event.type == pygame.KEYDOWN
                    and not player.is_jumping
                    and not player.is_dropping
                ):
                    time_jump = time_ns()
                    player.is_jumping = True

                # Change video settings (Graphic settings)
                # BUG: `pygame.key.set_repeat(1, 10)` causes this line to be executed
                #      multiple times per click, hence it rotates too quickly and
                #      causes unwanted results.
                if (
                    keys[pygame.K_g]
                    and event.type == pygame.KEYDOWN
                    and not (player.is_jumping or player.is_dropping)
                ):
                    if FPS == LOW_FPS:
                        FPS = GOLDEN_FPS
                    elif FPS == GOLDEN_FPS:
                        FPS = MAX_FPS
                    elif FPS == MAX_FPS:
                        FPS = LOW_FPS

                # Quit
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    return

            # Jump movement
            if player.is_jumping:
                player.image = (
                    player_jump_left if player.direction == LEFT else player_jump_right
                )
                if (time_ns() - time_jump) <= jump_duration:
                    player_rect.y -= jump_offset[FPS]
                else:
                    time_drop = time_ns()
                    player.is_jumping = False
                    player.is_dropping = True
            if player.is_dropping:
                player.image = (
                    player_drop_left if player.direction == LEFT else player_drop_right
                )
                if (time_ns() - time_drop) <= jump_duration:
                    player_rect.y += jump_offset[FPS]
                else:
                    player.is_dropping = False
                    player.is_jumping = False
            if not player.is_jumping and not player.is_dropping:
                player.image = player_left if player.direction == LEFT else player_right

            # Ball movement
            for tennis_ball in self.tennis_ball_group.sprites():
                tennis_ball.rect = tennis_ball.apply_gravity()
                tennis_ball.rect = tennis_ball.bounce()

            ## Collision logic
            # Tennis ball with player
            for tennis_ball in self.tennis_ball_group.sprites():
                if tennis_ball.rect.colliderect(player_rect):
                    (tennis_ball.angle, tennis_ball.speed) = add_vectors(
                        player.angle, player.speed, tennis_ball.angle, tennis_ball.speed
                    )

            # Draw the background and the background objects
            window.blit(background, (0, 0))
            self.background_group.draw(window)
            self.tennis_ball_group.draw(window)
            window.blit(player.image, player_rect)
            pygame.display.flip()


Doggo_Heaven().main()
pygame.quit()
