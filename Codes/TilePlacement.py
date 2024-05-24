import pygame
from TileDesign import Tile
from GameSettings import *
from player import Player

# Dependent Variable
scroll_value = 1
tiles = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()


class Level:
    def __init__(self, leve_map_data, lvl_surface):
        super().__init__()
        self.level_surface = lvl_surface
        self.level_draw(leve_map_data)

    def level_draw(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    tiles.add(tile)
                if col == 'P':
                    player_obj = Player((x, y), self.level_surface)
                    player.add(player_obj)

    def run(self):
        # for tiles
        tiles.update(scroll_value)
        tiles.draw(self.level_surface)

        # for Player
        player.update()
        player.draw(self.level_surface)
