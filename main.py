import pygame
import random
import math
from pygame import mixer

# Initialise pygame
pygame.init()
# create screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
# Background music
# mixer.music.load('BG.wav')
# mixer.music.play(-1)

# Title
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
PlayerImage = pygame.image.load('battleship.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# Enemy
EnemyImage = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImage.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(3)
    EnemyY_change.append(40)

# Bullet
# Ready = You can't see the bullet
# Fire = Bullet in moving
BulletImage = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 7
Bullet_state = "Ready"


def player(x, y):
    screen.blit(PlayerImage, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImage[i], (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "Fire"
    screen.blit(BulletImage, (x + 16, y + 10))


def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((enemyx - bulletx) ** 2 + (enemyy - bullety) ** 2)
    if distance < 72:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Close Window
        if event.type == pygame.QUIT:
            running = False

        # Keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -3
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 3
            if event.key == pygame.K_SPACE:
                if Bullet_state is "Ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            PlayerX_change = 0

    PlayerX += PlayerX_change
    if PlayerX >= 736:
        PlayerX = 736
    elif PlayerX <= 0:
        PlayerX = 0

    for i in range(num_of_enemies):


        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] >= 736:
            EnemyX_change[i] = -3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] <= 0:
            EnemyX_change[i] = 3
            EnemyY[i] += EnemyY_change[i]

        Collision_State = collision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if Collision_State:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            BulletY = 480
            Bullet_state = "Ready"
            score_value += 1
            # Respawn
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)
        # Game Over
        if EnemyY[i] >= 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break


        enemy(EnemyX[i], EnemyY[i], i)
    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "Ready"
    if Bullet_state is "Fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
