import pygame
import random

class Obstacle:
    def __init__(self, screen_width, screen_height, ground_image, terrain_speed):
        self.image = pygame.image.load('sprites/obstacle.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = screen_width
        self.y = screen_height - ground_image.get_height() - self.height + 10
        self.screen_width = screen_width
        self.terrain_speed = terrain_speed
        self.jumped_obstacles = []
        self.obstacle_frequency = 100  # Fréquence d'apparition des obstacles
        self.obstacle_timer = 0
        self.min_obstacle_distance = 200  # Distance minimale entre les obstacles

    def move(self):
        self.x -= self.terrain_speed

    def is_on_screen(self):
        return self.x > -self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
