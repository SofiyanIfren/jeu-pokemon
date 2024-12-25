import pygame
import sys
import random

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pokemon Game")

# Charger l'image de fond
background_image = pygame.image.load('sprites/background_image.png')
# Redimensionner l'image de fond pour qu'elle prenne tout l'écran
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Initialiser le mixer de Pygame
pygame.mixer.init()

# Charger le fond musical
pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.play(-1)  # Jouer en boucle

# Charger le son de perte
lose_sound = pygame.mixer.Sound('sounds/lose_sound.mp3')

# Définir les couleurs
white = (255, 255, 255)
black = (0, 0, 0)

# Charger les images du joueur
player_images_right = [
    pygame.image.load('sprites/sacha_1.png'),
    pygame.image.load('sprites/sacha_2.png'),
    pygame.image.load('sprites/sacha_3.png')
]
player_images_left = [
    pygame.image.load('sprites/sacha_left_1.png'),
    pygame.image.load('sprites/sacha_left_2.png'),
    pygame.image.load('sprites/sacha_left_3.png')
]
player_size = player_images_right[0].get_size()
player_x = screen_width // 4
player_y = screen_height - player_size[1] - 75
player_speed = 5
player_jump = False
player_jump_count = 10

# Variables pour l'animation
animation_index = 0
animation_speed = 0.3

# Variables pour le défilement du terrain
terrain_speed = 15
terrain_x = 0
ground_image = pygame.image.load('sprites/sol.png')
ground_width = ground_image.get_width()

# Variables pour les obstacles
obstacle_image = pygame.image.load('sprites/obstacle.png')
obstacle_width = obstacle_image.get_width()
obstacle_height = obstacle_image.get_height()
obstacles = []
obstacle_frequency = 100  # Fréquence d'apparition des obstacles
obstacle_timer = 0
min_obstacle_distance = 200  # Distance minimale entre les obstacles

# Variables pour le système de vies
lives = 3
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
        if game_over_timer > 5 * 30:  # 5 secondes * 30 FPS
            game_over = False
            game_over_timer = 0
            lives -= 1
            if lives <= 0:
                running = False
            else:
                player_x = screen_width // 4
                player_y = screen_height - player_size[1] - 75
                player_jump = False
                player_jump_count = 10
                obstacles = []
                score = 0  # Réinitialiser le score
                pygame.mixer.music.play(-1)  # Reprendre la musique de fond

    if not game_over:
        # Gérer les mouvements du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not player_jump:
            player_jump = True

        # Gérer le saut
        if player_jump:
            if player_jump_count >= -10:
                neg = 1
                if player_jump_count < 0:
                    neg = -1
                player_y -= (player_jump_count ** 2) * 0.5 * neg
                player_jump_count -= 1
            else:
                player_jump = False
                player_jump_count = 10

        # Défilement du terrain
        if keys[pygame.K_RIGHT]:
            terrain_x -= terrain_speed
            animation_index += animation_speed
            if animation_index >= len(player_images_right):
                animation_index = 0
        elif keys[pygame.K_LEFT]:
            terrain_x += terrain_speed
            animation_index += animation_speed
            if animation_index >= len(player_images_left):
                animation_index = 0

        if terrain_x < -ground_width:
            terrain_x = 0
        elif terrain_x > 0:
            terrain_x = 0

        # Ajouter des obstacles aléatoirement
        obstacle_timer += 1
        if obstacle_timer > obstacle_frequency:
            if not obstacles or (obstacles and obstacles[-1][0] < screen_width - min_obstacle_distance):
                obstacles.append([screen_width, screen_height - ground_image.get_height() - obstacle_height + 10])
                obstacle_timer = 0

        # Déplacer les obstacles
        for obstacle in obstacles:
            if keys[pygame.K_RIGHT]:
                obstacle[0] -= terrain_speed
            elif keys[pygame.K_LEFT]:
                obstacle[0] += terrain_speed

        # Supprimer les obstacles hors de l'écran
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]

        # Vérifier les collisions avec les obstacles
        player_rect = pygame.Rect(player_x + 10, player_y + 10, player_size[0] - 20, player_size[1] - 20)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0] + 10, obstacle[1] + 10, obstacle_width - 20, obstacle_height - 20)
            if player_rect.colliderect(obstacle_rect):
                game_over = True

        # Incrémenter le score si le joueur dépasse un obstacle
        for obstacle in obstacles:
            if player_x > obstacle[0] + obstacle_width:
                score += 1
                obstacles.remove(obstacle)
                break

    # Dessiner l'image de fond
    screen.blit(background_image, (0, 0))

    # Dessiner le terrain
    for i in range(0, screen_width * 2, ground_width):
        screen.blit(ground_image, (terrain_x + i, screen_height - ground_image.get_height()))

    # Dessiner les obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle)

    # Dessiner l'image du joueur
    if keys[pygame.K_RIGHT]:
        screen.blit(player_images_right[int(animation_index)], (player_x, player_y))
    elif keys[pygame.K_LEFT]:
        screen.blit(player_images_left[int(animation_index)], (player_x, player_y))
    else:
        screen.blit(player_images_right[0], (player_x, player_y))

    # Afficher le nombre de vies
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Vies : {lives}', True, black)
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
