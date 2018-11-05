import libtcodpy as libtcod
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint
from entity import Entity

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialise_tiles()

    def initialise_tiles(self):

        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]



        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):

        rooms = []
        num_rooms = 0

        for r in range(max_rooms):

            #Random width and height

            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # Random position without going beyond map boundaries

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            #run through the other rooms and check for intersections
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #presumes there are no intersections.
                #Paint to map tiles
                self.create_room(new_room)

                #center coordinates of the new room. Useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #Checks to see if this the newest room
                    player.x = new_x
                    player.y = new_y

                else:
                    #connect to previous room with a tunnel
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    #flip a coin
                    if randint(0, 1) == 1:
                        #first move horizontally
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room)

                #append new room to list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):

        #Go through the tiles in the rectangle and make them passable.
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):

        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monster, max_monsters_per_room):
        #get random number of monsters

        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            #choose random location in room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green)
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        else:
            return False
