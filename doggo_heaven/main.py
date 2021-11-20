"""
Author: Marios Yiannakou

The main instance of the particle system.

System used:
- CPU: AMD Ryzen 7 5700U
- GPU: AMD (Integrated) Radeon Graphics
- RAM: 1 * 8GB DDR4 @ 3200MHz
"""
# Remove the pygame welcome message ...
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from gc import collect
import pygame

from libraries import colors
from libraries.globals import *
from libraries.Sprites import *
from math import pi
from random import randint
from time import time_ns


class Doggo_Heaven:
    """A class instance of the game 'Doggo Heaven'"""

    # Sprite groups
    background_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tennis_ball_group = pygame.sprite.Group()

    # World variables
    clock = None
    window = None
    sys_font = None
    font_color = colors.BLACK

    def _initialise(self):
        """
        Initialise the `pygame` library and updates the games window and internal
        clock.
        """
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(SCREEN)
        self.sys_font = pygame.font.Font(pygame.font.get_default_font(), 14)
        pygame.display.set_caption(f"Doggo Heaven")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.ico").convert())

    def _reset(self):
        """Reset the program (Garbage collection)."""
        del self.clock
        del self.window

        for surface in self.background_group:
            del surface
        self.background_group.empty()

        for surface in self.tennis_ball_group:
            del surface
        self.tennis_ball_group.empty()

        for surface in self.player_group:
            del surface
        self.player_group.empty()

        collect(generation=2)
        self.main()

    def main(self):
        """Run the program."""
        self._initialise()
        FPS = GOLDEN_FPS
        draw_hitboxes = False
        # Reset here as the import is done after rendering, hence an `UnboundLocalError`
        # is raised.
        GRAVITY_MAGN = 1.0
        LIFETIME = 0

        # Sprites
        ## Background
        background= pygame.image.load("assets/images/bg.jpg").convert()

        ## Tennis ball
        tennis_ball_img = pygame.image.load(
            "assets/images/models/tennis_ball/tennis_ball_25x25.png"
        ).convert_alpha()
        for i in range(NUM_OF_BALLS):
            self.tennis_ball_group.add(
                Tennis_Ball(
                    tennis_ball_img,
                    tennis_ball_img.get_width(),
                    tennis_ball_img.get_height(),
                    tennis_ball_img.get_width() + i * (WINDOW_WIDTH / NUM_OF_BALLS),
                    200,
                    pi,
                    GRAVITY_MAGN,
                    0.8,
                    LIFETIME,
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
        jump_offset_dict = {
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
            self.clock.tick(FPS)
            # Keep a track of all tennis ball sprites
            tennis_balls = self.tennis_ball_group.sprites()

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
                    event.type == pygame.KEYUP
                    and event.key  == pygame.K_SPACE
                    and not player.is_jumping
                    and not player.is_dropping
                ):
                    time_jump = time_ns()
                    player.is_jumping = True

                # Change video settings (Graphic settings)
                if (
                    event.type == pygame.KEYUP
                    and event.key == pygame.K_f
                    and not (player.is_jumping or player.is_dropping)
                ):
                    if FPS == LOW_FPS:
                        FPS = GOLDEN_FPS
                    elif FPS == GOLDEN_FPS:
                        FPS = MAX_FPS
                    elif FPS == MAX_FPS:
                        FPS = LOW_FPS

                ## Gravity settings
                # Decrease gravity
                if (
                    event.type == pygame.KEYUP
                    and pygame.key.get_mods() & pygame.KMOD_SHIFT
                    and event.key == pygame.K_g
                    and not (player.is_jumping or player.is_dropping)
                ):
                    if GRAVITY_MAGN > 0.1:
                        GRAVITY_MAGN = float("{:.1f}".format(GRAVITY_MAGN - 0.1))
                    if GRAVITY_MAGN <= 0.6:
                        del background
                        background = pygame.image.load("assets/images/bg_space.jpg").convert()
                        self.font_color = colors.WHITE
                # Increase gravity
                if (
                    event.type == pygame.KEYUP
                    and pygame.key.get_mods() & pygame.KMOD_CTRL
                    and event.key == pygame.K_g
                    and not (player.is_jumping or player.is_dropping)
                ):
                    GRAVITY_MAGN = float("{:.1f}".format(GRAVITY_MAGN + 0.1))
                    if GRAVITY_MAGN > 0.6:
                        del background
                        background = pygame.image.load("assets/images/bg.jpg").convert()
                        self.font_color = colors.BLACK

                ## Ball lifetime settings
                # Decrease lifetime
                if (
                    event.type == pygame.KEYUP
                    and pygame.key.get_mods() & pygame.KMOD_SHIFT
                    and event.key == pygame.K_t
                ):
                    if LIFETIME > 0:
                        LIFETIME -= 1
                # Increase lifetime
                if (
                    event.type == pygame.KEYUP
                    and pygame.key.get_mods() & pygame.KMOD_CTRL
                    and event.key == pygame.K_t
                ):
                    LIFETIME += 1

                # Toggle hitboxes
                if (
                    event.type == pygame.KEYUP
                    and event.key == pygame.K_h
                ):
                    draw_hitboxes = not draw_hitboxes

                # Reset and Garbage collection
                if keys[pygame.K_r]:
                    # Sprites
                    del tennis_ball_img
                    del player_drop_left
                    del player_drop_right
                    del player_jump_left
                    del player_jump_right
                    del player_left
                    del player_right
                    # Models
                    del player
                    del background
                    self._reset()

                # Add tennis balls
                if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
                    self.tennis_ball_group.add(
                        Tennis_Ball(
                            tennis_ball_img,
                            tennis_ball_img.get_width(),
                            tennis_ball_img.get_height(),
                            randint(tennis_ball_img.get_width(), WINDOW_WIDTH - tennis_ball_img.get_width()),
                            randint(tennis_ball_img.get_height(), 200),
                            pi,
                            GRAVITY_MAGN,
                            0.8,
                            LIFETIME,
                        )
                    )
                
                # Remove tennis balls
                if keys[pygame.K_MINUS]:
                    tennis_balls = self.tennis_ball_group.sprites()
                    if len(tennis_balls) > 0:
                        last_ball = tennis_balls[-1]
                        self.tennis_ball_group.remove(
                            last_ball
                        )
                        del last_ball

                # Quit
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    return

            # Jump movement
            if player.is_jumping:
                player.image = (
                    player_jump_left if player.direction == LEFT else player_jump_right
                )
                player.hitbox[2] = player.image.get_width() + 5
                player.hitbox[3] = player.image.get_height() + 5
                player.direction = UP

                # Stop the motion early if out of bounds
                if player.rect.y <= 0:
                    time_drop = time_ns()
                    player.is_jumping = False
                    player.is_dropping = True

                if (time_ns() - time_jump) <= (jump_duration / GRAVITY_MAGN):
                    jump_offset = jump_offset_dict[FPS]
                    player.speed = jump_offset
                    player_rect.y -= jump_offset
                    player.hitbox[1] -= jump_offset
                else:
                    time_drop = time_ns()
                    player.is_jumping = False
                    player.is_dropping = True

            if player.is_dropping:
                player.image = (
                    player_drop_left if player.direction == LEFT else player_drop_right
                )
                player.hitbox[2] = player.image.get_width() + 5
                player.hitbox[3] = player.image.get_height() + 5
                player.direction = DOWN

                # Stop the motion early if out of bounds
                if player.rect.y >= (WINDOW_HEIGHT - player.rect.height):
                    player.is_dropping = False
                    player.is_jumping = False

                if (time_ns() - time_drop) <= (jump_duration / GRAVITY_MAGN):
                    jump_offset =  jump_offset_dict[FPS]
                    player.speed = jump_offset
                    player_rect.y += jump_offset
                    player.hitbox[1] += jump_offset
                else:
                    del time_drop
                    player.is_dropping = False
                    player.is_jumping = False

            if not player.is_jumping and not player.is_dropping:
                player.image = player_left if player.direction == LEFT else player_right
                player.hitbox[2] = player.image.get_width() + 5
                player.hitbox[3] = player.image.get_height() + 5

            # Tennis ball movement
            for tennis_ball in tennis_balls:
                if not tennis_ball.alive():
                    self.tennis_ball_group.remove(tennis_ball)
                    del tennis_ball
                    continue
                # Gravity
                tennis_ball.rect = tennis_ball.apply_gravity(GRAVITY_MAGN)
                tennis_ball.rect = tennis_ball.bounce()
                ## Collisions
                # Tennis ball with player
                if tennis_ball.rect.colliderect(player_rect):
                    (tennis_ball.angle, tennis_ball.speed) = add_vectors(
                        player.angle, player.speed, tennis_ball.angle, tennis_ball.speed
                    )
                collided_tennis_ball = pygame.sprite.spritecollideany(
                    tennis_ball, self.tennis_ball_group
                )
                # Tennis ball with tennis ball
                if collided_tennis_ball and collided_tennis_ball != tennis_ball:
                    (tennis_ball.angle, tennis_ball.speed) = add_vectors(
                        tennis_ball.angle,
                        (tennis_ball.speed * tennis_ball.elasticity),
                        collided_tennis_ball.angle,
                        (collided_tennis_ball.speed * collided_tennis_ball.elasticity),
                    )
                    # Explosion !!\*o*/!!
                    collided_tennis_ball.angle = -tennis_ball.angle
                    collided_tennis_ball.speed *= collided_tennis_ball.elasticity

            # Draw the game
            self.window.blit(background, (0, 0))
            # self.background_group.draw(self.window)
            self.tennis_ball_group.draw(self.window)
            self.window.blit(player.image, player_rect)
            # Draw the HUD
            self.window.blit(self.sys_font.render(f"FPS: {int(self.clock.get_fps())} - Switch between FPS settings with the 'f' key", True, self.font_color), (10, 5))
            self.window.blit(self.sys_font.render(f"Move: W, A, S, D -- Jump: Space", True, self.font_color), (10, 20))
            self.window.blit(self.sys_font.render(f"Tennis Balls: {len(tennis_balls)} - Add/Remove balls with the '+' and '-' keys", True, self.font_color), (10, 35))
            self.window.blit(self.sys_font.render(f"Gravity: {GRAVITY_MAGN} - Increase by pressing 'CTRL + g', or decrease by pressing the 'SHIFT + g' keys", True, self.font_color), (10, 50))
            self.window.blit(self.sys_font.render(f"Lifetime: {LIFETIME}s - Increase by pressing 'CTRL + t', or decrease by pressing the 'SHIFT + t' keys", True, self.font_color), (10, 65))
            self.window.blit(self.sys_font.render(f"Does not affect currently rendered balls. Set to 0 for infinite lifetime.", True, self.font_color), (105, 80))
            self.window.blit(self.sys_font.render(f"Toggle hitboxes with the 'h' key", True, self.font_color), (10, 95))
            # Draw the hitboxes
            if draw_hitboxes:
                pygame.draw.rect(self.window, colors.RED, player.hitbox, 2)
                for tennis_ball in tennis_balls:
                    pygame.draw.rect(
                        self.window,
                        colors.BLACK,
                        (
                            tennis_ball.rect.topleft[0] - 5,
                            tennis_ball.rect.topleft[1] - 5,
                            tennis_ball.width + 5,
                            tennis_ball.height + 5,
                        ),
                        2
                    )

            # Swap buffers
            pygame.display.flip()


pygame.init()
Doggo_Heaven().main()
pygame.quit()
quit()