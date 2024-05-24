import pygame
from support import import_folder


class Particles(pygame.sprite.Sprite):
    def __init__(self, pos, animation_type):
        super().__init__()
        self.frame_index = 0
        self.frame_speed = 0.15

        if animation_type == 'jump':
            self.frames = import_folder('PYgameAssests/3 - Overworld/graphics/character/dust_particles/jump')
        if animation_type == 'land':
            self.frames = import_folder('PYgameAssests/3 - Overworld/graphics/character/dust_particles/land')

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get.rect(center=pos)

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_change):
        self.animate()
        self.rect.x += x_change
