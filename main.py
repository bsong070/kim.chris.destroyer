import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800,600)) #width, height

# Background
background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1) #plays on loop


# Title and Icon
pygame.display.set_caption("Kim vs. Chris")
icon = pygame.image.load('ufo.jpg')
pygame.display.set_icon(icon)

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.jpg'))
    enemyX.append(random.randint(0,735)) #coordinates we want
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


# Player
playerImg = pygame.image.load('player.jpg')
playerX = 370 #coordinates we want
playerY = 480
playerX_change = 0

# bullet
# Ready - can't see the bullet on screen
# Fire - bullet is currently moving

bulletImg = pygame.image.load('bullet.jpg')
bulletX = 0 #coordinates we want
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX=10
textY=10

# game_over_text()

over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255)) #can click on screen (true)
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(x, y):
    screen.blit(playerImg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10)) #appear in center of spaceship

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    screen.fill((0,0,0)) #rgb - red green blue
    screen.blit(background,(0,0))# background image


    for event in pygame.event.get(): #every event that is happening gets inside pygame.event.get()
        if event.type == pygame.QUIT:  #if close button is pressed, turn to false
            running = False
        
        # if keystroke is pressed, check whether its left or right
        if event.type == pygame.KEYDOWN: #checks if keystroke is pressed
            
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play() #only want it to play once per shot
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # Checking boundaries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play() #only want it to play once per shot
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i], i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()