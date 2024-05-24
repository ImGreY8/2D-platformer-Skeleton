from os import walk
import pygame


def import_folder(path):
    all_assets_on_surface_list = []

    for _, _, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            all_assets_on_surface_list.append(image_surface)

    return all_assets_on_surface_list

# import_folder('PYgameAssests/MarioKing/idle')
