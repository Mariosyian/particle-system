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

        ## Bakcground
        self._create_background_objects()

        ## Tennis ball
        tennis_ball_img = pygame.image.load(
            "assets/images/models/tennis_ball/tennis_ball_25x25.png"
        ).convert_alpha()
        tennis_ball = Tennis_Ball(
            tennis_ball_img,
            tennis_ball_img.get_width(),
            tennis_ball_img.get_height(),
            50,
            200,
        )
        self.tennis_ball_group.add(tennis_ball)
        tennis_ball_rect = tennis_ball.rect

        ## Player
        player_left = pygame.image.load(
            "assets/images/models/dog/dog_left.png"
        ).convert_alpha()
        player_right = pygame.image.load(
            "assets/images/models/dog/dog_right.png"
        ).convert_alpha()
        player = Player(
            player_left, player_left.get_width(), player_left.get_height(), 850, 500
        )
        self.player_group.add(player)
        player_rect = player.rect

        # Physics
        offset = 0.5
        acceleration = 0.2
        tennis_ball_speed = [0, offset * acceleration]
        acceleration_rate = 0.05
        MAX_ACCELERATION = 0.5

        # Jump variables
        jump_peak = 40
        jump_offset = 2
        original_height = 0

        window.blit(background, (0, 0))
        pygame.display.flip()

        while True:
            clock.tick(FPS)
            pygame.display.set_caption(f"Doggo Heaven - {int(clock.get_fps())} FPS")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                # Key Bindings
                keys = pygame.key.get_pressed()
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
                ):
                    original_height = player_rect.y
                    player.is_jumping = True

                # Change video settings (Graphic settings)
                if keys[pygame.K_g] and event.type == pygame.KEYDOWN:
                    FPS = LOW_FPS if FPS == GOLDEN_FPS else GOLDEN_FPS

                # Quit
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    return

            # Jump movement
            if player.is_jumping:
                if player_rect.y > original_height - jump_peak:
                    player_rect.y -= jump_offset
                else:
                    player.is_jumping = False
                    player.is_dropping = True
            if player.is_dropping:
                if player_rect.y < original_height:
                    player_rect.y += jump_offset
                else:
                    player.is_jumping = False
                    player.is_dropping = False

            # If at any point, for whatever reason, the player model goes above the
            # allowed limit reset their position.
            if player_rect.y <= (400 - jump_peak + jump_offset):
                player.is_jumping = False
                player.is_dropping = False
                # Move the player model down to where they were before the action that
                # caused them to go off screen (most likely jump, hence `original_height`)
                player_rect.y = original_height

            # Ball movement
            tennis_ball_speed[1] += acceleration
            acceleration = (
                (acceleration + acceleration_rate)
                if acceleration < MAX_ACCELERATION
                else MAX_ACCELERATION
            )
            tennis_ball_rect = tennis_ball_rect.move(tennis_ball_speed)
            if tennis_ball_rect.top <= 0 or tennis_ball_rect.bottom >= WINDOW_HEIGHT:
                tennis_ball_speed[1] = -tennis_ball_speed[1]

            ## Collision logic
            # Tennis ball with player
            if tennis_ball_rect.colliderect(player_rect):
                tennis_ball_rect.y -= tennis_ball_speed[1]
                tennis_ball_speed[1] = -tennis_ball_speed[1]

            # Draw the background and the background objects
            window.blit(background, (0, 0))
            self.background_group.draw(window)
            window.blit(tennis_ball.image, tennis_ball_rect)
            window.blit(player.image, player_rect)
            pygame.display.flip()


Doggo_Heaven().main()
pygame.quit()
