# -------------------------------------------------------------------------------------------------------------------- #
# add a camera.
# add particles.
# use paint for some features.
# -------------------------------------------------------------------------------------------------------------------- #

import pygame
import sys

# Variables ---------------------------------------------------------------------------------------------------------- #
n = 5
WHITE = (255, 255, 255)
GAME_WIDTH = 1536
GAME_HEIGHT = 864
FPS = 60
screen = pygame.display.set_mode(size=(GAME_WIDTH, GAME_HEIGHT))

# Loading image.------------------------------------------------------------------------------------------------------ #
bg_image_ground = pygame.image.load('PYgameAssests/ground.png').convert_alpha()

# Calculating the ground image width.--------------------------------------------------------------------------------- #
bg_ground_width = bg_image_ground.get_width()

# collecting all background images in a list and displaying on the screen -------------------------------------------- #
bg_image_list = []
for i in range(1, 6):
    bg_image = pygame.image.load(f'PYgameAssests/plxbg-{i}.png').convert_alpha()
    bg_image_list.append(bg_image)


# Function to control the movement of the background image.----------------------------------------------------------- #
def background_movement():
    # calculating the width of the background image and placing the image next to each other.------------------------- #
    bg_width = bg_image_list[0].get_width()
    for x in range(n):
        bg_image_speed = 1
        for image in bg_image_list:
            screen.blit(image, ((x * bg_width) - game.bg_movement * bg_image_speed, 0))
            bg_image_speed += 0.2


def ground():
    # displaying ground image on Screen next to each other.----------------------------------------------------------- #
    for ground_image in range(n):
        screen.blit(bg_image_ground, (((ground_image * bg_ground_width) - 2) - game.bg_movement * 2.3, 770))


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        # Variables For Adding Left, Right And Jump to the cat --------------------------------------------------------#
        self.delta_x = 0
        self.delta_y = 0

        # Variables For Adding jump to the cat ------------------------------------------------------------------------#
        self.is_cat_jumping = False
        self.cat_gravity = 1
        self.cat_velocity = 0

        # Applying camera to the cat ----------------------------------------------------------------------------------#
        self.camera_scroll = 0

        # Loading Player Image, rectangle and getting the width and height of that image.----------------------------- #
        # Cat idle Sprites --------------------------------------------------------------------------------------------#
        self.cat_idle_list = []
        self.cat_idle_index = 0
        for _ in range(1, 4):
            self.cat_idle_list.append(pygame.image.load(f'PYgameAssests/cat_idle_{_}.png').convert_alpha())

        self.image = self.cat_idle_list[int(self.cat_idle_index)]

        # Cat walking Sprites -----------------------------------------------------------------------------------------#
        self.cat_walk_list = []
        self.cat_walk_index = 0
        for _ in range(1, 6):
            self.cat_walk_list.append(pygame.image.load(f'PYgameAssests/Cat_walk_resize_{_}.png').convert_alpha())

        self.image = self.cat_walk_list[int(self.cat_walk_index)]

        # Creating Rectangle for each sprite group --------------------------------------------------------------------#
        self.rect = self.image.get_rect(topleft=(300, 624))

        # rect bottom: 774
        # rect y: 624

    def cat_animation(self):

        if game.is_cat_idle:
            self.cat_idle_index += 0.08

            if self.cat_idle_index >= len(self.cat_idle_list):
                self.cat_idle_index = 0

        self.image = self.cat_idle_list[int(self.cat_idle_index)]

        key_for_cat_movement = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if key_for_cat_movement[pygame.K_d] or key_for_cat_movement[pygame.K_a]:
                game.is_cat_idle = False
                game.is_cat_walking = True

                if game.is_cat_walking:
                    self.cat_walk_index += 0.3

                    if self.cat_walk_index >= len(self.cat_walk_list):
                        self.cat_walk_index = 0

                self.image = self.cat_walk_list[int(self.cat_walk_index)]
            else:
                game.is_cat_idle = True

        if key_for_cat_movement[pygame.K_a]:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
            self.delta_x += 3.0
        if key_for_cat_movement[pygame.K_d]:
            self.delta_x -= 3.0
        if self.delta_x <= -115:
            self.delta_x = -115
        if self.delta_x > 335:
            self.delta_x = 335

        self.rect = self.image.get_rect(topleft=(300 - self.delta_x, 624))

    def cat_jumping(self):
        key_for_cat_jumping = pygame.key.get_pressed()

        if key_for_cat_jumping[pygame.K_SPACE] and not self.is_cat_jumping:
            self.cat_velocity = -15

        if not key_for_cat_jumping[pygame.K_SPACE]:
            self.is_cat_jumping = False

        # Adding Gravity ----------------------------------------------------------------------------------------------#
        self.cat_velocity += 1
        if self.cat_velocity > 15:
            self.cat_velocity = 15

        self.delta_y += self.cat_velocity
        self.rect.y += self.delta_y

        if self.rect.bottom >= 774:
            self.rect.bottom = 774
            self.delta_y = 0

    def update(self):
        self.cat_animation()
        self.cat_jumping()


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.bg_movement = 0
        self.is_cat_idle = True
        self.is_cat_walking = False

        # Naming the game -------------------------------------------------------------------------------------------- #
        pygame.display.set_caption('The Rising Alps')

        # Creating Sprite and groups --------------------------------------------------------------------------------- #
        self.player_sprite = pygame.sprite.GroupSingle()
        Player(self.player_sprite)

    def run(self):
        game_run = True
        while game_run:

            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)

            # Get User input.----------------------------------------------------------------------------------------- #
            key = pygame.key.get_pressed()
            if key[pygame.K_a] and self.bg_movement > 0:
                self.bg_movement -= 3.0
            if key[pygame.K_d]:
                self.bg_movement += 3.0
            if key[pygame.K_a] and key[pygame.K_d]:
                self.bg_movement -= 1.0

            # ESC to escape the game
            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            # game quit ---------------------------------------------------------------------------------------------- #
            for game_event in pygame.event.get():
                if game_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Calling the Function.----------------------------------------------------------------------------------- #
            background_movement()
            self.player_sprite.draw(screen)
            self.player_sprite.update()
            ground()

            self.clock.tick(FPS)
            pygame.display.update()

    def update(self):
        self.run()


if __name__ == "__main__":
    game = Game()
    game.run()
