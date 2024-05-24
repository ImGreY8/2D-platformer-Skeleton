import sys
import pygame
import TilePlacement
from GameSettings import GAME_WIDTH
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()

        # importing assets
        self.import_player_assets()

        # Character Animation
        self.frame_index = 0
        self.frame_speed = 0.15

        # import dust particles
        self.import_run_particles()
        self.dust_frame_index = 0
        self.dust_frame_speed = 0.15
        self.display_surface = surface

        self.image = self.animation_states['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = 7

        self.gravity = 0.9
        self.jump_velocity = -16
        self.grounded = False

        # player state
        self.status = 'idle'
        self.facing_right = True

    def import_player_assets(self):
        player_path = 'PYgameAssests/3 - Overworld/graphics/character/'
        self.animation_states = {'idle': [], 'fall': [], 'jump': [], 'run': []}

        for animation in self.animation_states.keys():
            full_path = player_path + animation
            self.animation_states[animation] = import_folder(full_path)

    def import_run_particles(self):
        self.run_particles = import_folder('PYgameAssests/3 - Overworld/graphics/character/dust_particles/run')
        print(self.run_particles)

    def player_animation(self):
        animation = self.animation_states[self.status]
        self.frame_index += self.frame_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def run_particles_animation(self):
        if self.status == 'run':
            self.dust_frame_index += self.dust_frame_speed
            if self.dust_frame_index >= len(self.run_particles):
                self.dust_frame_index = 0

            dust_particles = self.run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos1 = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particles, pos1)
            if self.direction.x < 0:
                pos2 = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flip_dust = pygame.transform.flip(dust_particles, True, False)
                self.display_surface.blit(flip_dust, pos2)

    def get_player_state(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def player_movement(self):

        # player Horizontal movement
        input = pygame.key.get_pressed()
        if input[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif input[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif input[pygame.K_w] and input[pygame.K_SPACE]:
            self.jump_velocity = -25
        else:
            self.jump_velocity = -16
            self.direction.x = 0

    def player_camera(self):
        # Camera Scrolling with respect to player
        if self.rect.x < GAME_WIDTH / 4 and self.direction.x < 0:
            self.player_speed = 0
            TilePlacement.scroll_value = 8
        elif self.rect.x > GAME_WIDTH - (GAME_WIDTH / 4) and self.direction.x > 0:
            self.player_speed = 0
            TilePlacement.scroll_value = -8
        else:
            TilePlacement.scroll_value = 0
            self.player_speed = 7

    def player_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        if self.rect.y >= 750:
            pygame.quit()
            sys.exit()

    def player_jump(self):
        self.direction.y = self.jump_velocity

    def horizontal_collision(self):

        player_sprite = TilePlacement.player.sprite
        player_sprite.rect.x += player_sprite.direction.x * player_sprite.player_speed

        for sprite in TilePlacement.tiles.sprites():
            if sprite.rect.colliderect(player_sprite.rect):
                if self.direction.x < 0:
                    player_sprite.rect.left = sprite.rect.right
                elif self.direction.x > 0:
                    player_sprite.rect.right = sprite.rect.left

    def vertical_collision(self):

        jump_key = pygame.key.get_pressed()
        player_sprite = TilePlacement.player.sprite
        player_sprite.player_gravity()

        for sprite in TilePlacement.tiles.sprites():
            if sprite.rect.colliderect(player_sprite.rect):
                if self.direction.y > 0:
                    self.grounded = True
                    self.direction.y = 0
                    player_sprite.rect.bottom = sprite.rect.top
                elif self.direction.y != 0:
                    self.grounded = False
                if self.direction.y < 0:
                    self.direction.y = 0
                    player_sprite.rect.top = sprite.rect.bottom

        if jump_key[pygame.K_SPACE] and self.grounded:
            self.player_jump()
            self.grounded = False

    def update(self):

        # pos = pygame.mouse.get_pos()
        # print(pos)

        self.player_movement()
        self.player_camera()
        self.horizontal_collision()
        self.vertical_collision()
        self.get_player_state()
        self.player_animation()
        self.run_particles_animation()
