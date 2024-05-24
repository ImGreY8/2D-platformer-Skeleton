import pygame
import sys
from GameSettings import *
from TilePlacement import Level

pygame.init()

# Initial Display / Screen
screen = pygame.display.set_mode(size=(GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Jack's Adventure")
clock = pygame.time.Clock()

level = Level(basic_level_map, screen)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    screen.fill('black')
    # Calling the Functions And objects for the Classes
    level.run()

    pygame.display.update()
    clock.tick(FPS)
