import pygame
from sys import exit
from sprite import *
from random import choice

# Color list: https://www.pygame.org/docs/ref/color_list.html

# Initialization
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

#Setup
pygame.display.set_caption('Pong')
game_state = 0
game_over_sound = pygame.mixer.Sound('materials/gameover_sfx.mp3')
game_over_sound.set_volume(0.1)
win_sfx = pygame.mixer.Sound('materials/eat_sfx.mp3')
win_sfx.set_volume(0.1)

#Sprites
player = pygame.sprite.GroupSingle(Player())
ai = pygame.sprite.GroupSingle(AI())
ball = pygame.sprite.GroupSingle(Ball()) 

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_state:
            if event.type == pygame.KEYDOWN:
                game_state = 1
    
    # Renders
    display.fill(pygame.Color('darkslategrey'))
    player.draw(display)
    ai.draw(display)
    ball.update(display,game_state,player.sprite,ai.sprite)
    player.update()
    ai.update(ball.sprite)
    player.sprite.scoreboard(display,20)
    ai.sprite.scoreboard(display,780)
    
    # Game over
    if ball.sprite.rect.collidepoint((-10,ball.sprite.rect.y)) or ball.sprite.rect.collidepoint((810,ball.sprite.rect.y)): 
        if ball.sprite.rect.collidepoint((-10,ball.sprite.rect.y)):
            game_over_sound.play()
            ai.sprite.score += 1
        else:
            win_sfx.play()
            player.sprite.score += 1           
        
        player.sprite.rect.centery = 200
        ai.sprite.rect.centery = 200
        ball.sprite.rect.center = (400,200)
        ball.sprite.direction = choice([0,1])
        ball.sprite.angle = 0

        game_state = 0
    # Display update and FPS
    pygame.display.update()
    clock.tick(60)