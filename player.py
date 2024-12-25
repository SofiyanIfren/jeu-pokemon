import pygame

class Player:
    def __init__(self, screen_width, screen_height, ground_image, terrain_speed):
        self.images_right = [
            pygame.image.load('sprites/sacha_1.png'),
            pygame.image.load('sprites/sacha_2.png'),
            pygame.image.load('sprites/sacha_3.png')
        ]
        self.images_left = [
            pygame.image.load('sprites/sacha_left_1.png'),
            pygame.image.load('sprites/sacha_left_2.png'),
            pygame.image.load('sprites/sacha_left_3.png')
        ]
        self.size = self.images_right[0].get_size()
        self.x = screen_width // 4
        self.y = screen_height - self.size[1] - 75
        self.speed = 5
        self.jumping = False
        self.jump_count = 10
        self.animation_index = 0
        self.animation_speed = 0.3
        self.direction = 'right'
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_image = ground_image
        self.terrain_speed = terrain_speed
        self.player_jump = False
        self.player_jump_count = 10
        self.lives = 3

    def reset(self):
        self.x = self.screen_width // 4
        self.y = self.screen_height - self.size[1] - 75
        self.jumping = False
        self.jump_count = 10
        self.animation_index = 0
        self.direction = 'right'

    def jump(self):
        self.jumping = True

    def update(self):
        if self.jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jumping = False
                self.jump_count = 10

    def move_right(self):
        self.x += self.speed
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images_right):
            self.animation_index = 0
        self.direction = 'right'

    def move_left(self):
        self.x -= self.speed
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images_left):
            self.animation_index = 0
        self.direction = 'left'

    def draw(self, screen):
        if self.direction == 'right':
            screen.blit(self.images_right[int(self.animation_index)], (self.x, self.y))
        else:
            screen.blit(self.images_left[int(self.animation_index)], (self.x, self.y))

    def draw_ground(self, screen, terrain_x):
        ground_width = self.ground_image.get_width()
        for i in range(0, self.screen_width * 2, ground_width):
            screen.blit(self.ground_image, (terrain_x + i, self.screen_height - self.ground_image.get_height()))

    def collides_with(self, obstacles):
        player_rect = pygame.Rect(self.x + 10, self.y + 10, self.size[0] - 20, self.size[1] - 20)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle.x + 10, obstacle.y + 10, obstacle.width - 20, obstacle.height - 20)
            if player_rect.colliderect(obstacle_rect):
                return True
        return False

    def has_passed(self, obstacle):
        return self.x > obstacle.x + obstacle.width
