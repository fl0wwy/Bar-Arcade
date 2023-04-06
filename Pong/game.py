import pygame
from sys import exit
import sprite
from random import choice

# Color list: https://www.pygame.org/docs/ref/color_list.html

# Initialization
pygame.init()
display = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

#Setup
pygame.display.set_caption('Pong')
game_state = 0

#Sprites
players = pygame.sprite.Group(sprite.Player(),sprite.Player_2())
ball = pygame.sprite.GroupSingle(sprite.Ball()) 

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
    players.draw(display)
    ball.update(display,game_state,players.sprites()[0],players.sprites()[1])
    players.update()
    players.sprites()[0].scoreboard(display,20)
    players.sprites()[1].scoreboard(display,780)
    
    # Game over
    if ball.sprite.rect.collidepoint((-10,ball.sprite.rect.y)) or ball.sprite.rect.collidepoint((810,ball.sprite.rect.y)): 
        if ball.sprite.rect.collidepoint((-10,ball.sprite.rect.y)):
            players.sprites()[1].score += 1
        else:
            players.sprites()[0].score += 1           
        
        for player in players.sprites():
            player.rect.y = 200
        ball.sprite.rect.center = (400,200)
        ball.sprite.direction = choice([0,1])
        ball.sprite.angle = 0

        game_state = 0
    # Display update and FPS
    pygame.display.update()
    clock.tick(60)