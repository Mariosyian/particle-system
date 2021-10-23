from time import sleep

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Screen limits
MAX_UP = -0.3
MAX_DOWN = -1.0
MAX_LEFT = -1.0
MAX_RIGHT = 1.0

def _move(object, direction, offset=0.01):
    """
    Increase the object's y-coordinates by `offset` amount.
    
    :param object: The object to apply the transformation to.
    :param direction: The direction on the screen to move towards.
        Can be any of [LEFT | RIGHT].
    :param y: The amount to translate the object by. 
    """
    index = 0
    for point in object:
        # Pass over the color
        if index == 4:
            break
        if direction == UP:
            point[1] += offset
        elif direction == DOWN:
            point[1] -= offset
        elif direction == RIGHT:
            point[0] += offset
        elif direction == LEFT:
            point[0] -= offset
        index += 1

def moveUp(object, offset=0.01):
    """
    Increase the object's y-coordinates by `offset` amount.
    
    :param object: The object to apply the transformation to.
    :param y: The amount to translate the object by. 
    """
    if object[0][1] < MAX_UP:
        _move(object, UP, offset)

def moveDown(object, offset=0.01):
    """
    Decrease the object's y-coordinates by `y` amount.
    
    :param object: The object to apply the transformation to.
    :param y: The amount to translate the object by. 
    """
    if object[3][1] > MAX_DOWN:
        _move(object, DOWN, offset)

def moveRight(object, offset=0.01):
    """
    Increase the object's x-coordinates by `offset` amount.
    
    :param object: The object to apply the transformation to.
    :param y: The amount to translate the object by. 
    """
    if object[1][0] < MAX_RIGHT:
        _move(object, RIGHT, offset)
    

def moveLeft(object, offset=0.01):
    """
    Decrease the object's x-coordinates by `offset` amount.
    
    :param object: The object to apply the transformation to.
    :param y: The amount to translate the object by. 
    """
    if object[3][0] > MAX_LEFT:
        _move(object, LEFT, offset)

def jump(object, max_height_offset=0.1, offset=0.01, tick=0.01):
    """
    Make the object jump (travel upwards, then return to the original position).

    :param object: The object to apply the transformation to.
    :param max_height_offset: The offset which the object 'jumps' to.
    :param offset: The offset that the object travels by, each tick.
    :param tick: The time interval to sleep between each loop.
        i.e. The games internal clock.
    """
    original_height = object[0][1]
    while object[0][1] < original_height + max_height_offset:
        object[0][1] += offset
        object[1][1] += offset
        object[2][1] += offset
        object[3][1] += offset
        sleep(tick)
    while object[0][1] > original_height:
        object[0][1] -= offset
        object[1][1] -= offset
        object[2][1] -= offset
        object[3][1] -= offset
        sleep(tick)