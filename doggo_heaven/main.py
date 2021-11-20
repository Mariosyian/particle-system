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
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

import pygame
import sys

from libraries import colors, vertices
from libraries.globals import *
from libraries.objloader import *
from libraries.Sprites import *
from math import pi
from random import randint
from time import time_ns


class Doggo_Heaven:
    """A class instance of the game 'Doggo Heaven'"""
    # World variables
    clock = None
    window = None
    sys_font = None
    font_color = colors.BLACK

    player_model = None

    center_x = 0
    center_y = 0
    center_z = 0

    eye_x = 0
    eye_y = 0
    eye_z = 0

    lon = 0.0
    lat = 0.0

    def calculate_lookpoint(self):
        self.center_x = self.eye_x + cos(self.lat * DEG_TO_RAD) * sin(self.lon * DEG_TO_RAD)
        self.center_y = self.eye_y + sin(self.lat * DEG_TO_RAD)
        self.center_z = self.eye_y + cos(self.lat * DEG_TO_RAD) * cos(self.lon * DEG_TO_RAD)

    def _initialise(self):
        """
        Initialise the `pygame` library and updates the games window and internal
        clock.
        """
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(SCREEN, DOUBLEBUF|OPENGL)
        self.sys_font = pygame.font.Font(pygame.font.get_default_font(), 14)
        pygame.display.set_caption(f"Doggo Heaven")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.ico").convert())

        # Load the model
        self.player_model = OBJ("assets/models/cubone.obj", swapyz=True)
        self.player_model.generate()
        glMatrixMode(GL_PROJECTION)

        # Position the camera
        gluPerspective(100.0, WINDOW_WIDTH/WINDOW_HEIGHT, 1.0, 100.0)
        glTranslatef(0.0, -5.0, -20.0)
        # Color the background
        glClearColor(colors.SKY[0], colors.SKY[1], colors.SKY[2], 1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

    def _reset(self):
        """Reset the program (Garbage collection)."""
        del self.clock
        del self.window
        del self.player_model

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

    def draw_ground(self):
        vertices = (
            (-20, 0, -20),
            (-20, 0, 20),
            (20, 0, 20),
            (20, 0, -20),
        )
        quads = (
            (0, 1, 2, 3),
        )

        glColor3f(colors.GREEN[0], colors.GREEN[1], colors.GREEN[2])
        glBegin(GL_QUADS)
        for quad in quads:
            for vertex in quad:
                glVertex3fv(vertices[vertex])
        glEnd()
        glColor3f(0, 0, 0)

    def main(self):
        """Run the program."""
        self._initialise()
        FPS = GOLDEN_FPS
        draw_hitboxes = False

        self.center_x = 0
        self.center_y = 0
        self.center_z = 0

        self.eye_x = 0
        self.eye_y = -5.0
        self.eye_z = -20.0

        self.lon = 0.0
        self.lat = 0.0

        # Reset here as the import is done after rendering, hence an `UnboundLocalError`
        # is raised.
        GRAVITY_MAGN = 1.0
        LIFETIME = 0

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
        angle = 0
        bg = pygame.image.load("assets/images/bg.jpg").convert()        
        pygame.key.set_repeat(1, 10)
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                # Key Bindings
                keys = pygame.key.get_pressed()

                # Camera movement
                ## Anti-clockwise rotation on longitude
                if keys[pygame.K_RIGHT]:
                    angle += 1
                ## Clockwise rotation on longitude
                if keys[pygame.K_LEFT]:
                   angle -= 1

                # Movement
                ## Up
                if keys[pygame.K_w]:
                    self.eye_x += sin((self.lon) * DEG_TO_RAD)
                    self.eye_z += cos((self.lon) * DEG_TO_RAD)
                ## Down
                if keys[pygame.K_s]:
                    self.eye_x -= sin((self.lon) * DEG_TO_RAD)
                    self.eye_z -= cos((self.lon) * DEG_TO_RAD)
                ## Left
                if keys[pygame.K_a]:
                    self.eye_x += sin((self.lon + 90.0) * DEG_TO_RAD)
                    self.eye_z += cos((self.lon + 90.0) * DEG_TO_RAD)
                ## Right
                if keys[pygame.K_d]:
                    self.eye_x -= sin((self.lon + 90.0) * DEG_TO_RAD)
                    self.eye_z -= cos((self.lon + 90.0) * DEG_TO_RAD)
                ## Jump
                # if (
                #     event.type == pygame.KEYUP
                #     and event.key  == pygame.K_SPACE
                #     and not player.is_jumping
                #     and not player.is_dropping
                # ):
                #     time_jump = time_ns()
                #     player.is_jumping = True

                # Change video settings (Graphic settings)
                if (
                    event.type == pygame.KEYUP
                    and event.key == pygame.K_f
                    # and not (player.is_jumping or player.is_dropping)
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
                    # and not (player.is_jumping or player.is_dropping)
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
                    # and not (player.is_jumping or player.is_dropping)
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
                    # Models
                    del background
                    self._reset()

                # Add tennis balls
                
                # Remove tennis balls

                # Quit
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    return

            # Jump movement

                # Stop the motion early if out of bounds

            # Tennis ball movement

                # Gravity

                ## Collisions
                # Tennis ball with player

                # Tennis ball with tennis ball

                    # Explosion !!\*o*/!!

            # Draw the game
            # Draw the HUD
            self.window.blit(self.sys_font.render(f"FPS: {int(self.clock.get_fps())} - Switch between FPS settings with the 'f' key", True, self.font_color), (10, 5))
            self.window.blit(self.sys_font.render(f"Move: W, A, S, D -- Jump: Space", True, self.font_color), (10, 20))
            # self.window.blit(self.sys_font.render(f"Tennis Balls: {len(tennis_balls)} - Add/Remove balls with the '+' and '-' keys", True, self.font_color), (10, 35))
            self.window.blit(self.sys_font.render(f"Gravity: {GRAVITY_MAGN} - Increase by pressing 'CTRL + g', or decrease by pressing the 'SHIFT + g' keys", True, self.font_color), (10, 50))
            self.window.blit(self.sys_font.render(f"Lifetime: {LIFETIME}s - Increase by pressing 'CTRL + t', or decrease by pressing the 'SHIFT + t' keys (Does not affect currently rendered balls)", True, self.font_color), (10, 65))
            self.window.blit(self.sys_font.render(f"Does not affect currently rendered balls. Set to 0 for infinite lifetime.", True, self.font_color), (105, 80))
            self.window.blit(self.sys_font.render(f"Toggle hitboxes with the 'h' key", True, self.font_color), (10, 95))

            # Swap buffers
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            # self.calculate_lookpoint()
            gluLookAt(self.eye_x, self.eye_y, self.eye_z, self.center_x, self.center_y, self.center_z, 0, 1, 0)

            glRotate(angle, 0, 1, 0)
            self.draw_ground()
            self.player_model.render()

            pygame.display.flip()


pygame.init()
Doggo_Heaven().main()
pygame.quit()
quit()