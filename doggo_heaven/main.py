import libraries.colors as colors
import libraries.vertices as vertices
import glfw
import keyboard

from copy import deepcopy
from libraries.movement import *
from OpenGL.GL import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

player = deepcopy(vertices.dog)


def initialise():
    """
    Initialise the rendering sequence and check for null values.

    :returns: The window instance used for rendering.
    :throws Exception: If any of the initialisations return null.
    """
    # Initialise the glfw module
    if not glfw.init():
        raise Exception("The GLFW library has failed to initialise.")

    # Configure the window
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Doggo Heaven", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Window failed to generate.")
    glfw.make_context_current(window)

    return window

def destroy(window):
    """
    Performs any necessary clean-up before terminating:
        - Sets a windows CLOSABLE property to `True`.

    :param window: The window to be closed.
    """
    glfw.set_window_should_close(window, True)

def reset():
    """
    Reset the game to its original state.
    """
    # Reset the player ... `player=deepcopy(vertices.dog)` did not work
    index = 0
    for vertice in player:
        if index == 4:
            vertice = vertices.get_color(vertices.dog)
            break
        vertice[0] = vertices.dog[index][0]
        vertice[1] = vertices.dog[index][1]
        vertice[2] = vertices.dog[index][2]
        index += 1

def draw_quads(quads):
    """
    Draws the given array of quadrangles.

    :params quads: An array of exactly five elements.
        The first four elements must be the (x, y, z) coordinates of the quadrangle,
        and the fifth element must either `None`, or a color in the form of (r, g, b).
    """
    glBegin(GL_QUADS)
    for quad in quads:
        if quad[4]:
            glColor(quad[4])
        glVertex3f(quad[0][0], quad[0][1], quad[0][2])
        glVertex3f(quad[1][0], quad[1][1], quad[1][2])
        glVertex3f(quad[2][0], quad[2][1], quad[2][2])
        glVertex3f(quad[3][0], quad[3][1], quad[3][2])

    glColor(colors.WHITE)
    glEnd()

def main():
    """
    Run the program.
    """
    window = initialise()
    # Limit FPS by drawing at slower intervals (solves 100% GPU usage)
    # Through trial and error, I found that this value gives the best GPU
    #   performance and still provide natural-looking movement.
    glfw.swap_interval(2)

    # Key-Bindings
    ## Quit
    keyboard.add_hotkey("q", destroy, args=[window])
    keyboard.add_hotkey("esc", destroy, args=[window])
    ## Settings / Config
    # keyboard.add_hotkey("c", config, args=[])
    ## Reset
    keyboard.add_hotkey("r", reset, args=[])
    ## Movement
    ### Up
    keyboard.add_hotkey("w", moveUp, args=[player])
    ### Down
    keyboard.add_hotkey("s", moveDown, args=[player])
    ### Left
    keyboard.add_hotkey("a", moveLeft, args=[player])
    ### Right
    keyboard.add_hotkey("d", moveRight, args=[player])
    ### Jump
    keyboard.add_hotkey("space", jump, args=[player])

    # Render the window
    while not glfw.window_should_close(window):
        # Draw the sky
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(colors.SKY[0], colors.SKY[1], colors.SKY[2], 1)

        glfw.poll_events()
        draw_quads([
            vertices.cloud_1,
            vertices.cloud_2,
            vertices.cloud_2_1,
            vertices.mountain_1,
            vertices.mountain_1_1,
            vertices.ground,
            player
        ])
        glfw.swap_buffers(window)

    # Clean up
    glfw.terminate()

main()
