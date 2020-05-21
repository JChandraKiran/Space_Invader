import pygame
import random
from math import sqrt
from pygame import mixer

# initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)
# Player
playerImg = pygame.image.load('gaming.png')
playerx = 370
playery = 500
playerXchange = 0

# Enemy
enemyImg = []
enemyx = []
enemyy = []
enemyXchange = []
enemyYchange = []
no_of_enemys = 6
for i in range(no_of_enemys):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyx.append(random.randint(10, 730))
    enemyy.append(35)
    enemyXchange.append(1.5)
    enemyYchange.append(0.2)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 500
bulletXchange = 0
bulletYchange = 2
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

game_over_font = pygame.font.Font('freesansbold.ttf', 55)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    screen.blit(bulletImg(x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(a, b, c, d):
    distance = sqrt(((c - a) ** 2) + ((d - b) ** 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    gameover = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameover, (250, 250))


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking any key stroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerXchange = 5
            if event.key == pygame.K_LEFT:
                playerXchange = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play(0)
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerXchange = 0

    playerx += playerXchange
    if playerx >= 730:
        playerx = 730
    if playerx <= 10:
        playerx = 10
    # Enemy movements
    for i in range(no_of_enemys):
        # Game over
        if enemyy[i] > 475:
            for j in range(no_of_enemys):
                enemyy[j] = 2000
            game_over()
            break

        enemyx[i] += enemyXchange[i]
        if enemyx[i] >= 730:
            enemyXchange[i] = -1.5
        if enemyx[i] <= 10:
            enemyXchange[i] = 1.5

        enemyy[i] += enemyYchange[i]

        collision = isCollision(bulletx, bullety, enemyx[i], enemyy[i])
        if collision:
            bullety = 500
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(10, 730)
            enemyy[i] = 35
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
        enemy(enemyx[i], enemyy[i], i)
    # Bullet movement
    if bullet_state == 'fire':
        bullet_fire(bulletx, bullety)
        bullety -= bulletYchange
    if bullety == 0:
        bullety = 500
        bullet_state = 'ready'

    player(playerx, playery)
    show_score(10, 10)
    pygame.display.update()
