# Generic entity data

class Entity:
    """
    An object to represent player, enemies, items, etcself.
    """

    def __init__(self, x, y, char, color):

        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):

        #move entity by a given amount

        self.x += dx
        self.y += dy
