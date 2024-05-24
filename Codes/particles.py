import pygame
import random
import sys


# class to control the drawing, moving and deleting of Particles -------------------------------#
class DrawParticles:
    def __init__(self):
        self.particles = []

    def particle_movement(self):
        if self.particles:
            self.delete_particles()
            for one_particle in self.particles:
                one_particle[0][0] += one_particle[2][0]
                one_particle[0][1] += one_particle[2][1]
                one_particle[1] -= 0.2

                # draw circle around the particles ---------------------------------------------#
                pygame.draw.circle(screen, pygame.Color('White'), one_particle[0], int(one_particle[1]))

    def add_particles(self):
        x_pos = 250
        y_pos = 250
        x_direction = random.randint(-5, 5)
        y_direction = random.randint(-5, 5)
        radius = 5

        particle_total = [[x_pos, y_pos], radius, [x_direction, y_direction]]
        self.particles.append(particle_total)

    def delete_particles(self):
        particle_list_copy = [particle for particle in self.particles if particle[1] > 0]
        particle_obj.particles = particle_list_copy

    def update(self):
        self.particle_movement()
        self.add_particles()
        self.delete_particles()


# initializing pygame
pygame.init()

# constant variables ---------------------------------------------------------------------------#
FPS = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Set the pygame Window ------------------------------------------------------------------------#
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PARTICLES")

# create object of class DrawParticles ---------------------------------------------------------#
particle_obj = DrawParticles()

# Setting the timer for the above event --------------------------------------------------------#
PARTICLE_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_SPAWN_EVENT, 40)

# Game Loop ------------------------------------------------------------------------------------#
while True:

    # Fill background colour with Black --------------------------------------------------------#
    screen.fill((30, 30, 30))

    # setup to Exit the Game -------------------------------------------------------------------#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        # Check for the event and call the function particle accordingly.
        if event.type == PARTICLE_SPAWN_EVENT:
            particle_obj.add_particles()

    # calling the movement function ---------------------------------------------------------------#
    particle_obj.particle_movement()

    # Update screen every frame -------------------------------------------------------------------#
    pygame.display.update()
    clock.tick(FPS)
