import pygame
import sys
import random

from player import Player
from obstacle import Obstacle

# Initialiser Pygame + # Définir les couleurs
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pokemon Game")

# Charger l'image de fond
background_image = pygame.image.load('sprites/background_image.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Initialiser le mixer de Pygame + Charger le fond musical
pygame.mixer.init()
pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.play(-1)  # Jouer en boucle
lose_sound = pygame.mixer.Sound('sounds/lose_sound.mp3')

# Variables pour l'animation + défilement du terrain
animation_index = 0
animation_speed = 0.3
ground_speed = 15
ground_x = 0
ground_image = pygame.image.load('sprites/sol.png')
ground_width = ground_image.get_width()

# Instancier les objets du jeu
player_object = Player(screen_width, screen_height, ground_image, ground_speed)
obstacle_object = Obstacle(screen_width, screen_height, ground_image, ground_speed)

# Variables pour le système de vies
game_over = False
game_over_timer = 0

# Variable pour le score
score = 0

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        game_over_timer += 1
        if game_over_timer == 1:  # Jouer le son de perte une seule fois
            pygame.mixer.music.stop()
            lose_sound.play()
        if game_over_timer > 2 * 30:  # 2 secondes * 30 FPS
            game_over = False
            game_over_timer = 0
            player_object.lives -= 1
            if player_object.lives <= 0:
                running = False
            else:
                player_object.reset()
                ground_x = 0  # Réinitialiser la position du terrain
                pygame.mixer.music.play(-1)  # Reprendre la musique de fond
                obstacle_object.jumped_obstacles = []
                score = 0  # Réinitialiser le score
                pygame.mixer.music.play(-1)  # Reprendre la musique de fond

    if not game_over:
        # Gérer les mouvements du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not player_object.player_jump:
            player_object.player_jump = True

        # Gérer le saut
        if player_object.player_jump:
            if player_object.player_jump_count >= -10:
                neg = 1
                if player_object.player_jump_count < 0:
                    neg = -1
                player_object.y -= (player_object.player_jump_count ** 2) * 0.5 * neg
                player_object.player_jump_count -= 1
            else:
                player_object.player_jump = False
                player_object.player_jump_count = 10

        # Défilement du terrain
        if keys[pygame.K_RIGHT]:
            ground_x -= ground_speed
            animation_index += animation_speed
            if animation_index >= len(player_object.images_right):
                animation_index = 0
        elif keys[pygame.K_LEFT]:
            ground_x += ground_speed
            animation_index += animation_speed
            if animation_index >= len(player_object.images_left):
                animation_index = 0

        if ground_x < -ground_width:
            ground_x = 0
        elif ground_x > 0:
            ground_x = 0

        # Ajouter des obstacles aléatoirement
        obstacle_object.obstacle_timer += 1
        if obstacle_object.obstacle_timer > obstacle_object.obstacle_frequency:
            if not obstacle_object.jumped_obstacles or (obstacle_object.jumped_obstacles and obstacle_object.jumped_obstacles[-1][0] < screen_width - obstacle_object.min_obstacle_distance):
                obstacle_object.jumped_obstacles.append([screen_width, screen_height - ground_image.get_height() - obstacle_object.height + 10])
                obstacle_object.obstacle_timer = 0

        # Déplacer les obstacles
        for obstacle in obstacle_object.jumped_obstacles:
            if keys[pygame.K_RIGHT]:
                obstacle[0] -= ground_speed
            elif keys[pygame.K_LEFT]:
                obstacle[0] += ground_speed
        
        # Supprimer les obstacles hors de l'écran
        obstacles = [obstacle for obstacle in obstacle_object.jumped_obstacles if obstacle[0] > -obstacle_object.width]

        # Vérifier les collisions avec les obstacles
        player_rect = pygame.Rect(player_object.x + 10, player_object.y + 10, player_object.size[0] - 20, player_object.size[1] - 20)
        for obstacle in obstacle_object.jumped_obstacles:
            obstacle_rect = pygame.Rect(obstacle[0] + 10, obstacle[1] + 10, obstacle_object.width - 20, obstacle_object.height - 20)
            if player_rect.colliderect(obstacle_rect):
                game_over = True

        # Incrémenter le score si le joueur dépasse un obstacle
        for obstacle in obstacle_object.jumped_obstacles:
            if player_object.x > obstacle[0] + obstacle_object.width:
                score += 1
                obstacle_object.jumped_obstacles.remove(obstacle)
                break

    # Dessiner l'image de fond
    screen.blit(background_image, (0, 0))

    # Dessiner le terrain
    for i in range(0, screen_width * 2, ground_width):
        screen.blit(ground_image, (ground_x + i, screen_height - ground_image.get_height()))

    # Dessiner les obstacles
    for obstacle in obstacle_object.jumped_obstacles:
        screen.blit(obstacle_object.image, obstacle)

    # Dessiner l'image du joueur
    if keys[pygame.K_RIGHT]:
        screen.blit(player_object.images_right[int(animation_index)], (player_object.x, player_object.y))
    elif keys[pygame.K_LEFT]:
        screen.blit(player_object.images_left[int(animation_index)], (player_object.x, player_object.y))
    else:
        screen.blit(player_object.images_right[0], (player_object.x, player_object.y))

    # Afficher le nombre de vies
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Vies : {player_object.lives}', True, black)
    screen.blit(lives_text, (10, 10))

    # Afficher le score
    score_text = font.render(f'Score : {score}', True, black)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    # Afficher le message de game over
    if game_over:
        game_over_text = font.render('Game Over!', True, black)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de la boucle
    clock.tick(30)

# Quitter Pygame
pygame.quit()
sys.exit()
